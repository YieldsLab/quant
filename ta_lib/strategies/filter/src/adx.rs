use base::{Filter, OHLCVSeries, Price};
use core::Series;
use trend::dmi;

pub struct ADXFilter {
    adx_period: usize,
    di_period: usize,
    threshold: f32,
}

impl ADXFilter {
    pub fn new(adx_period: f32, di_period: f32, threshold: f32) -> Self {
        Self {
            adx_period: adx_period as usize,
            di_period: di_period as usize,
            threshold,
        }
    }
}

impl Filter for ADXFilter {
    fn lookback(&self) -> usize {
        std::cmp::max(self.adx_period, self.di_period)
    }

    fn apply(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let (adx, _, _) = dmi(
            &data.high,
            &data.low,
            &data.atr(self.di_period),
            self.adx_period,
            self.di_period,
        );

        (adx.sgt(self.threshold), adx.sgt(self.threshold))
    }
}