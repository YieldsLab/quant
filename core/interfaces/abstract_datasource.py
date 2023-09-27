from abc import ABC, abstractmethod

from core.models.symbol import Symbol
from core.models.timeframe import Timeframe


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: Symbol, timeframe: Timeframe, lookback: int):
        pass
