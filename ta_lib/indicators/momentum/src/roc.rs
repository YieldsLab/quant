use core::series::Series;

pub fn roc(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let roc = 100.0 * (&source - &source.shift(period)) / source.shift(period);

    roc
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roc() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let expected = vec![0.0, 0.0, 0.0, 300.0, 150.0];

        let result: Vec<f32> = roc(&source, period).into();

        assert_eq!(result, expected);
    }
}
