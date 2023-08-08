use core::series::Series;

pub fn bullish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(3).lt(&open.shift(3))
        & high.shift(2).eq(&high.shift(1))
        & low.shift(2).eq(&low.shift(1))
        & close
            .shift(1)
            .max(&open.shift(1))
            .eq(&close.shift(2).max(&open.shift(2)))
        & close
            .shift(1)
            .min(&open.shift(1))
            .eq(&close.shift(2).min(&open.shift(2)))
}

pub fn bearish(open: &[f64], high: &[f64], low: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    close.shift(3).gt(&open.shift(3))
        & high.shift(2).eq(&high.shift(1))
        & low.shift(2).eq(&low.shift(1))
        & close
            .shift(1)
            .max(&open.shift(1))
            .eq(&close.shift(2).max(&open.shift(2)))
        & close
            .shift(1)
            .min(&open.shift(1))
            .eq(&close.shift(2).min(&open.shift(2)))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_doppelganger_bullish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let low = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let close = vec![4.5, 3.5, 4.5, 3.5, 4.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_doppelganger_bearish() {
        let open = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let high = vec![4.0, 3.0, 4.0, 3.0, 4.0];
        let low = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let close = vec![3.5, 2.5, 3.5, 2.5, 3.5];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &high, &low, &close).into();

        assert_eq!(result, expected);
    }
}