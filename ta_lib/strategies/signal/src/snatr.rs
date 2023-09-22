use base::{OHLCVSeries, Signal};
use core::Series;
use volatility::snatr;

pub struct SNATRSignal {
    atr_period: usize,
    atr_smoothing_period: usize,
    lower_barrier: f32,
    upper_barrier: f32,
}

impl SNATRSignal {
    pub fn new(
        atr_period: f32,
        atr_smoothing_period: f32,
        lower_barrier: f32,
        upper_barrier: f32,
    ) -> Self {
        Self {
            atr_period: atr_period as usize,
            atr_smoothing_period: atr_smoothing_period as usize,
            lower_barrier,
            upper_barrier,
        }
    }
}

impl Signal for SNATRSignal {
    fn id(&self) -> String {
        format!(
            "SNATR_{}:{}:{}:{}",
            self.atr_period, self.atr_smoothing_period, self.lower_barrier, self.upper_barrier
        )
    }

    fn lookback(&self) -> usize {
        std::cmp::max(self.atr_period, self.atr_smoothing_period)
    }

    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let snatr = snatr(
            &data.high,
            &data.low,
            &data.close,
            self.atr_period,
            self.atr_smoothing_period,
        );

        (
            snatr.cross_under_line(self.upper_barrier),
            snatr.cross_over_line(self.lower_barrier),
        )
    }

    fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        (Series::empty(1), Series::empty(1))
    }
}