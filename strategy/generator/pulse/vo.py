from dataclasses import dataclass

from core.models.parameter import Parameter, StaticParameter

from .base import Pulse, PulseType


@dataclass(frozen=True)
class VoPulse(Pulse):
    type: PulseType = PulseType.Vo
    short_period: Parameter = StaticParameter(7.0)
    long_period: Parameter = StaticParameter(13.0)
