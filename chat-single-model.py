import os

import panel as pn
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import Choice
from panel.chat import ChatInterface

from chat_utils.core import get_timestamp
from chat_utils.fs import prepare_folders

# https://panel.holoviz.org/
pn.extension()

prepare_folders(["chats"])

chat_memory = []
chat_memory_file = f"chats/chat_memory_{get_timestamp()}.jsonl"

AVATAR_USER = "https://api.iconify.design/carbon:user.svg"
AVATAR_BOT = "https://api.iconify.design/carbon:chat-bot.svg"

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

model = "llama3-8b-8192"


def get_response(user_input: str, user, instance: ChatInterface):
    chat_memory.append({"role": "user", "content": user_input})

    response: Stream[ChatCompletionChunk] = client.chat.completions.create(
        model=model,
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
                }  # Process the text as needed
            if 'end' in chunk and chunk.end:
                break  # Exit the loop if the stream is marked as ended
    finally:
        instance.scroll = True
        # Append the collected replies as a single entry to the chat history
        if replies:  # Ensure we do not add empty responses
            chat_memory.append({"role": "assistant", "content": replies})
        response.close()  # Ensure the stream is properly closed after processing
        #save_jsonl(chat_memory_file, chat_memory)


chat_interface = ChatInterface(
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
    ],
    main=[chat_interface]
)

if __name__ == "__main__":
    ui.show(open=False)
else:
    chat_interface.send(
        value=f"""
        Hello, i will be using `{model}` LLM. 
        You can ask me anything and i will do my best to assist you
        """,
        user='Assistant',
        avatar=AVATAR_BOT,
        respond=False)
    ui.servable()
