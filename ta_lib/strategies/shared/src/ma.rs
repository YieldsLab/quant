use base::OHLCVSeries;
use core::Series;
use trend::{
    alma, dema, ema, frama, gma, hma, kama, lsma, rmsma, sinwma, sma, smma, t3, tema, tma, vwma,
    wma, zlema, zlsma,
};

pub enum MovingAverageType {
    ALMA,
    DEMA,
    EMA,
    FRAMA,
    GMA,
    HMA,
    KAMA,
    LSMA,
    RMSMA,
    SINWMA,
    SMA,
    SMMA,
    TTHREE,
    TEMA,
    TMA,
    VWMA,
    WMA,
    ZLEMA,
    ZLSMA,
}

pub fn ma_indicator(
    smoothing: &MovingAverageType,
    data: &OHLCVSeries,
    period: usize,
) -> Series<f32> {
    match smoothing {
        MovingAverageType::ALMA => alma(&data.close, period, 0.85, 6.0),
        MovingAverageType::DEMA => dema(&data.close, period),
        MovingAverageType::EMA => ema(&data.close, period),
        MovingAverageType::FRAMA => frama(&data.high, &data.low, &data.close, period),
        MovingAverageType::GMA => gma(&data.close, period),
        MovingAverageType::HMA => hma(&data.close, period),
        MovingAverageType::KAMA => kama(&data.close, period),
        MovingAverageType::LSMA => lsma(&data.close, period),
        MovingAverageType::RMSMA => rmsma(&data.close, period),
        MovingAverageType::SINWMA => sinwma(&data.close, period),
        MovingAverageType::SMA => sma(&data.close, period),
        MovingAverageType::SMMA => smma(&data.close, period),
        MovingAverageType::TTHREE => t3(&data.close, period),
        MovingAverageType::TEMA => tema(&data.close, period),
        MovingAverageType::TMA => tma(&data.close, period),
        MovingAverageType::VWMA => vwma(&data.close, &data.volume, period),
        MovingAverageType::WMA => wma(&data.close, period),
        MovingAverageType::ZLEMA => zlema(&data.close, period),
        MovingAverageType::ZLSMA => zlsma(&data.close, period),
    }
}
