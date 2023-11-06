from enum import Enum, auto
from typing import Union

from core.actors.base import BaseActor
from core.events.ohlcv import NewMarketDataReceived
from core.events.position import (
    BrokerPositionClosed,
    BrokerPositionOpened,
    PositionCloseRequested,
    PositionInitialized,
)
from core.models.ohlcv import OHLCV
from core.models.order import Order, OrderStatus
from core.models.position import PositionSide
from core.models.strategy import Strategy
from core.models.symbol import Symbol
from core.models.timeframe import Timeframe

OrderEventType = Union[
    NewMarketDataReceived, PositionInitialized, PositionCloseRequested
]
PositionEventType = Union[PositionInitialized, PositionCloseRequested]


class PriceDirection(Enum):
    OHLC = auto()
    OLHC = auto()


class PaperOrderExecutor(BaseActor):
    _POSITION_EVENTS = [PositionInitialized, PositionCloseRequested]

    def __init__(self, symbol: Symbol, timeframe: Timeframe, strategy: Strategy):
        super().__init__(symbol, timeframe, strategy)
        self.last_tick = None

    async def start(self):
        await super().start()

        self._dispatcher.register(
            NewMarketDataReceived, self.handle, self._filter_market_event
        )

        for event in self._POSITION_EVENTS:
            self._dispatcher.register(event, self.handle, self._filter_position_event)

    async def stop(self):
        await super().stop()

        self._dispatcher.unregister(NewMarketDataReceived, self.handle)

        for event in self._POSITION_EVENTS:
            self._dispatcher.unregister(event, self.handle)

    async def handle(self, event: OrderEventType):
        handlers = {
            PositionInitialized: self._execute_order,
            PositionCloseRequested: self._close_position,
            NewMarketDataReceived: self._update_tick,
        }

        handler = handlers.get(type(event))

        if handler:
            await handler(event)

    def _filter_market_event(self, event: NewMarketDataReceived):
        return event.symbol == self._symbol and event.timeframe == self._timeframe

    def _filter_position_event(self, event: PositionEventType):
        signal = event.position.signal
        return signal.symbol == self._symbol and signal.timeframe == self._timeframe

    async def _execute_order(self, event: PositionInitialized):
        current_position = event.position
        fill_price = self._determine_fill_price(current_position.side)

        order = Order(
            status=OrderStatus.EXECUTED,
            price=fill_price,
            size=current_position.size,
        )

        next_position = current_position.add_order(order).update_prices(order.price)

        await self.dispatch(BrokerPositionOpened(next_position))

    async def _close_position(self, event: PositionCloseRequested):
        current_position = event.position
        fill_price = self._determine_fill_price(current_position.side)

        if current_position.closed:
            next_position = current_position.update_prices(fill_price)
        else:
            next_position = current_position.close(event.meta.timestamp).update_prices(
                fill_price
            )

        await self.dispatch(BrokerPositionClosed(next_position))

    async def _update_tick(self, event: NewMarketDataReceived):
        self.last_tick = event.ohlcv

    @staticmethod
    def _intrabar_price_movement(tick: OHLCV) -> PriceDirection:
        return (
            PriceDirection.OHLC
            if abs(tick.open - tick.high) < abs(tick.open - tick.low)
            else PriceDirection.OLHC
        )

    def _determine_fill_price(self, side: PositionSide) -> float:
        direction = self._intrabar_price_movement(self.last_tick)

        if side == PositionSide.LONG and direction == PriceDirection.OHLC:
            return self.last_tick.high
        elif side == PositionSide.SHORT and direction == PriceDirection.OLHC:
            return self.last_tick.low
        else:
            return self.last_tick.close
