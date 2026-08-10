Master Architect decision: Day 1 is accepted based on your working conversation engine, passing tests, and successful JSON export. We are moving forward.

I will use plain text formatting because code boxes are not rendering correctly for you.

SPRINT 1, DAY 2

Topic: Model Parameters and Controlled LLM Experiments

Duration: 90 minutes

Today’s objective:

By the end of Day 2, you will understand:

Temperature
Maximum output tokens
Top-p
Stop sequences
Reproducibility
Why model parameters must be application configuration
How to test model behavior systematically

You will not call a paid API today. You will build a provider-independent configuration system and a model simulator.

PART 1: THEORY

Time: 40 minutes

CORE CONCEPT

A prompt is only one part of an LLM request.

A complete request also includes generation parameters:

Prompt + Model + Parameters + Context = Generated response

Two requests with the same prompt can produce different answers because:

The model may be probabilistic.
Temperature may allow more or less variation.
Top-p may restrict token selection.
The output-token limit may truncate the response.
The provider may use a different model version.
Some providers may not guarantee deterministic output.

CONCEPT 1: TEMPERATURE

Temperature controls how much randomness is allowed during token selection.

Lower temperature:

0.0 to 0.3

Best suited for:

Data extraction
Classification
Code generation
JSON output
Factual question answering

Higher temperature:

0.7 to 1.2

Best suited for:

Brainstorming
Creative writing
Marketing ideas
Alternative product names
Generating diverse examples

Engineering warning:

Temperature does not improve intelligence.

A high temperature does not make the model smarter. It increases variation and can increase inconsistent or incorrect answers.

CONCEPT 2: MAXIMUM OUTPUT TOKENS

Maximum output tokens limit the number of tokens the model may generate.

This protects your application from:

Unexpectedly long responses
Higher API costs
Slow requests
Excessive output
Agent loops producing large responses

A token is not exactly one word.

Do not build token calculations using:

token count = number of words

That is inaccurate.

For today, we will treat the parameter as a configurable model limit. Later, we will use a tokenizer to measure actual token usage.

Engineering warning:

Maximum output tokens usually limit generated output, not the entire conversation context.

The total request may include:

System instructions
Conversation history
User input
Retrieved RAG context
Tool descriptions
Generated output

CONCEPT 3: TOP-P

Top-p is also called nucleus sampling.

The model considers a collection of likely next tokens whose combined probability reaches the configured top-p value.

A smaller top-p restricts the selection.

A larger top-p allows more possibilities.

Example interpretation:

top_p = 0.2

The model selects from a narrow set of highly likely tokens.

top_p = 1.0

The model does not apply a restrictive probability cutoff.

Engineering rule:

Do not aggressively tune temperature and top-p simultaneously during your first experiments.

Change one variable at a time. Otherwise, you cannot determine which parameter caused the observed behavior.

CONCEPT 4: STOP SEQUENCES

A stop sequence tells the generation process to stop when a particular string appears.

Possible stop sequences:

END

USER:

Stop sequences can help prevent the model from:

Continuing into another simulated role
Producing unnecessary sections
Generating beyond a required delimiter

Stop sequences are not a security boundary.

Do not rely on them to prevent sensitive output or prompt injection.

CONCEPT 5: REPRODUCIBILITY

Low temperature can make output more consistent, but it does not guarantee identical output across every provider and model.

Results may change because of:

Model updates
Provider infrastructure
Different sampling implementations
Hidden provider settings
Changes in system prompts
Conversation-history differences

A professional experiment must record:

Provider
Model
Prompt
System instruction
Temperature
Top-p
Maximum output tokens
Timestamp
Output
Latency

PART 2: HANDS-ON IMPLEMENTATION

Time: 30 minutes

STEP 1: CREATE A NEW FOLDER

Enter this command in PowerShell:

New-Item -ItemType Directory -Force "C:\Users\on255005\Gen-AI-Engineer\sprint-01\day-02"

Then enter:

Set-Location "C:\Users\on255005\Gen-AI-Engineer\sprint-01\day-02"

Then enter:

code .

Create these files in VS Code:

model_config.py

test_model_config.py

Important:

The Python content below belongs inside the VS Code files. Do not paste Python definitions directly into PowerShell.


Add a new method to ModelConfig:

recommended_use_case

It must return one of these values:

deterministic
balanced
creative

Rules:

If temperature is between 0.0 and 0.3 inclusive:

Return deterministic

If temperature is greater than 0.3 and less than or equal to 0.7:

Return balanced

If temperature is greater than 0.7:

Return creative

The method signature should be:

def recommended_use_case(self) -> str:

Add at least five tests:

Temperature 0.0 returns deterministic.
Temperature 0.3 returns deterministic.
Temperature 0.31 returns balanced.
Temperature 0.7 returns balanced.
Temperature 0.71 returns creative.

Do not duplicate the decision logic inside your tests.

Your tests should call the real method and verify its returned value.

SOCRATIC ENGINEERING QUESTIONS

Submit answers in your own words:

Why is temperature 0.9 unsuitable for strict JSON extraction?

Why should model parameters be stored in a configuration object rather than scattered throughout the application?

What is wrong with changing temperature and top-p simultaneously during an experiment?

Why does a maximum output-token setting not completely solve context-window problems?


Your smaller Day 2 challenge

Change only the temperature and run the program three times.

Experiment 1

Set:

temperature=0.1

Expected recommendation:

deterministic

Experiment 2

Set:

temperature=0.5

Expected recommendation:

balanced

Experiment 3

Set:

temperature=0.9

Expected recommendation:

creative

After each run, note the result.

Important observation

This method does not call an LLM. It classifies the configuration based on rules that we wrote.

The purpose is to learn:

Model parameters should be stored together.
Parameter values should be validated.
Application behavior should be testable without spending money.
Boundary values such as 0.3 and 0.7 require careful handling.
Submit this next

Send me:

The output when temperature is 0.1
The output when temperature is 0.5
The output when temperature is 0.9
The complete content of your current model_config.py



Why these test values matter

We are not testing random temperatures. We are testing boundaries:

0.0: lowest accepted value
0.3: final deterministic value
0.31: immediately inside balanced
0.7: final balanced value
0.71: immediately inside creative
2.0: highest accepted value
2.01: first invalid example above the limit

This is called boundary-value testing. Defects frequently occur at transitions such as < versus <=.

Remaining engineering questions

Answer briefly in your own words:

Q1.Why is temperature 0.9 unsuitable for strict JSON extraction?
Ans:High temperature increases sampling randomness (entropy), leading the model to select less probable tokens. For structured data like JSON, this frequently introduces syntax errors (unclosed quotes, trailing commas) or schema mismatches. Extraction requires deterministic, low-temperature settings (0.0 to 0.2) to ensure strict format adherence.

Q2.Why store generation parameters in one configuration object?
Ans:It encapsulates parameter validation at initialization (preventing runtime type/value errors downstream), simplifies function signatures across the codebase, ensures repeatable configurations, and allows clean serialization (to_dict()) for experiment logging and tracking.

Q3.Why should an experiment change only one model parameter at a time?
Ans:To isolate variables and establish clear causality. If you adjust multiple parameters simultaneously (e.g., lowering temperature while shrinking top_p), you cannot isolate which specific parameter caused a change in output quality, diversity, or length.

Q4.Why does max_output_tokens not solve the entire context-window problem?
Ans:max_output_tokens only caps the length of the generated response (completion). A model's context window encompasses both the input prompt and the output response combined. If an oversized prompt fills the context window, the model will fail or truncate context before max_output_tokens even comes into play.

Submit the test output and four answers. Then Day 2 is complete.
test_above_point_seven_is_creative (test_model_config.TestGenerationConfig.test_above_point_seven_is_creative) ... ok
test_above_point_three_is_balanced (test_model_config.TestGenerationConfig.test_above_point_three_is_balanced) ... ok
test_point_seven_is_balanced (test_model_config.TestGenerationConfig.test_point_seven_is_balanced) ... ok
test_point_three_is_deterministic (test_model_config.TestGenerationConfig.test_point_three_is_deterministic) ... ok
test_temperature_above_two_is_rejected (test_model_config.TestGenerationConfig.test_temperature_above_two_is_rejected) ... ok
test_two_is_creative (test_model_config.TestGenerationConfig.test_two_is_creative) ... ok
test_zero_temperature_is_deterministic (test_model_config.TestGenerationConfig.test_zero_temperature_is_deterministic) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.003s

OK