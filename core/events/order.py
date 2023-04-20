from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from ..timeframe import Timeframe
from ..event_dispatcher import Event

class OrderSide(Enum):
    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value

@dataclass
class Order:
    side: OrderSide
    entry: float
    size: float
    stop_loss: float
    take_profit: Optional[float] = None
    id: Optional[str] = None
    timestamp: int = datetime.now().timestamp()

    def to_dict(self):
        return asdict(self)
    
    def __hash__(self):
        return hash((self.side, self.entry, self.size, self.stop_loss, self.take_profit, self.id, self.timestamp))

@dataclass(frozen=True)
class FillOrder(Event):
    symbol: str
    timeframe: Timeframe
    order: Order
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    