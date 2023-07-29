use core::series::Series;

pub fn mfi(hlc3: &[f64], volume: &[f64], period: usize) -> Vec<f64> {
    let hlc3 = Series::from(hlc3);
    let volume = Series::from(volume);

    let changes = hlc3.change(1);

    let volume_hlc3 = volume * hlc3;

    let positive_volume = changes.gt(0.0) * &volume_hlc3;
    let negative_volume = changes.lt(0.0) * &volume_hlc3;

    let upper = positive_volume.sum(period);
    let lower = negative_volume.sum(period);

    let money_ratio = upper / lower;

    let mfi = 100.0 - 100.0 / (1.0 + money_ratio);

    mfi.nz(Some(50.0)).into()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mfi() {
        let hlc3 = vec![2.0, 2.1666, 2.0, 1.8333, 2.0];
        let volume = vec![1.0, 1.0, 1.0, 1.0, 1.0];
        let period = 3;
        let epsilon = 0.001;

        let expected = vec![50.0, 100.0, 51.9992, 36.1106, 34.2859];

        let result = mfi(&hlc3, &volume, period);

        for i in 0..hlc3.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            )
        }
    }
}