use core::prelude::*;
use criterion::{criterion_group, criterion_main, Criterion};
use momentum::*;
use price::prelude::*;
use volatility::atr;

fn momentum(c: &mut Criterion) {
    let mut group = c.benchmark_group("momentum");
    let open: Vec<f32> = vec![
        6.8430, 6.8660, 6.8635, 6.8610, 6.865, 6.8595, 6.8565, 6.852, 6.859, 6.86, 6.8580, 6.8605,
        6.8620, 6.867, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8350, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1520, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1330, 7.1225, 7.1180, 7.1250,
    ];

    let high: Vec<f32> = vec![
        6.8430, 6.8660, 6.8685, 6.8690, 6.865, 6.8595, 6.8565, 6.862, 6.859, 6.86, 6.8580, 6.8605,
        6.8620, 6.86, 6.859, 6.8670, 6.8640, 6.8575, 6.8485, 6.8450, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1230, 7.1225, 7.1180, 7.1250,
    ];

    let low: Vec<f32> = vec![
        6.8380, 6.8430, 6.8595, 6.8640, 6.8435, 6.8445, 6.8510, 6.8560, 6.8520, 6.8530, 6.8550,
        6.8550, 6.8565, 6.8475, 6.8480, 6.8535, 6.8565, 6.8455, 6.8445, 6.8365, 7.1195, 7.136,
        7.1405, 7.112, 7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495,
        7.1515, 7.1415, 7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135,
        7.1280, 7.1220, 7.1230, 7.1225, 7.1180, 7.1250,
    ];

    let close: Vec<f32> = vec![
        6.855, 6.858, 6.86, 6.8480, 6.8575, 6.864, 6.8565, 6.8455, 6.8450, 6.8365, 6.8310, 6.8355,
        6.8360, 6.8345, 6.8285, 6.8395, 7.1135, 7.088, 7.112, 7.1205, 7.1195, 7.136, 7.1405, 7.112,
        7.1095, 7.1220, 7.1310, 7.1550, 7.1480, 7.1435, 7.1405, 7.1440, 7.1495, 7.1515, 7.1415,
        7.1445, 7.1525, 7.1440, 7.1370, 7.1305, 7.1375, 7.1250, 7.1190, 7.1135, 7.1280, 7.1220,
        7.1230, 7.1225, 7.1180, 7.1250, 7.1230, 7.1130, 7.1210, 7.13, 7.134, 7.132, 7.116, 7.1235,
        7.1645, 7.1565,
    ];

    group.bench_function("ao", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let source = median_price(&high, &low);
                let short_period = 5;
                let long_period = 34;

                (source, short_period, long_period)
            },
            |(source, short_period, long_period)| ao(source, *short_period, *long_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("apo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let short_period = 10;
                let long_period = 20;
                (source, short_period, long_period)
            },
            |(source, short_period, long_period)| apo(source, *short_period, *long_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("bop", |b| {
        b.iter_batched_ref(
            || {
                let open = Series::from(&open);
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let smoothing_period = 14;
                (open, high, low, close, smoothing_period)
            },
            |(open, high, low, close, smoothing_period)| {
                bop(open, high, low, close, *smoothing_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let short_period = 20;
                let long_period = 15;
                let smoothing_period = 13;
                (source, short_period, long_period, smoothing_period)
            },
            |(source, short_period, long_period, smoothing_period)| {
                cc(source, *short_period, *long_period, *smoothing_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cci", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let hlc3 = typical_price(&high, &low, &close);
                let period = 14;
                let factor = 0.015;
                (hlc3, period, factor)
            },
            |(hlc3, period, factor)| cci(hlc3, *period, *factor),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cfo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                (source, period)
            },
            |(source, period)| cfo(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("cmo", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                (source, period)
            },
            |(source, period)| cmo(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("di", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                let smoothing = None;
                (source, period, smoothing)
            },
            |(source, period, smoothing)| di(source, *period, *smoothing),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("dmi", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let adx_period = 14;
                let di_period = 14;
                let atr = atr(&high, &low, &close, di_period, Some("SMMA"));
                (high, low, atr, adx_period, di_period)
            },
            |(high, low, atr, adx_period, di_period)| dmi(high, low, atr, *adx_period, *di_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("kst", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let roc_period_first = 10;
                let roc_period_second = 15;
                let roc_period_third = 20;
                let roc_period_fouth = 30;
                let period_first = 10;
                let period_second = 10;
                let period_third = 10;
                let period_fouth = 15;

                (
                    source,
                    roc_period_first,
                    roc_period_second,
                    roc_period_third,
                    roc_period_fouth,
                    period_first,
                    period_second,
                    period_third,
                    period_fouth,
                )
            },
            |(
                source,
                roc_period_first,
                roc_period_second,
                roc_period_third,
                roc_period_fouth,
                period_first,
                period_second,
                period_third,
                period_fouth,
            )| {
                kst(
                    source,
                    *roc_period_first,
                    *roc_period_second,
                    *roc_period_third,
                    *roc_period_fouth,
                    *period_first,
                    *period_second,
                    *period_third,
                    *period_fouth,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("macd", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let fast_period = 15;
                let slow_period = 26;
                let signal_period = 9;
                (source, fast_period, slow_period, signal_period)
            },
            |(source, fast_period, slow_period, signal_period)| {
                macd(source, *fast_period, *slow_period, *signal_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("roc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 9;
                (source, period)
            },
            |(source, period)| roc(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("rsi", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 14;
                (source, period)
            },
            |(source, period)| rsi(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("stc", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let fast_period = 23;
                let slow_period = 50;
                let cycle = 10;
                let d_first = 3;
                let d_second = 3;
                (source, fast_period, slow_period, cycle, d_first, d_second)
            },
            |(source, fast_period, slow_period, cycle, d_first, d_second)| {
                stc(
                    source,
                    *fast_period,
                    *slow_period,
                    *cycle,
                    *d_first,
                    *d_second,
                )
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("stochosc", |b| {
        b.iter_batched_ref(
            || {
                let high = Series::from(&high);
                let low = Series::from(&low);
                let close = Series::from(&close);
                let period = 14;
                let k_period = 5;
                let d_period = 5;
                (high, low, close, period, k_period, d_period)
            },
            |(high, low, close, period, k_period, d_period)| {
                stochosc(high, low, close, *period, *k_period, *d_period)
            },
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tii", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let major_period = 30;
                let minor_period = 10;
                (source, major_period, minor_period)
            },
            |(source, major_period, minor_period)| tii(source, *major_period, *minor_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("trix", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let period = 18;
                (source, period)
            },
            |(source, period)| trix(source, *period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.bench_function("tsi", |b| {
        b.iter_batched_ref(
            || {
                let source = Series::from(&close);
                let long_period = 25;
                let short_period = 13;
                (source, long_period, short_period)
            },
            |(source, long_period, short_period)| tsi(source, *long_period, *short_period),
            criterion::BatchSize::SmallInput,
        )
    });

    group.finish();
}

criterion_group!(indicators, momentum);
criterion_main!(indicators);