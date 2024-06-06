import json
import os
from datetime import datetime
from typing import Dict

import panel as pn
from llama_index.core.tools import FunctionTool
from panel.chat import ChatInterface

AVATAR_USER = "https://api.iconify.design/carbon:user.svg"
AVATAR_BOT = "https://api.iconify.design/carbon:chat-bot.svg"
AVATAR_SYSTEM = "https://api.iconify.design/carbon:ibm-event-automation.svg"


def get_models() -> dict:
    """
    Get a dictionary of models with their details
    :return:
    """
    return {
        "LLaMA3 8b":
            {
                "model": "llama3-8b-8192",
                "base_url": "https://api.groq.com/openai/v1",
                "provider": "groq",
                "context_window": 8192
            },
        "LLaMA3 70b":
            {
                "model": "llama3-70b-8192",
                "base_url": "https://api.groq.com/openai/v1",
                "provider": "groq",
                "context_window": 8192
            },
        "Mixtral 8x7b":
            {
                "model": "mixtral-8x7b-32768",
                "base_url": "https://api.groq.com/openai/v1",
                "provider": "groq",
                "context_window": 32768
            },
        "Gemma 7b":
            {
                "model": "gemma-7b-it",
                "base_url": "https://api.groq.com/openai/v1",
                "provider": "groq",
                "context_window": 8192
            },
        "GPT-4 Turbo":
            {
                "model": "gpt-4-turbo",
                "base_url": "https://api.openai.com/v1",
                "provider": "openai",
                "context_window": 128000
            },
        "GPT-4":
            {
                "model": "gpt-4",
                "base_url": "https://api.openai.com/v1",
                "provider": "openai",
                "context_window": 8192
            },
        "GPT-3.5 Turbo":
            {
                "model": "gpt-3.5-turbo",
                "base_url": "https://api.openai.com/v1",
                "provider": "openai",
                "context_window": 16385
            },
        "GPT-3.5 Turbo (Updated)":
            {
                "model": "gpt-3.5-turbo-0125",
                "base_url": "https://api.openai.com/v1",
                "provider": "openai",
                "context_window": 16385
            }
    }


def get_timestamp() -> str:
    """
    Get timestamp string in YYYY-MM-DD_HHMMSS format
    :return: timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def get_list_of_chats(
        path: str
) -> list[str]:
    """
    Get a list of chat files in the directory
    :param path:
    :return:
    """
    # check if the path exists
    if not os.path.exists(path):
        return []

    # check if the path is a directory
    if not os.path.isdir(path):
        return []

    # get the list of files in the directory, only with the jsonl extension
    files = [f for f in os.listdir(path) if f.endswith(".jsonl")]

    # return list of files without extensions and sorted by date, because they are stored
    # as chat_memory_2024-04-25_084851.jsonl
    return sorted([f.replace(".jsonl", "") for f in files])


def create_chat_button(
        label: str,
        list_of_chats,
        click_action
):
    button = pn.widgets.Button(
        name=label,
        button_type='light',
        button_style='solid',
        width_policy='max'
    )

    def wrapped_click_action(
            event
    ):
        for btn in list_of_chats.objects:
            btn.button_type = 'light'
        button.button_type = 'default'
        # Find the index of the clicked button
        index = list_of_chats.objects.index(button)
        # Move the clicked button to the top
        item = list_of_chats.pop(index)
        list_of_chats.insert(0, item)
        # Call the original click action
        click_action(event)

    button.on_click(wrapped_click_action)
    return button


def load_chat_from_file(
        chat_context: Dict,
        path: str,
        chat_instance: ChatInterface
) -> None:
    """
    Load chat from a file
    :param chat_context:
    :param chat_instance:
    :param path:
    :return:
    """
    chat_instance.clear()

    chat_context["chat_memory"] = []
    chat_context["chat_memory_file"] = path

    if not os.path.exists(path):
        chat_instance.send("Hello, how can I help you?",
                           user='Assistant',
                           avatar=AVATAR_BOT,
                           respond=False)
    else:
        with open(path, 'r') as f:
            for line in f:
                message = json.loads(line.strip())
                chat_context["chat_memory"].append(message)

                user = "You" if message["role"] == "user" else "Assistant"

                chat_instance.send(
                    value=message["content"],
                    user=user,
                    avatar=AVATAR_USER if message["role"] == "user" else AVATAR_BOT,
                    respond=False
                )

        chat_instance.send(
            value=f"_Loaded from file: {path}_",
            user=user,
            avatar=AVATAR_SYSTEM,
            respond=False
        )


def start_new_chat(
        chat_context: Dict,
        list_of_chats,
        chat_instance: ChatInterface
):
    """
    Start a new chat
    :return:
    """
    chat_instance.clear()

    chat_label = f"chat_memory_{get_timestamp()}"

    chat_context["chat_memory"] = []
    chat_context["chat_memory_file"] = f"chats/{chat_label}.jsonl"

    chat_instance.send("Hello, how can I help you?",
                       user='Assistant',
                       avatar=AVATAR_BOT,
                       respond=False)

    button = create_chat_button(
        label=chat_label,
        list_of_chats=list_of_chats,
        click_action=lambda
            event: load_chat_from_file(
            chat_context=chat_context,
            path=f"chats/{event.obj.name}.jsonl",
            chat_instance=chat_instance)
    )
    list_of_chats.insert(0, button)


def llamaindex_tool(
        func,
        description: str = None
):
    return FunctionTool.from_defaults(fn=func, description=description)
