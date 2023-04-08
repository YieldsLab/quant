

from shared.meta_label import meta_label
from ta.base.abstract_indicator import AbstractIndicator
from ta.base.ma import MovingAverage


@meta_label
class MACD(AbstractIndicator):
    NAME = 'MACD'

    def __init__(self, short_period=12, long_period=26, signal_period=9):
        super().__init__()
        self.fast_ema = MovingAverage(window=short_period)
        self.slow_ema = MovingAverage(window=long_period)
        self.signal_ema = MovingAverage(window=signal_period)

    def call(self, data):
        ema_fast = self.fast_ema.ema(data['close'])
        ema_slow = self.fast_ema.ema(data['close'])

        macd = ema_fast - ema_slow
        signal_line = self.signal_ema.ema(macd)
        histogram = macd - signal_line

        return macd, signal_line, histogram