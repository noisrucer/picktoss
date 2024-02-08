from reminder.core.llm.openai import ChatMessage


def load_prompt_messages(prompt_path: str) -> list[ChatMessage]:
    with open(prompt_path) as f:
        content = f.read().strip()

    parts = content.split("[%")
    messages = []

    for part in parts[1:]:
        split_part = part.split("%]", 1)
        if len(split_part) == 2:
            role, message_content = split_part
            role = role.strip()
            message_content = message_content.strip()
            messages.append(ChatMessage(role=role, content=message_content))

    return messages


def fill_message_placeholders(messages: list[ChatMessage], placeholders: dict[str, str]) -> list[ChatMessage]:
    messages = [ChatMessage(role=message.role, content=message.content) for message in messages]

    for message in messages:
        for placeholder_name, value in placeholders.items():
            if "{{$%s}}" % placeholder_name in message.content:
                message.content = message.content.replace("{{$%s}}" % placeholder_name, str(value))

    return messages
