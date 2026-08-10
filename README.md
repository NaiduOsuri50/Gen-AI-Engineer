# Gen-AI-Engineer
Complete AI course Sprint 1 to 7 
Sprint 1: Building ChatGPT-Style Applications
Outcomes

By the end of Sprint 1, you will be able to:

Build advanced conversational applications using multiple LLM providers.
Apply structured prompting techniques using JSON and XML.
Implement conversation history, system instructions, validation, and error handling.
Access hosted and open-source models through provider APIs.
Run local models using Ollama and LM Studio.
Build chatbot interfaces using Gradio.
Design safe, configurable interfaces for developers and end users.
Compare models based on quality, latency, context window, privacy, and cost.
Tools and Platforms
OpenAI
Grok
OpenRouter
Hugging Face
Ollama
LM Studio
Gradio
Sprint 2: Automation with AI
Outcomes

By the end of Sprint 2, you will be able to:

Build automated job-search workflows using n8n nodes, triggers, and webhooks.
Generate personalized resumes and cover letters with LLMs.
Integrate the HeyGen API to create AI-based video resumes.
Build prototypes using Bolt and Lovable.
Distinguish deterministic AI workflows from autonomous AI agents.
Add retries, validation, logging, fallbacks, and error handling to workflows.
Optimize workflow reliability, execution time, and API cost.
Tools and Platforms
n8n
HeyGen
Bolt
Lovable
Sprint 3: Customizing AI and Building RAG Systems
Outcomes

By the end of Sprint 3, you will be able to:

Build Retrieval-Augmented Generation applications using LlamaIndex.
Ingest, clean, chunk, embed, store, and retrieve external data.
Customize AI applications using documents, images, audio, and personal data.
Understand embeddings, similarity search, reranking, and retrieval quality.
Integrate external services such as Google and YouTube APIs.
Evaluate RAG systems for faithfulness, relevance, and answer correctness.
Build Atlas, a personal “Second Brain” that organizes and recalls information.
Tools and Platforms
LlamaIndex
LanceDB
Gradio
Embedding models
Vector databases
Sprint 4: Open-Source Multimodal AI and Cost Engineering
Outcomes

By the end of Sprint 4, you will be able to:

Build applications that process and generate text, images, and audio.
Use Hugging Face pipelines and Diffusers.
Integrate Gemini and Anthropic models.
Select models based on capability, latency, privacy, and cost.
Use Langfuse to trace and observe LLM applications.
Measure token consumption, latency, error rates, and cost per request.
Estimate production costs under different traffic patterns.
Implement caching, routing, batching, and model fallback strategies.
Tools and Platforms
Hugging Face
Diffusers
Gemini
Anthropic
Langfuse
Sprint 5: Autonomous AI Agents and MCP
Outcomes

By the end of Sprint 5, you will be able to:

Build AI agents that use tools, APIs, databases, and code execution.
Understand the agent reasoning and action loop.
Define tools with schemas, validation, permissions, and error handling.
Apply the Model Context Protocol to connect models with external capabilities.
Build and monitor agent workflows using LangChain and LangSmith.
Execute agent tasks on local machines, servers, and cloud environments.
Apply safeguards against uncontrolled loops and unsafe tool execution.
Tools and Platforms
Claude
Cursor
LangChain
LangSmith
Model Context Protocol
LlamaIndex agents
Server and cloud execution environments
Sprint 6: Intelligent Multi-Agent AI Systems
Outcomes

By the end of Sprint 6, you will be able to:

Design multi-agent systems in which specialized agents collaborate on complex tasks.
Assign clear roles, responsibilities, tools, memory, and permissions to each agent.
Implement supervisor, router, hierarchical, sequential, and peer-to-peer orchestration patterns.
Build communication protocols for task delegation, result sharing, and conflict resolution.
Manage shared state and prevent context duplication between agents.
Add termination conditions, execution budgets, timeouts, and retry policies.
Detect and prevent circular conversations and uncontrolled agent loops.
Evaluate whether a problem genuinely requires multiple agents.
Compare multi-agent architectures with simpler workflows and single-agent systems.
Trace agent decisions, tool calls, messages, latency, and token consumption.
Build a multi-agent engineering team that can plan, implement, review, test, and revise a software feature.
Practical Project

Build an AI Software Delivery Squad consisting of:

Product Analyst Agent
 Converts a user request into requirements and acceptance criteria.

Solution Architect Agent
 Creates the technical design and assigns implementation tasks.

Developer Agent
 Produces the initial implementation.

Code Reviewer Agent
 identifies bugs, security issues, and inefficient logic.

Test Engineer Agent
 Generates and executes test cases.

Supervisor Agent
 Controls delegation, budgets, retries, and final delivery.

Tools and Platforms
LangGraph
AutoGen
CrewAI
OpenAI Swarm-style orchestration patterns
LangSmith
Langfuse
MCP
Python and TypeScript
Engineering Principle

A multi-agent system is not automatically better than a single agent.

You will use multiple agents only when the problem benefits from:

Role specialization
Parallel execution
Independent verification
Separation of permissions
Iterative review
Distributed tool access

If one deterministic workflow can solve the problem reliably, building six agents is architectural waste.

Sprint 7: Production Capstone and Hackathon
Outcomes

By the end of Sprint 7, you will be able to:

Design and build an original AI-powered product.
Apply prompting, RAG, agents, automation, multimodal AI, and observability.
Create a production-quality architecture.
Test functionality, safety, retrieval quality, latency, and cost.
Deploy the system to a server or cloud platform.
Prepare technical documentation and an architecture diagram.
Demonstrate the product through a polished presentation.
Publish a portfolio-ready repository and case study.

At this stage, you will no longer be reproducing tutorials. You will be building and defending your own engineering decisions.

Sprint 1, Day 1: LLM Applications Are Stateful Systems Around Stateless Models
Today’s Objective

By the end of this 90-minute session, you will be able to:

Explain the difference between an LLM and an LLM application.
Represent chat messages using a provider-neutral schema.
manage conversation state outside the model.
Construct a deterministic prompt payload.
Validate basic input before sending it to an LLM.
Implement a minimal conversation engine in Python.
Today’s Single Core Concept

The LLM does not own the conversation. Your application does.

An LLM API normally receives a list of messages and generates a response. On the next request, your application must send the relevant conversation history again.

Therefore:

Plain Text
1
Chat application
2
|
3
| Constructs messages
4
| Manages history
5
| Applies system instructions
6
| Validates input
7
| Selects provider and model
8
v
9
LLM provider
10
|
11
| Generates the next response
12
v
13
Chat application stores the result
Show more lines

If you fail to separate these responsibilities, you will produce fragile chatbot code that cannot be tested, extended, or migrated between providers.

Exact 90-Minute Schedule
Part 1: Theory, 45 Minutes
0 to 10 minutes: LLM versus LLM application

An LLM is responsible for generation.

The surrounding application is responsible for:

Authentication
User interface
Conversation history
Prompt construction
Provider selection
Validation
Output parsing
Retries
Logging
Security and safety
Cost tracking

A common beginner mistake looks like this:

Python
1
prompt = input("Ask: ")
2
response = call_model(prompt)
3
print(response)
Show more lines

This is a model call, not a conversational application.

It has:

No role separation
No conversation state
No input validation
No provider abstraction
No testable data model
No error handling
10 to 20 minutes: Message roles

A provider-neutral chat message can be represented as:

JSON
1
{
2
"role": "user",
3
"content": "Explain dependency injection."
4
}
Show more lines

The three roles we will use today are:

system: Defines application-level behavior and constraints.
user: Contains the user’s request.
assistant: Contains a previous model response.

Example:

Python
1
messages = [
2
{
3
"role": "system",
4
"content": "You are a concise Python tutor."
5
},
6
{
7
"role": "user",
8
"content": "What is a decorator?"
9
},
10
{
11
"role": "assistant",
12
"content": "A decorator wraps a callable to extend its behavior."
13
},
14
{
15
"role": "user",
16
"content": "Show a small example."
17
}
18
]
Show more lines

The model receives this context. It does not retrieve earlier turns magically.

20 to 30 minutes: State ownership

We will keep chat state in a Python object.

The state must enforce invariants:

The system message appears once.
Only supported roles are accepted.
Empty messages are rejected.
User and assistant messages are stored in order.
Internal state is not exposed for accidental mutation.

That fifth point matters.

This is inefficient and unsafe:

Python
1
def get_messages(self):
2
return self.messages
Show more lines

The caller could mutate internal state:

Python
1
history = chat.get_messages()
2
history.clear()
Show more lines

A safer method returns a copy.

30 to 38 minutes: Provider boundaries

Your conversation engine should not know whether the eventual provider is:

OpenAI
OpenRouter
Grok
Ollama
LM Studio

Those are infrastructure decisions.

Today, the engine will produce a provider-neutral list of messages. In a later lesson, adapters will translate that representation into provider-specific requests.

A clean architecture will eventually look like:

Plain Text
1
User interface
2
|
3
Conversation engine
4
|
5
Provider interface
6
|
7
+-----+------+--------+----------+
8
| OpenAI | Ollama | LM Studio |
9
+-----------+--------+-----------+
Show more lines

Do not put conversation memory, HTTP requests, and UI code into one function. That creates tightly coupled code and makes testing painful.

38 to 45 minutes: Failure cases

Before coding, identify what can go wrong:

Empty input
Whitespace-only input
Unsupported role
Extremely large input
Mutable state escaping the class
Assistant reply saved before a user message
Provider failure
Invalid structured output
Conversation history exceeding the context window

Today, you will handle the first five. Later lessons will handle provider and context-window failures.

Part 2: Hands-On Coding, 45 Minutes
Guided Implementation, 25 Minutes

Create a project directory:

Plain Text
1
genai-engineer/
2
└── sprint_01/
3
└── day_01/
4
├── chat_engine.py
5
└── test_chat_engine.py
Show more lines
Step 1: Define an immutable message

Create chat_engine.py:

Python
1
from dataclasses import dataclass, asdict
2
from typing import Literal
3
 
4
 
5
Role = Literal["system", "user", "assistant"]
6
 
7
 
8
@dataclass(frozen=True)
9
class Message:
10
role: Role
11
content: str
12
 
13
def __post_init__(self) -> None:
14
if self.role not in {"system", "user", "assistant"}:
15
raise ValueError(f"Unsupported role: {self.role}")
16
 
17
if not isinstance(self.content, str):
18
raise TypeError("Message content must be a string")
19
 
20
if not self.content.strip():
21
raise ValueError("Message content cannot be empty")
22
 
23
def to_dict(self) -> dict[str, str]:
24
return asdict(self)
Show more lines

Why frozen=True?

Because a message already stored in conversation history should not be silently modified.

Step 2: Build the conversation engine

Continue in chat_engine.py:

Python
1
class Conversation:
2
def __init__(
3
self,
4
system_prompt: str,
5
max_message_length: int = 4000,
6
) -> None:
7
if max_message_length <= 0:
8
raise ValueError("max_message_length must be positive")
9
 
10
self._max_message_length = max_message_length
11
self._messages: list[Message] = [
12
Message(role="system", content=system_prompt)
13
]
14
 
15
def _validate_length(self, content: str) -> None:
16
if len(content) > self._max_message_length:
17
raise ValueError(
18
f"Message exceeds the limit of "
19
f"{self._max_message_length} characters"
20
)
21
 
22
def add_user_message(self, content: str) -> None:
23
self._validate_length(content)
24
self._messages.append(
25
Message(role="user", content=content)
26
)
27
 
28
def add_assistant_message(self, content: str) -> None:
29
self._validate_length(content)
30
self._messages.append(
31
Message(role="assistant", content=content)
32
)
33
 
34
def get_messages(self) -> list[dict[str, str]]:
35
return [message.to_dict() for message in self._messages]
36
 
37
def clear(self) -> None:
38
system_message = self._messages[0]
39
self._messages = [system_message]
Show more lines
Step 3: Exercise the engine

Add this at the bottom of the file:

Python
1
def main() -> None:
2
conversation = Conversation(
3
system_prompt=(
4
"You are a precise GenAI engineering mentor. "
5
"Explain concepts using concise examples."
6
)
7
)
8
 
9
conversation.add_user_message(
10
"What is the difference between an LLM and a chatbot?"
11
)
12
 
13
conversation.add_assistant_message(
14
"An LLM generates text. A chatbot is an application "
15
"that manages prompts, history, interfaces, and model calls."
16
)
17
 
18
conversation.add_user_message(
19
"Why must the application manage history?"
20
)
21
 
22
for message in conversation.get_messages():
23
print(f"{message['role'].upper()}: {message['content']}")
24
 
25
 
26
if __name__ == "__main__":
27
main()
Show more lines

Expected structure:

Plain Text
1
SYSTEM: You are a precise GenAI engineering mentor...
2
USER: What is the difference between an LLM and a chatbot?
3
ASSISTANT: An LLM generates text...
4
USER: Why must the application manage history?
Show more lines

We are deliberately not calling a real model today. First, we make the state engine correct and testable. Provider integration comes after the boundary is clean.

Step 4: Write baseline tests

Create test_chat_engine.py:

Python
1
import unittest
2
 
3
from chat_engine import Conversation, Message
4
 
5
 
6
class TestMessage(unittest.TestCase):
7
def test_empty_content_is_rejected(self) -> None:
8
with self.assertRaises(ValueError):
9
Message(role="user", content=" ")
10
 
11
def test_message_is_converted_to_dictionary(self) -> None:
12
message = Message(role="user", content="Hello")
13
 
14
self.assertEqual(
15
message.to_dict(),
16
{
17
"role": "user",
18
"content": "Hello",
19
},
20
)
21
 
22
 
23
class TestConversation(unittest.TestCase):
24
def test_system_message_is_created(self) -> None:
25
conversation = Conversation("You are a tutor.")
26
 
27
messages = conversation.get_messages()
28
 
29
self.assertEqual(len(messages), 1)
30
self.assertEqual(messages[0]["role"], "system")
31
 
32
def test_user_message_is_added(self) -> None:
33
conversation = Conversation("You are a tutor.")
34
 
35
conversation.add_user_message("Explain embeddings.")
36
 
37
messages = conversation.get_messages()
38
 
39
self.assertEqual(len(messages), 2)
40
self.assertEqual(messages[1]["role"], "user")
41
 
42
def test_long_message_is_rejected(self) -> None:
43
conversation = Conversation(
44
"You are a tutor.",
45
max_message_length=5,
46
)
47
 
48
with self.assertRaises(ValueError):
49
conversation.add_user_message("123456")
50
 
51
def test_clear_preserves_system_message(self) -> None:
52
conversation = Conversation("You are a tutor.")
53
conversation.add_user_message("Hello")
54
conversation.add_assistant_message("Hi")
55
 
56
conversation.clear()
57
 
58
messages = conversation.get_messages()
59
 
60
self.assertEqual(len(messages), 1)
61
self.assertEqual(messages[0]["role"], "system")
62
 
63
 
64
if __name__ == "__main__":
65
unittest.main()
Show more lines

Run:

Shell
1
python -m unittest -v
Show more lines

All tests must pass.

Mandatory 20-Minute Mini-Challenge
Challenge: Enforce Valid Conversation Order

Your current implementation allows this invalid history:

Plain Text
1
SYSTEM
2
ASSISTANT
3
ASSISTANT
4
USER
Show more lines

That is bad application logic.

Modify Conversation so it enforces these rules:

The first non-system message must be from the user.
A user message cannot immediately follow another user message.
An assistant message cannot immediately follow another assistant message.
clear() must preserve the original system message.
Failed additions must not modify conversation history.
Existing public methods must continue working.
Required behavior
Python
1
conversation = Conversation("You are helpful.")
2
 
3
conversation.add_user_message("Hello")
4
conversation.add_assistant_message("Hi")
5
 
6
conversation.add_assistant_message("How can I help?")
7
# Must raise ValueError
Show more lines

This must also fail:

Python
1
conversation = Conversation("You are helpful.")
2
 
3
conversation.add_assistant_message("Hello")
4
# Must raise ValueError
Show more lines
Required Tests

Add tests for:

Assistant added before the first user message
Consecutive user messages
Consecutive assistant messages
Valid user-assistant-user sequence
History unchanged after a failed addition
New conversation sequence after clear()
Constraints

You may not:

Remove the Message class.
Expose _messages publicly.
duplicate sequence-validation logic in both public methods.
use external packages.
catch an exception without handling it.
modify internal history before completing validation.
Design hint

Create one private method that both public methods use:

Python
1
def _add_message(self, role: Role, content: str) -> None:
2
...
Show more lines

Do not blindly copy that hint. Decide what validations belong inside it and in what order they should run.

Submission Format

Submit all three items:

1. Your implementation
Python
1
# chat_engine.py
Show more lines
2. Your tests
Python
1
# test_chat_engine.py
Show more lines
3. Your engineering explanation

Answer these questions in your own words:

Why is conversation history application state rather than model state?
Why should validation happen before modifying _messages?
Why is duplicated validation logic dangerous?
What is one limitation of strict user-assistant alternation?
Grading Rubric

I will grade your submission out of 100:

Correctness: 35 points
Edge-case handling: 20 points
Test quality: 20 points
Code structure: 15 points
Engineering explanation: 10 points
Passing standard
85 or above: Proceed to Sprint 1, Day 2
70 to 84: Revise specific defects
Below 70: Rebuild the solution

Do not send screenshots. Send the actual code and test output. Your next move is implementation, not another tutorial.
