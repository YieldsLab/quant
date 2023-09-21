use core::series::Series;

pub fn tma(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    let sma = source.ma(period);
    let tma = sma.ma(period);

    tma
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, 1.25, 1.5, 2.1666667, 3.0];

        let result: Vec<f32> = tma(&source, 3).into();

        assert_eq!(result, expected);
    }
}