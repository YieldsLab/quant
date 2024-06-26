use core::prelude::*;

pub fn sinwma(source: &Series<f32>, period: usize) -> Series<f32> {
    let weights = (0..period)
        .map(|i| ((i as f32 + 1.) * std::f32::consts::PI / (period as f32 + 1.)).sin())
        .collect::<Vec<_>>();

    source.wg(&weights)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sinwma() {
        let source = Series::from([
            0.01707, 0.01706, 0.01707, 0.01705, 0.01710, 0.01705, 0.01704, 0.01709,
        ]);
        let expected = [
            0.0,
            0.0,
            0.017065858,
            0.017061213,
            0.017070502,
            0.01707071,
            0.017061714,
            0.017057573,
        ];
        let epsilon = 0.0001;

        let result: Vec<f32> = sinwma(&source, 3).into();

        for i in 0..source.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            );
        }
    }
}
