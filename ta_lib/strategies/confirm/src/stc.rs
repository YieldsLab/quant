use base::prelude::*;
use core::prelude::*;
use momentum::stc;

const LOWER_LINE: f32 = 25.;
const UPPER_LINE: f32 = 75.;

pub struct STCConfirm {
    smooth_type: Smooth,
    fast_period: usize,
    slow_period: usize,
    cycle: usize,
    d_first: usize,
    d_second: usize,
}

impl STCConfirm {
    pub fn new(
        smooth_type: Smooth,
        fast_period: f32,
        slow_period: f32,
        cycle: f32,
        d_first: f32,
        d_second: f32,
    ) -> Self {
        Self {
            smooth_type,
            fast_period: fast_period as usize,
            slow_period: slow_period as usize,
            cycle: cycle as usize,
            d_first: d_first as usize,
            d_second: d_second as usize,
        }
    }
}

impl Confirm for STCConfirm {
    fn lookback(&self) -> usize {
        let adj_lookback_one = std::cmp::max(self.fast_period, self.slow_period);
        let adj_lookback_two = std::cmp::max(adj_lookback_one, self.cycle);
        let adj_lookback_three = std::cmp::max(adj_lookback_two, self.d_first);
        std::cmp::max(adj_lookback_three, self.d_second)
    }

    fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let stc = stc(
            &data.close,
            self.smooth_type,
            self.fast_period,
            self.slow_period,
            self.cycle,
            self.d_first,
            self.d_second,
        );
        let prev_stc = stc.shift(1);

        (
            stc.sgt(&prev_stc) & stc.sgt(&UPPER_LINE),
            stc.slt(&prev_stc) & stc.slt(&LOWER_LINE),
        )
    }
}
