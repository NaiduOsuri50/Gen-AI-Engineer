from dataclasses import asdict, dataclass, field


@dataclass
class GenerationConfig:
    model: str
    temperature: float = 1.0
    top_p: float = 1.0
    max_output_tokens: int = 2048
    stop_sequences: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.model, str):
            raise TypeError("model must be a string")

        if not self.model.strip():
            raise ValueError("model cannot be empty")

        if not isinstance(self.temperature, (int, float)):
            raise TypeError("temperature must be a number")

        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError(
                "temperature must be between 0.0 and 2.0"
            )

        if not isinstance(self.top_p, (int, float)):
            raise TypeError("top_p must be a number")

        if not 0.0 < self.top_p <= 1.0:
            raise ValueError(
                "top_p must be greater than 0.0 and at most 1.0"
            )

        if not isinstance(self.max_output_tokens, int):
            raise TypeError(
                "max_output_tokens must be an integer"
            )

        if self.max_output_tokens <= 0:
            raise ValueError(
                "max_output_tokens must be positive"
            )

        if not isinstance(self.stop_sequences, tuple):
            raise TypeError(
                "stop_sequences must be a tuple"
            )

        for sequence in self.stop_sequences:
            if not isinstance(sequence, str):
                raise TypeError(
                    "each stop sequence must be a string"
                )

            if not sequence:
                raise ValueError(
                    "stop sequences cannot be empty"
                )

    def to_dict(self) -> dict:
        config = asdict(self)
        config["stop_sequences"] = list(
            self.stop_sequences
        )
        return config

    def recommended_use_case(self) -> str:
        if self.temperature <= 0.3:
            return "deterministic"

        if self.temperature <= 0.7:
            return "balanced"

        return "creative"


if __name__ == "__main__":
    config = GenerationConfig(
        model="gpt-4o",
        temperature=0.9,
        top_p=0.9,
        max_output_tokens=1000,
        stop_sequences=("\n", "END"),
    )

    print(config.to_dict())
    print(config.recommended_use_case())