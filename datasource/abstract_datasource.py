from abc import ABC, abstractmethod
from typing import List

from core.timeframe import Timeframe


class AbstractDatasource(ABC):
    @abstractmethod
    def fetch(self, symbol: str, timeframe: Timeframe):
        pass
    
    @abstractmethod
    def account_size(self):
        pass

    @abstractmethod
    def symbols(self) -> List[str]:
        pass
    
    @abstractmethod
    def fee_and_precisions(self, symbol: str):
        pass
