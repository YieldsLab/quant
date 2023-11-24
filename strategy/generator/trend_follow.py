from enum import Enum, auto
from itertools import product
from random import shuffle
from symtable import Symbol

import numpy as np

from core.interfaces.abstract_strategy_generator import AbstractStrategyGenerator
from core.models.candle import TrendCandleType
from core.models.parameter import RandomParameter, StaticParameter
from core.models.strategy import Strategy, StrategyType
from core.models.timeframe import Timeframe
from strategy.exit.ast import AstExit
from strategy.exit.ce import ChExit
from strategy.exit.dumb import DumbExit
from strategy.exit.highlow import HighLowExit
from strategy.exit.ma import MovingAverageExit
from strategy.exit.pattern import PatternExit
from strategy.exit.rsi import RSIExit
from strategy.regime.adx import ADXFilter
from strategy.regime.apo import APOFilter
from strategy.regime.bop import BOPFilter
from strategy.regime.braid import BraidFilter
from strategy.regime.eis import EISFilter
from strategy.regime.fib import FibFilter
from strategy.regime.ma import MovingAverageFilter
from strategy.regime.macd import MACDFilter
from strategy.regime.ribbon import RibbonFilter
from strategy.regime.rsi import RSIFilter
from strategy.regime.stoch import StochFilter
from strategy.regime.supertrend import SupertrendFilter
from strategy.regime.tii import TIIFilter
from strategy.signal.ao_flip import AOFlipSignal
from strategy.signal.ao_saucer import AOSaucerSignal
from strategy.signal.apo_flip import APOFlipSignal
from strategy.signal.bop_flip import BOPFlipSignal
from strategy.signal.cc_flip import CCFlipSignal
from strategy.signal.dch_two_ma import DCH2MovingAverageSignal
from strategy.signal.di_cross import DICrossSignal
from strategy.signal.di_flip import DIFlipSignal
from strategy.signal.dmi_cross import DMICrossSignal
from strategy.signal.hl import HighLowSignal
from strategy.signal.kst_cross import KSTCrossSignal
from strategy.signal.ma_three_cross import MA3CrossSignal
from strategy.signal.macd_color_switch import MACDColorSwitchSignal
from strategy.signal.macd_cross import MACDCrossSignal
from strategy.signal.macd_flip import MACDFlipSignal
from strategy.signal.qstick_cross import QSTICKCrossSignal
from strategy.signal.qstick_flip import QSTICKFlipSignal
from strategy.signal.quadruple import QuadrupleSignal
from strategy.signal.roc_flip import ROCFlipSignal
from strategy.signal.rsi_ma_pullback import RSIMovingAveragePullbackSignal
from strategy.signal.rsi_neutrality_cross import RSINautralityCrossSignal
from strategy.signal.rsi_neutrality_pullback import RSINautralityPullbackSignal
from strategy.signal.rsi_neutrality_rejection import RSINautralityRejectionSignal
from strategy.signal.rsi_two_ma import RSI2MovingAverageSignal
from strategy.signal.rsi_v import RSIVSignal
from strategy.signal.snatr import SNATRSignal
from strategy.signal.stc_flip import STCFlipSignal
from strategy.signal.stc_uturn import STCUTurnSignal
from strategy.signal.stoch_cross import StochCrossSignal
from strategy.signal.supertrend_flip import SupertrendFlipSignal
from strategy.signal.supertrend_pullback import SupertrendPullBackSignal
from strategy.signal.testing_ground import TestingGroundSignal
from strategy.signal.tii_cross import TIICrossSignal
from strategy.signal.tii_v import TIIVSignal
from strategy.signal.trend_candle import TrendCandleSignal
from strategy.signal.trix_cross import TRIXCrossSignal
from strategy.signal.trix_flip import TRIXFlipSignal
from strategy.signal.tsi_cross import TSICrossSignal
from strategy.signal.tsi_flip import TSIFlipSignal
from strategy.signal.vwap_cross import VWAPCrossSignal
from strategy.stop_loss.atr import ATRStopLoss
from strategy.volume.dumb import DumbVolume
from strategy.volume.osc import OSCVolume


class TrendSignalType(Enum):
    CROSS = auto()
    FLIP = auto()
    V = auto()
    UTurn = auto()
    TWO_MA = auto()
    CUSTOM = auto()
    PULLBACK = auto()


class TrendFollowStrategyGenerator(AbstractStrategyGenerator):
    def __init__(
        self,
        n_samples: int,
        symbols: list[Symbol],
        timeframes: list[Timeframe],
    ):
        super().__init__()
        self.n_samples = n_samples
        self.timeframes = timeframes
        self.symbols = symbols

    def generate(self) -> list[tuple[Symbol, Timeframe, Strategy]]:
        strategies = self.generate_strategies()
        sampled_symbols = self.generate_symbols()
        sampled_timeframes = self.generate_timeframes()

        data = list(product(sampled_symbols, sampled_timeframes, strategies))

        shuffle(data)

        return data

    def generate_strategies(self) -> list[Strategy]:
        return self._diversified_strategies() + self._random_strategies()

    def generate_symbols(self) -> list[Symbol]:
        num_symbols_to_sample = min(self.n_samples, len(self.symbols))

        return np.random.choice(self.symbols, size=num_symbols_to_sample, replace=False)

    def generate_timeframes(self) -> list[Timeframe]:
        num_timeframes_to_sample = min(self.n_samples, len(self.timeframes))

        return np.random.choice(
            self.timeframes, size=num_timeframes_to_sample, replace=False
        )

    def _diversified_strategies(self):
        stop_loss = ATRStopLoss(
            period=StaticParameter(14.0), multi=StaticParameter(1.0)
        )
        regime = RSIFilter()
        exit = DumbExit()
        volume = DumbVolume()
        strategies = [
            (
                StrategyType.TREND,
                TrendCandleSignal(
                    candle=StaticParameter(TrendCandleType.DOUBLE_TROUBLE)
                ),
                regime,
                volume,
                stop_loss,
                exit,
            ),
            (
                StrategyType.TREND,
                SupertrendFlipSignal(),
                regime,
                volume,
                stop_loss,
                exit,
            ),
        ]

        return [Strategy(*strategy) for strategy in strategies]

    def _random_strategies(self):
        strategies_set = set()

        def add_strategy():
            strategy = self._generate_strategy()
            if strategy not in strategies_set:
                strategies_set.add(strategy)

        for _ in range(self.n_samples):
            add_strategy()

        remainders = self.n_samples - len(strategies_set)

        for _ in range(remainders):
            add_strategy()

        return list(strategies_set)

    def _generate_strategy(self):
        signal_groups = list(TrendSignalType)
        entry_signal = self._generate_signal(np.random.choice(signal_groups))
        regime = np.random.choice(
            [
                MovingAverageFilter(period=RandomParameter(150.0, 300.0, 25.0)),
                RSIFilter(),
                ADXFilter(),
                TIIFilter(),
                StochFilter(),
                SupertrendFilter(),
                MACDFilter(),
                RibbonFilter(),
                FibFilter(),
                EISFilter(),
                BraidFilter(),
                APOFilter(),
                BOPFilter(),
            ]
        )
        volume = np.random.choice([DumbVolume(), OSCVolume()])
        stop_loss = np.random.choice(
            [ATRStopLoss(multi=RandomParameter(0.85, 1.8, 0.15))]
        )
        exit_signal = np.random.choice(
            [
                AstExit(),
                ChExit(),
                DumbExit(),
                PatternExit(),
                HighLowExit(),
                MovingAverageExit(),
                RSIExit(),
            ]
        )

        return Strategy(
            *(StrategyType.TREND, entry_signal, regime, volume, stop_loss, exit_signal)
        )

    def _generate_signal(self, signal: TrendSignalType):
        ma_short_period, ma_medium_period, ma_long_period = sorted(
            [
                RandomParameter(20.0, 50.0, 5.0),
                RandomParameter(50.0, 100.0, 5.0),
                RandomParameter(50.0, 200.0, 10.0),
            ]
        )

        if signal == TrendSignalType.FLIP:
            return np.random.choice(
                [
                    AOFlipSignal(),
                    MACDFlipSignal(),
                    SupertrendFlipSignal(),
                    ROCFlipSignal(),
                    TRIXFlipSignal(),
                    TSIFlipSignal(),
                    DIFlipSignal(),
                    QSTICKFlipSignal(),
                    CCFlipSignal(),
                    STCFlipSignal(),
                    APOFlipSignal(),
                    BOPFlipSignal(),
                ]
            )
        if signal == TrendSignalType.V:
            return np.random.choice([TIIVSignal(), RSIVSignal()])

        if signal == TrendSignalType.UTurn:
            return np.random.choice([STCUTurnSignal()])

        if signal == TrendSignalType.CROSS:
            return np.random.choice(
                [
                    MA3CrossSignal(
                        short_period=ma_short_period,
                        medium_period=ma_medium_period,
                        long_period=ma_long_period,
                    ),
                    MACDCrossSignal(),
                    TIICrossSignal(),
                    RSINautralityCrossSignal(),
                    TSICrossSignal(),
                    DICrossSignal(),
                    QSTICKCrossSignal(),
                    VWAPCrossSignal(),
                    DMICrossSignal(),
                    StochCrossSignal(),
                    KSTCrossSignal(),
                    TRIXCrossSignal(),
                ]
            )
        if signal == TrendSignalType.TWO_MA:
            return np.random.choice(
                [
                    RSI2MovingAverageSignal(),
                    DCH2MovingAverageSignal(),
                ]
            )
        if signal == TrendSignalType.PULLBACK:
            return np.random.choice(
                [
                    SupertrendPullBackSignal(),
                    RSINautralityPullbackSignal(),
                    RSIMovingAveragePullbackSignal(),
                ]
            )

        return np.random.choice(
            [
                AOSaucerSignal(),
                MACDColorSwitchSignal(),
                TrendCandleSignal(),
                SNATRSignal(),
                RSINautralityRejectionSignal(),
                TestingGroundSignal(period=ma_long_period),
                QuadrupleSignal(),
                HighLowSignal(),
            ]
        )
