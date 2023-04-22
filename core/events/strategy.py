from dataclasses import dataclass, field

from .base_event import Event, EventMeta
from ..timeframe import Timeframe

@dataclass(order=True)
class StrategyEvent(Event):
    symbol: str
    timeframe: Timeframe
    strategy: str
    entry: float
    stop_loss: float
    take_profit: float
    meta: EventMeta = field(default_factory=lambda: EventMeta(priority=1))

@dataclass(order=True)
class GoLong(StrategyEvent):
    pass

@dataclass(order=True)
class GoShort(StrategyEvent):
    pass