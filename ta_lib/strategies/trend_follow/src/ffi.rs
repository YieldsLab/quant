use crate::CrossMAStrategy;
use crate::TestingGroundStrategy;
use base::register_strategy;

#[no_mangle]
pub fn register_crossma(
    smothing: usize,
    short_period: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let ma = match smothing {
        1 => "ALMA",
        2 => "DEMA",
        3 => "EMA",
        4 => "FRAMA",
        5 => "GMA",
        6 => "HMA",
        7 => "KAMA",
        8 => "RMSMA",
        9 => "SINWMA",
        10 => "SMA",
        11 => "SMMA",
        12 => "T3",
        13 => "TEMA",
        14 => "TMA",
        15 => "VWMA",
        16 => "WMA",
        17 => "ZLEMA",
        _ => "SMA",
    };

    let strategy = CrossMAStrategy::new(ma, short_period, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}

#[no_mangle]
pub fn register_ground(
    smothing: usize,
    long_period: usize,
    atr_period: usize,
    stop_loss_multi: f32,
) -> i32 {
    let ma = match smothing {
        1 => "ALMA",
        2 => "DEMA",
        3 => "EMA",
        4 => "FRAMA",
        5 => "GMA",
        6 => "HMA",
        7 => "KAMA",
        8 => "RMSMA",
        9 => "SINWMA",
        10 => "SMA",
        11 => "SMMA",
        12 => "T3",
        13 => "TEMA",
        14 => "TMA",
        15 => "VWMA",
        16 => "WMA",
        17 => "ZLEMA",
        _ => "SMA",
    };

    let strategy = TestingGroundStrategy::new(ma, long_period, atr_period, stop_loss_multi);
    register_strategy(Box::new(strategy))
}
