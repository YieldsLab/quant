use base::prelude::*;
use core::prelude::*;
use momentum::trix;

pub struct TrixSignalLineSignal {
    smooth_type: Smooth,
    period: usize,
    signal_period: usize,
}

impl TrixSignalLineSignal {
    pub fn new(smooth_type: Smooth, period: f32, signal_period: f32) -> Self {
        Self {
            smooth_type,
            period: period as usize,
            signal_period: signal_period as usize,
        }
    }
}

impl Signal for TrixSignalLineSignal {
    fn lookback(&self) -> usize {
        std::cmp::max(self.period, self.signal_period)
    }

    fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let trix = trix(&data.close(), self.smooth_type, self.period);
        let signal_line = trix.smooth(self.smooth_type, self.signal_period);

        (
            trix.cross_over(&signal_line),
            trix.cross_under(&signal_line),
        )
    }
}
