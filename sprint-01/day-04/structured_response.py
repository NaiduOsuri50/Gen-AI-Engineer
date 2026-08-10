import json
from dataclasses import asdict, dataclass
from typing import Any


class ResponseValidationError(ValueError):
    pass


@dataclass(frozen=True)
class CandidateEvaluation:
    score: int
    decision: str
    feedback: str
    skills: tuple[str, ...]

    ALLOWED_DECISIONS = {
        "reject",
        "review",
        "interview",
    }

    def __post_init__(self) -> None:
        # Score validation
        if isinstance(self.score, bool) or not isinstance(self.score, int):
            raise ResponseValidationError("score must be an integer")

        if not 0 <= self.score <= 100:
            raise ResponseValidationError("score must be between 0 and 100")

        # Decision validation
        if not isinstance(self.decision, str):
            raise ResponseValidationError("decision must be a string")

        normalized_decision = self.decision.strip().lower()

        if normalized_decision not in self.ALLOWED_DECISIONS:
            raise ResponseValidationError(
                "decision must be reject, review, or interview"
            )

        # Feedback validation
        if not isinstance(self.feedback, str):
            raise ResponseValidationError("feedback must be a string")

        if not self.feedback.strip():
            raise ResponseValidationError("feedback cannot be empty")

        # Skills validation
        if not isinstance(self.skills, (tuple, list)):
            raise ResponseValidationError("skills must be a list")

        if len(self.skills) == 0:
            raise ResponseValidationError("skills list cannot be empty")

        normalized_skills = []
        seen_lower = set()

        for skill in self.skills:
            if isinstance(skill, bool) or not isinstance(skill, str):
                raise ResponseValidationError("each skill must be a string")

            cleaned_skill = skill.strip()
            if not cleaned_skill:
                raise ResponseValidationError(
                    "skill cannot be empty or whitespace"
                )

            lower_skill = cleaned_skill.lower()
            if lower_skill in seen_lower:
                raise ResponseValidationError(
                    f"duplicate skill detected: '{cleaned_skill}'"
                )

            seen_lower.add(lower_skill)
            normalized_skills.append(cleaned_skill)

        # Immutably set normalized attributes
        object.__setattr__(self, "decision", normalized_decision)
        object.__setattr__(self, "feedback", self.feedback.strip())
        object.__setattr__(self, "skills", tuple(normalized_skills))

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["skills"] = list(self.skills)
        return data


class CandidateEvaluationParser:
    REQUIRED_FIELDS = {
        "score",
        "decision",
        "feedback",
        "skills",
    }

    def parse(self, response_text: str) -> CandidateEvaluation:
        if not isinstance(response_text, str):
            raise TypeError("response_text must be a string")

        if not response_text.strip():
            raise ResponseValidationError("response_text cannot be empty")

        try:
            data = json.loads(response_text)
        except json.JSONDecodeError as error:
            raise ResponseValidationError(
                f"invalid JSON: {error.msg}"
            ) from error

        if not isinstance(data, dict):
            raise ResponseValidationError("response must be a JSON object")

        if "skills" in data and not isinstance(data["skills"], list):
            raise ResponseValidationError("skills must be a list")

        received_fields = set(data.keys())

        missing_fields = self.REQUIRED_FIELDS - received_fields
        unknown_fields = received_fields - self.REQUIRED_FIELDS

        if missing_fields:
            names = ", ".join(sorted(missing_fields))
            raise ResponseValidationError(f"missing fields: {names}")

        if unknown_fields:
            names = ", ".join(sorted(unknown_fields))
            raise ResponseValidationError(f"unknown fields: {names}")

        return CandidateEvaluation(
            score=data["score"],
            decision=data["decision"],
            feedback=data["feedback"],
            skills=data["skills"],
        )


def main() -> None:
    response_text = (
        '{"score": 85, '
        '"decision": "INTERVIEW", '
        '"feedback": "Strong Python fundamentals.", '
        '"skills": ["Python", "SQL"]}'
    )

    parser = CandidateEvaluationParser()
    evaluation = parser.parse(response_text)

    print(evaluation.to_dict())


if __name__ == "__main__":
    main()