use core::series::Series;

pub fn bullish(open: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (open - &close).abs();

    close.gt(&close.shift(1))
        & close.shift(1).gt(&close.shift(2))
        & close.shift(2).gt(&close.shift(3))
        & body.gte(&body.highest(5))
        & body.shift(1).gte(&body.shift(1).highest(5))
        & body.shift(2).gte(&body.shift(2).highest(5))
}

pub fn bearish(open: &[f64], close: &[f64]) -> Series<bool> {
    let open = Series::from(open);
    let close = Series::from(close);

    let body = (open - &close).abs();

    close.lt(&close.shift(1))
        & close.shift(1).lt(&close.shift(2))
        & close.shift(2).lt(&close.shift(3))
        & body.gte(&body.highest(5))
        & body.shift(1).gte(&body.shift(1).highest(5))
        & body.shift(2).gte(&body.shift(2).highest(5))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_three_candles_bullish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bullish(&open, &close).into();

        assert_eq!(result, expected);
    }

    #[test]
    fn test_three_candles_bearish() {
        let open = vec![4.0, 4.0, 4.0, 4.0, 4.0];
        let close = vec![2.0, 2.5, 2.0, 1.5, 2.0];
        let expected = vec![false, false, false, false, false];

        let result: Vec<bool> = bearish(&open, &close).into();

        assert_eq!(result, expected);
    }
}
