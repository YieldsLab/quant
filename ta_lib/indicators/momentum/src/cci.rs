use core::prelude::*;

pub fn cci(hlc3: &Series<f32>, period: usize, factor: f32) -> Series<f32> {
    (hlc3 - hlc3.ma(period)) / (factor * hlc3.md(period))
}

#[cfg(test)]
mod tests {
    use super::*;
    use price::prelude::*;

    #[test]
    fn test_cci() {
        let high = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let low = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let close = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let hlc3 = typical_price(&high, &low, &close);
        let expected = vec![0.0, 66.66667, 100.0, 100.0, 100.0];

        let result: Vec<f32> = cci(&hlc3, 3, 0.015).into();

        assert_eq!(result, expected);
    }
}
