import json
import tempfile
import unittest
from pathlib import Path

from chat_engine import Conversation, Message


class TestMessage(unittest.TestCase):
    def test_empty_message_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Message(role="user", content="   ")

    def test_message_converts_to_dictionary(self) -> None:
        message = Message(role="user", content="Hello")

        self.assertEqual(
            message.to_dict(),
            {"role": "user", "content": "Hello"},
        )


class TestConversation(unittest.TestCase):
    def test_first_message_is_system_message(self) -> None:
        conversation = Conversation("You are helpful.")

        messages = conversation.get_messages()

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "system")

    def test_valid_sequence_is_accepted(self) -> None:
        conversation = Conversation("You are helpful.")

        conversation.add_user_message("Hello")
        conversation.add_assistant_message("Hi")
        conversation.add_user_message("Explain RAG")

        roles = [
            message["role"]
            for message in conversation.get_messages()
        ]

        self.assertEqual(
            roles,
            ["system", "user", "assistant", "user"],
        )

    def test_assistant_cannot_be_first(self) -> None:
        conversation = Conversation("You are helpful.")

        with self.assertRaises(ValueError):
            conversation.add_assistant_message("Hello")

    def test_consecutive_user_messages_are_rejected(self) -> None:
        conversation = Conversation("You are helpful.")
        conversation.add_user_message("First")

        with self.assertRaises(ValueError):
            conversation.add_user_message("Second")

    def test_consecutive_assistant_messages_are_rejected(self) -> None:
        conversation = Conversation("You are helpful.")
        conversation.add_user_message("Hello")
        conversation.add_assistant_message("Hi")

        with self.assertRaises(ValueError):
            conversation.add_assistant_message("Another reply")

    def test_failed_addition_does_not_change_history(self) -> None:
        conversation = Conversation("You are helpful.")
        before = conversation.get_messages()

        with self.assertRaises(ValueError):
            conversation.add_assistant_message("Invalid")

        after = conversation.get_messages()

        self.assertEqual(before, after)

    def test_clear_preserves_system_message(self) -> None:
        conversation = Conversation("You are helpful.")
        conversation.add_user_message("Hello")
        conversation.add_assistant_message("Hi")

        conversation.clear()

        messages = conversation.get_messages()

        self.assertEqual(
            messages,
            [
                {
                    "role": "system",
                    "content": "You are helpful.",
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()