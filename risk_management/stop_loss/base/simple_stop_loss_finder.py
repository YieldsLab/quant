from typing import Type
from ohlcv.context import OhlcvContext
from risk_management.stop_loss.base.abstract_stop_loss_finder import AbstractStopLoss
from shared.meta_label import meta_label
from shared.position_side import PositionSide


@meta_label
class SimpleStopLossFinder(AbstractStopLoss):
    NAME = 'SIMPLE'

    def __init__(self, ohlcv: Type[OhlcvContext], stop_loss_pct=0.02):
        super().__init__(ohlcv)
        self.stop_loss_pct = stop_loss_pct

    def next(self, position_side, entry_price):
        if position_side == PositionSide.LONG:
            stop_loss_price = entry_price * (1.0 - self.stop_loss_pct)
        elif position_side == PositionSide.SHORT:
            stop_loss_price = entry_price * (1.0 + self.stop_loss_pct)

        return stop_loss_price