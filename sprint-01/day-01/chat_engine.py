import json
from dataclasses import asdict, dataclass
from typing import Literal


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str

    def __post_init__(self) -> None:
        valid_roles = {"system", "user", "assistant"}

        if self.role not in valid_roles:
            raise ValueError(f"Unsupported role: {self.role}")

        if not isinstance(self.content, str):
            raise TypeError("Message content must be a string")

        if not self.content.strip():
            raise ValueError("Message content cannot be empty")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


class Conversation:
    def __init__(
        self,
        system_prompt: str,
        max_message_length: int = 4000,
    ) -> None:
        if max_message_length <= 0:
            raise ValueError("max_message_length must be positive")

        self._max_message_length = max_message_length
        self._messages: list[Message] = [
            Message(role="system", content=system_prompt)
        ]

    def _add_message(self, role: Role, content: str) -> None:
        message = Message(role=role, content=content)

        if len(message.content) > self._max_message_length:
            raise ValueError(
                f"Message exceeds {self._max_message_length} characters"
            )

        previous_role = self._messages[-1].role

        if role == "assistant" and previous_role != "user":
            raise ValueError(
                "An assistant message must follow a user message"
            )

        if role == "user" and previous_role == "user":
            raise ValueError(
                "A user message cannot follow another user message"
            )

        self._messages.append(message)

    def add_user_message(self, content: str) -> None:
        self._add_message(role="user", content=content)

    def add_assistant_message(self, content: str) -> None:
        self._add_message(role="assistant", content=content)


    def get_messages(self) -> list[dict[str, str]]:
        return [message.to_dict() for message in self._messages]

    def export_json(self, file_path: str) -> None:
        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")

        if not file_path.strip():
            raise ValueError("file_path cannot be empty")

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.get_messages(),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def clear(self) -> None:
        self._messages = [self._messages[0]]


def main() -> None:
    conversation = Conversation(
        system_prompt="You are a concise Python tutor."
    )

    conversation.add_user_message(
        "What is the difference between an LLM and a chatbot?"
    )

    conversation.add_assistant_message(
        "An LLM generates output. A chatbot is an application "
        "that manages the model, prompts, state, safety, and interface."
    )

    conversation.add_user_message(
        "Who owns the conversation history?"
    )

    for message in conversation.get_messages():
        role = message["role"].upper()
        content = message["content"]
        print(f"{role}: {content}")

    conversation.export_json("conversation.json")
    print("Conversation exported to conversation.json")


if __name__ == "__main__":
    main()