import logging
from typing import Union

from core.actors import Actor
from core.events.backtest import BacktestEnded
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionClosed,
    PositionCloseRequested,
    PositionInitialized,
    PositionOpened,
)
from core.events.risk import RiskThresholdBreached
from core.events.signal import (
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    GoLongSignalReceived,
    GoShortSignalReceived,
)
from core.interfaces.abstract_config import AbstractConfig
from core.interfaces.abstract_position_factory import AbstractPositionFactory
from core.models.position import Position, PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

from ._sm import PositionStateMachine
from ._state import PositionStorage

SignalEvent = Union[GoLongSignalReceived, GoShortSignalReceived]
BrokerPositionEvent = Union[BrokerPositionOpened, BrokerPositionClosed]
ExitSignal = Union[
    GoLongSignalReceived,
    GoShortSignalReceived,
    ExitLongSignalReceived,
    ExitShortSignalReceived,
    RiskThresholdBreached,
    BacktestEnded,
]

PositionEvent = Union[SignalEvent, ExitSignal, BrokerPositionEvent]

logger = logging.getLogger(__name__)


class PositionActor(Actor):
    _EVENTS = [
        GoLongSignalReceived,
        GoShortSignalReceived,
        ExitLongSignalReceived,
        ExitShortSignalReceived,
        BacktestEnded,
        BrokerPositionOpened,
        BrokerPositionClosed,
        RiskThresholdBreached,
    ]

    def __init__(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        strategy: Strategy,
        position_factory: AbstractPositionFactory,
        config_service: AbstractConfig,
    ):
        super().__init__(symbol, timeframe, strategy)
        self.position_factory = position_factory

        self.sm = PositionStateMachine(self)
        self.state = PositionStorage()
        self.config = config_service.get("position")

    def pre_receive(self, event: PositionEvent) -> bool:
        symbol, timeframe = self._get_event_key(event)
        return self._symbol == symbol and self._timeframe == timeframe

    async def on_receive(self, event):
        symbol, _ = self._get_event_key(event)
        await self.sm.process_event(symbol, event)

    async def handle_signal_received(self, event: SignalEvent) -> bool:
        async def create_and_store_position(event: SignalEvent):
            position = await self.position_factory.create_position(
                event.signal, event.ohlcv, event.entry_price, event.stop_loss
            )

            await self.state.store_position(position)
            await self.tell(PositionInitialized(position))
            return True

        symbol, timeframe = self._get_event_key(event)

        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if not long_position and isinstance(event, GoLongSignalReceived):
            return await create_and_store_position(event)

        if not short_position and isinstance(event, GoShortSignalReceived):
            return await create_and_store_position(event)

        return False

    async def handle_reverse_position(self, event: SignalEvent):
        symbol, timeframe = self._get_event_key(event)

        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if (
            long_position
            and isinstance(event, GoShortSignalReceived)
            and long_position.entry_price < event.entry_price
        ):
            await self.tell(PositionCloseRequested(long_position, event.entry_price))
            return True

        if (
            short_position
            and isinstance(event, GoLongSignalReceived)
            and short_position.entry_price > event.entry_price
        ):
            await self.tell(PositionCloseRequested(short_position, event.entry_price))
            return True

        return False

    async def handle_position_opened(self, event: BrokerPositionOpened) -> bool:
        await self.state.update_stored_position(event.position)
        await self.tell(PositionOpened(event.position))
        return True

    async def handle_position_closed(self, event: BrokerPositionClosed) -> bool:
        await self.state.close_stored_position(event.position)
        await self.tell(PositionClosed(event.position))
        return True

    async def handle_exit_received(self, event: ExitSignal) -> bool:
        symbol, timeframe = self._get_event_key(event)

        async def try_close_position(position: Position) -> bool:
            if (
                position
                and position.last_modified < event.meta.timestamp
                and self.can_close_position(event, position)
            ):
                await self.tell(PositionCloseRequested(position, event.exit_price))
                return True
            return False

        long_position, short_position = await self.state.retrieve_position(
            symbol, timeframe
        )

        if await try_close_position(long_position) or await try_close_position(
            short_position
        ):
            return True

        return False

    def can_close_position(self, event, position: Position) -> bool:
        if (
            position.side == PositionSide.LONG
            and isinstance(event, ExitLongSignalReceived)
        ) or (
            position.side == PositionSide.SHORT
            and isinstance(event, ExitShortSignalReceived)
        ):
            close_to_tp = abs(event.exit_price - position.take_profit_price)
            close_to_sl = abs(position.stop_loss_price - event.exit_price)

            return (
                close_to_tp >= self.config["tp_threshold"]
                or close_to_sl <= self.config["sl_threshold"]
            )

        if (
            isinstance(event, RiskThresholdBreached)
            and position.side == event.position.side
        ):
            return True

        if isinstance(event, BacktestEnded):
            return True

        return False

    @staticmethod
    def _get_event_key(event: PositionEvent):
        signal = (
            event.signal
            if hasattr(event, "signal")
            else event.position.signal
            if hasattr(event, "position")
            else event
        )

        return (signal.symbol, signal.timeframe)
