from core.event_dispatcher import register_handler
from core.events.order import FillOrder, Order, OrderSide
from core.events.position import ClosePosition, ClosedPosition, OpenLongPosition, OpenShortPosition
from .abstract_trader import AbstractTrader

class PaperTrader(AbstractTrader):
    def __init__(self):
        super().__init__()

    @register_handler(OpenLongPosition)
    async def _open_long_position(self, event: OpenLongPosition):
        await self.trade(event)

    @register_handler(OpenShortPosition)
    async def _open_short_position(self, event: OpenShortPosition):
        await self.trade(event)

    @register_handler(ClosePosition)
    async def _on_close_position(self, event: ClosePosition):
        await self.dispatcher.dispatch(ClosedPosition(symbol=event.symbol, timeframe=event.timeframe, exit_price=event.exit_price))
        
    async def trade(self, event):
        order_side = OrderSide.BUY if isinstance(event, OpenLongPosition) else OrderSide.SELL
        order = Order(side=order_side, entry=event.entry, size=event.size, stop_loss=event.stop_loss, take_profit=event.take_profit)
        
        await self.dispatcher.dispatch(FillOrder(symbol=event.symbol, timeframe=event.timeframe, order=order))