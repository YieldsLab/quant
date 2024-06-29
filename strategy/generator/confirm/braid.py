from dataclasses import dataclass

from core.models.parameter import (
    CategoricalParameter,
    Parameter,
    StaticParameter,
)
from core.models.smooth import Smooth, SmoothATR

from .base import Confirm, ConfirmType


@dataclass(frozen=True)
class BraidConfirm(Confirm):
    type: Confirm = ConfirmType.Braid
    smooth_type: Parameter = CategoricalParameter(Smooth)
    fast_period: Parameter = StaticParameter(5.0)
    slow_period: Parameter = StaticParameter(21.0)
    open_period: Parameter = StaticParameter(9.0)
    strength: Parameter = StaticParameter(40.0)
    smooth_atr: Parameter = CategoricalParameter(SmoothATR)
    period_atr: Parameter = StaticParameter(14.0)