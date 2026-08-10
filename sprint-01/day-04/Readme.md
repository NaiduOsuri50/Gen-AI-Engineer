Cost: Free
 API required: No
 Deliverable: A validated JSON response-processing pipeline

 Today’s objective
By the end of Day 4, you will be able to:
1. Explain the difference between JSON text and valid application data.
2. Parse JSON safely.
3. Validate required fields and data types.
4. Reject unknown fields.
5. Validate allowed values and numerical ranges.
6. separate parsing errors from schema-validation errors.
7. Understand why “Return JSON” is not enough.

90-Minute Schedule
Theory: 45 minutes
0 to 10 minutes: JSON text versus Python objects
10 to 20 minutes: Parsing failures
20 to 30 minutes: Schema-validation failures
30 to 38 minutes: Required fields, types, enums, and ranges
38 to 45 minutes: Strict validation and downstream safety

Hands-on work: 45 minutes
45 to 55 minutes: Create the response model
55 to 70 minutes: Build the JSON parser
70 to 80 minutes: Run the program
80 to 90 minutes: Complete the challenge

Concept 1: JSON text is not trusted data

An LLM might return this text:

{"score": 85, "decision": "interview", "feedback": "Strong Python skills"}

The text looks correct, but your application must still verify:

1. Is it valid JSON?
2. Is score present?
3. Is score an integer?
4. Is score between 0 and 100?
5. Is decision one of the permitted values?
6. Is feedback a non-empty string?
7. Are unexpected fields present?

Master Architect rule:

Parsing proves that text is syntactically valid JSON.
Validation proves that the parsed data satisfies your application contract.

These are different operations.

Concept 2: Parsing failure

This is invalid JSON:

{"score": 85, "decision": "interview",}

The trailing comma causes JSON parsing to fail.

Python raises:
JSONDecodeError
Your application should translate provider-specific or library-specific exceptions into clear application errors.

Concept 3: Validation failure

This is syntactically valid JSON:

{"score": 500, "decision": "hire_immediately", "feedback": ""}

However, it violates the application rules:

Score exceeds 100.
Decision is unsupported.
Feedback is empty.

A JSON parser will accept it. Your validation layer must reject it.


Concept 4: Unknown fields

Consider this response:

{"score": 85, "decision": "interview", "feedback": "Strong", "salary": 5000000}

If salary is not part of the contract, reject it.

Silently accepting unknown fields can hide:

Model hallucinations
Schema-version mismatches
Prompt-injection effects
Misspelled fields
Unintended downstream behavior


Hands-On Project
Step 1: Create the Day 4 folder

Run this in PowerShell:

New-Item -ItemType Directory -Force "C:\Users\on255005\Gen-AI-Engineer\sprint-01\day-04"

Then run:
Set-Location "C:\Users\on255005\Gen-AI-Engineer\sprint-01\day-04"

Then run:
code .

Create two files:
structured_response.py
test_structured_response.py


Step 2: Create structured_response.py
Refer from structured_response.py

Expected result:
{'score': 85, 'decision': 'interview', 'feedback': 'Strong Python fundamentals.'}

Notice that INTERVIEW becomes lowercase interview. This is normalization.

Why the Boolean Check Matters:

Python treats Boolean values as a subtype of integers.

Without this explicit check:  if isinstance(self.score, bool):

the value true could accidentally pass an integer-type check.
That is a subtle validation defect. Professional validation must account for language behavior, not merely business requirements.

Step 4: Create test_structured_response.py
Refer test_structured_response.py

Expected final result:
Ran 11 tests in 0.003s
OK

Mandatory 20-Minute Challenge

Extend the response with a new field:
skills: tuple[str, ...]

A valid response should resemble:
{'score': 85, 'decision': 'interview', 'feedback': 'Strong Python fundamentals.', 'skills': ['Python', 'SQL']}

Requirements
1. skills must be required.
2. The JSON value must be a list.
3. Every skill must be a string.
4. Every skill must contain non-whitespace text.
5. At least one skill must be present.
6. Duplicate skills must be rejected case-insensitively.
7. The final dataclass must store skills as a tuple.
8. Unknown fields must still be rejected.

Required tests
Write tests proving that:

1. A valid skills list is accepted.
2. An empty skills list is rejected.
3. A string instead of a list is rejected.
4. An empty skill is rejected.
5. A non-string skill is rejected.
6. Python and python are treated as duplicates.
7. Skills are stored as a tuple.

Design warning:
Do not silently remove duplicates. Reject them.
Silent correction hides bad model output. Validation should expose contract violations.

Engineering Questions:
1. What is the difference between JSON parsing and schema validation?
Ans: JSON parsing only checks for valid syntax (e.g., matching braces, quotes, commas). Schema validation checks semantic correctness (e.g., checking that keys exist, values fall within correct numerical ranges, strings are non-empty, and data matches expected business rules).

2. Why should unknown fields be rejected?
Ans: Rejecting unknown fields prevents schema drift and hallucinated output from the LLM. It ensures that downstream applications receive strictly predictable data contracts and catches unexpected model behavior immediately during ingestion.

3. Why is a low temperature insufficient for reliable structured output?
Ans: Low temperature reduces token sampling variance, but it does not enforce structural grammar or application invariants. The model can still generate syntactically invalid JSON, omit required keys, or produce values out of range regardless of temperature setting.

4. Why do we translate JSONDecodeError into ResponseValidationError?
Ans: Translating low-level parsing errors into a unified domain exception isolates the rest of the application from implementation details. Callers only need to handle one exception type (ResponseValidationError) when processing LLM outputs.

5. Why should invalid LLM output be rejected before entering business logic?
Ans: LLM outputs are untrusted external inputs. Unvalidated output passed into core logic can lead to runtime crashes, database corruption, invalid state mutations, or security vulnerabilities. Strict validation acts as a boundary guard to preserve system reliability.

** Skills Validation Logic Highlight

# Skills validation snippet from CandidateEvaluation.__post_init__()
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
        raise ResponseValidationError("skill cannot be empty or whitespace")

    lower_skill = cleaned_skill.lower()
    if lower_skill in seen_lower:
        raise ResponseValidationError(
            f"duplicate skill detected: '{cleaned_skill}'"
        )

    seen_lower.add(lower_skill)
    normalized_skills.append(cleaned_skill)

object.__setattr__(self, "skills", tuple(normalized_skills))

** Valid and Invalid JSON Examples

    Valid JSON Example:
    {
  "score": 85,
  "decision": "INTERVIEW",
  "feedback": "Strong Python and backend fundamentals.",
  "skills": ["Python", "SQL", "Docker"]
}

Invalid JSON Example (Contains duplicate skills case-insensitively):
{
  "score": 85,
  "decision": "interview",
  "feedback": "Candidate profile",
  "skills": ["Python", "python"]
}