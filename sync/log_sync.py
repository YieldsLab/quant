from core.abstract_event_manager import AbstractEventManager
from core.event_decorators import register_handler
from core.events.backtest import BacktestStarted
from core.events.ohlcv import NewMarketDataReceived
from core.events.portfolio import PortfolioPerformanceUpdated
from core.events.position import ActivePositionOpened, PositionClosed, OrderFilled, ClosePositionPrepared, LongPositionOpened, ShortPositionOpened
from core.events.risk import RiskThresholdBreached
from core.events.strategy import ExitLongSignalReceived, ExitShortSignalReceived, GoLongSignalReceived, GoShortSignalReceived


class LogSync(AbstractEventManager):
    def __init__(self):
        super().__init__()

    @register_handler(NewMarketDataReceived)
    async def _log_market(self, event: NewMarketDataReceived):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(BacktestStarted)
    async def _log_backtest(self, event: BacktestStarted):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(GoLongSignalReceived)
    async def _log_go_long(self, event: GoLongSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(GoShortSignalReceived)
    async def _log_go_short(self, event: GoShortSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(OrderFilled)
    async def _log_fill_order(self, event: OrderFilled):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(LongPositionOpened)
    async def _log_open_long_position(self, event: LongPositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ShortPositionOpened)
    async def _log_open_short_position(self, event: ShortPositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ActivePositionOpened)
    async def _log_evaluate_risk(self, event: ActivePositionOpened):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(RiskThresholdBreached)
    async def _log_exit_risk(self, event: RiskThresholdBreached):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ExitLongSignalReceived)
    async def _log_exit_long(self, event: ExitLongSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ExitShortSignalReceived)
    async def _log_exit_short(self, event: ExitShortSignalReceived):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(ClosePositionPrepared)
    async def _log_close_position(self, event: ClosePositionPrepared):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(PositionClosed)
    async def _log_closed_position(self, event: PositionClosed):
        print('----------------------------------------------------->')
        print(event)

    @register_handler(PortfolioPerformanceUpdated)
    async def _log_portfolio_performance(self, event: PortfolioPerformanceUpdated):
        print('----------------------------------------------------->')
        print(event)
