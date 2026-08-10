import unittest

from model_config import GenerationConfig


class TestGenerationConfig(unittest.TestCase):
    def test_zero_temperature_is_deterministic(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=0.0,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "deterministic",
        )

    def test_point_three_is_deterministic(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=0.3,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "deterministic",
        )

    def test_above_point_three_is_balanced(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=0.31,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "balanced",
        )

    def test_point_seven_is_balanced(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=0.7,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "balanced",
        )

    def test_above_point_seven_is_creative(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=0.71,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "creative",
        )

    def test_two_is_creative(self) -> None:
        config = GenerationConfig(
            model="test-model",
            temperature=2.0,
        )

        self.assertEqual(
            config.recommended_use_case(),
            "creative",
        )

    def test_temperature_above_two_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            GenerationConfig(
                model="test-model",
                temperature=2.01,
            )


if __name__ == "__main__":
    unittest.main()