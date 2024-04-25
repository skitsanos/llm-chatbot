import os

import panel as pn
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import Choice
from panel.chat import ChatInterface

from chat_utils.core import get_timestamp, get_models
from chat_utils.fs import prepare_folders, save_jsonl

# https://panel.holoviz.org/
pn.extension()

prepare_folders(["chats"])

AVATAR_USER = "https://api.iconify.design/carbon:user.svg"
AVATAR_BOT = "https://api.iconify.design/carbon:chat-bot.svg"
AVATAR_SYSTEM = "https://api.iconify.design/carbon:ibm-event-automation.svg"

chat_memory = []
chat_memory_file = f"chats/chat_memory_{get_timestamp()}.jsonl"

sidebar_selector = pn.widgets.Select(
    name="Model",
    description="Select the model to use",
    options=get_models()
)

sidebar_keep_memory = pn.widgets.Checkbox(
    name="Keep memory on model switch",
    value=True,
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = "llama3-8b-8192"


def model_selected(event):
    if not sidebar_keep_memory.value:
        global chat_memory
        chat_memory = []

    selected_model = sidebar_selector.value

    chat_interface.send(
        f"""
        Model changed to `{selected_model['model']}`. This model has \
        `{selected_model['context_window']}` tokens context window.
        """,
        avatar=AVATAR_SYSTEM,
        user='System',
        respond=False
    )
    if selected_model["provider"] == "groq":
        client.base_url = selected_model["base_url"]
        client.api_key = os.getenv("GROQ_API_KEY")

    if selected_model["provider"] == "openai":
        client.base_url = selected_model["base_url"]
        client.api_key = os.getenv("OPENAI_API_KEY")


sidebar_selector.param.watch(model_selected, "value")


def get_response(user_input: str, user, instance: ChatInterface):
    chat_memory.append({"role": "user", "content": user_input})

    response: Stream[ChatCompletionChunk] = client.chat.completions.create(
        model=sidebar_selector.value["model"],
        messages=chat_memory,
        stream=True
    )

    replies = ""

    try:
        for chunk in response:
            if chunk.choices:
                choice: Choice = chunk.choices[0]
                text = choice.delta.content
                if text:
                    replies += text
                yield {
                    "avatar": AVATAR_BOT,
                    "user": "Assistant",
                    "object": replies
                }
            if 'end' in chunk and chunk.end:
                break  # Exit the loop if the stream is marked as ended
    finally:
        # Append the collected replies as a single entry to the chat history
        if replies:  # Ensure we do not add empty responses
            chat_memory.append({"role": "assistant", "content": replies})
        response.close()  # Ensure the stream is properly closed after processing
        save_jsonl(chat_memory_file, chat_memory)


chat_interface = ChatInterface(
    scroll=True,
    user="You",
    avatar=AVATAR_USER,
    callback=get_response,
    callback_user="Assistant",
    show_clear=False,
    show_undo=False,
    show_rerun=False,
)

ui = pn.template.FastListTemplate(
    site="Demo App",
    title=f"Chat",
    header_background="black",
    sidebar=[
        sidebar_selector,
        sidebar_keep_memory
    ],
    main=[chat_interface]
)

if __name__ == "__main__":
    chat_interface.show()
else:
    chat_interface.send("Hello, how can I help you?", user='Assistant', respond=False)
    ui.servable()
