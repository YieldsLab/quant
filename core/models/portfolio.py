from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BasicPortfolioPerformance:
    total_trades: int
    successful_trades: int
    win_rate: float
    risk_of_ruin: float
    rate_of_return: float
    annualized_return: float
    annualized_volatility: float
    total_pnl: float
    average_pnl: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    max_drawdown: float
    calmar_ratio: float
    recovery_factor: float

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class AdvancedPortfolioPerformance:
    sharpe_ratio: float
    sortino_ratio: float
    lake_ratio: float
    burke_ratio: float
    rachev_ratio: float
    tail_ratio: float
    omega_ratio: float
    sterling_ratio: float
    kappa_three_ratio: float
    profit_factor: float
    skewness: float
    kurtosis: float
    var: float
    cvar: float
    ulcer_index: float

    def to_dict(self):
        return asdict(self)
