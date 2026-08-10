import unittest

from structured_response import (
    CandidateEvaluationParser,
    ResponseValidationError,
)


class TestCandidateEvaluationParser(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = CandidateEvaluationParser()

    def test_valid_response_is_parsed(self) -> None:
        result = self.parser.parse(
            '{"score": 85, '
            '"decision": "interview", '
            '"feedback": "Strong candidate", '
            '"skills": ["Python", "SQL"]}'
        )

        self.assertEqual(result.score, 85)
        self.assertEqual(result.decision, "interview")
        self.assertEqual(result.feedback, "Strong candidate")
        self.assertEqual(result.skills, ("Python", "SQL"))

    def test_invalid_json_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse('{"score": 85,}')

    def test_missing_field_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"skills": ["Python"]}'
            )

    def test_unknown_field_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "Strong", '
                '"skills": ["Python"], '
                '"salary": 5000000}'
            )

    def test_score_below_zero_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": -1, '
                '"decision": "reject", '
                '"feedback": "Invalid score", '
                '"skills": ["Python"]}'
            )

    def test_score_above_100_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 101, '
                '"decision": "interview", '
                '"feedback": "Invalid score", '
                '"skills": ["Python"]}'
            )

    def test_boolean_score_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": true, '
                '"decision": "review", '
                '"feedback": "Invalid type", '
                '"skills": ["Python"]}'
            )

    def test_invalid_decision_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "hire", '
                '"feedback": "Unsupported decision", '
                '"skills": ["Python"]}'
            )

    def test_empty_feedback_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "   ", '
                '"skills": ["Python"]}'
            )

    def test_non_object_json_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse('["score", 85]')

    def test_decision_is_normalized(self) -> None:
        result = self.parser.parse(
            '{"score": 70, '
            '"decision": " REVIEW ", '
            '"feedback": "Needs another review", '
            '"skills": ["Python"]}'
        )

        self.assertEqual(result.decision, "review")

    # --- Skills Challenge Tests ---

    def test_valid_skills_list_is_accepted(self) -> None:
        result = self.parser.parse(
            '{"score": 85, '
            '"decision": "interview", '
            '"feedback": "Great skills", '
            '"skills": ["Python", "Docker", "Git"]}'
        )
        self.assertEqual(result.skills, ("Python", "Docker", "Git"))

    def test_empty_skills_list_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "No skills", '
                '"skills": []}'
            )

    def test_string_instead_of_list_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "String skills", '
                '"skills": "Python"}'
            )

    def test_empty_skill_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "Whitespace skill", '
                '"skills": ["Python", "   "]}'
            )

    def test_non_string_skill_is_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "Numeric skill", '
                '"skills": ["Python", 123]}'
            )

    def test_case_insensitive_duplicate_skills_are_rejected(self) -> None:
        with self.assertRaises(ResponseValidationError):
            self.parser.parse(
                '{"score": 85, '
                '"decision": "interview", '
                '"feedback": "Duplicate skills", '
                '"skills": ["Python", "python"]}'
            )

    def test_skills_are_stored_as_tuple(self) -> None:
        result = self.parser.parse(
            '{"score": 85, '
            '"decision": "interview", '
            '"feedback": "Tuple test", '
            '"skills": ["Python", "FastAPI"]}'
        )
        self.assertIsInstance(result.skills, tuple)


if __name__ == "__main__":
    unittest.main()