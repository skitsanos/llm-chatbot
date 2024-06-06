import json
import panel as pn
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import Choice
from panel.chat import ChatInterface

from chat_utils.core import get_timestamp
from chat_utils.fs import prepare_folders
from tools.datetime import today
from tools.mock import get_product_details, send_email, get_current_weather

# Mapping of tool names to functions
TOOLS = {
    'today': today,
    'get_product_details': get_product_details,
    "send_email": send_email,
    "get_current_weather": get_current_weather
}

# Setup the environment and prepare folders
pn.extension()
prepare_folders(["chats"])

chat_memory = []
chat_memory_file = f"chats/chat_memory_{get_timestamp()}.jsonl"

AVATAR_USER = "https://api.iconify.design/carbon:user.svg"
AVATAR_BOT = "https://api.iconify.design/carbon:chat-bot.svg"

client = OpenAI()

model = "gpt-4o"


def get_response(
        user_input: str,
        user,
        instance: ChatInterface
):
    chat_memory.append({
        "role": "user",
        "content": user_input
    })

    system_prompt = """
    You are an assistant that helps users by utilizing available tools whenever possible. 
    Before generating a response, always check if there is a relevant tool available that can 
    provide the necessary information.
    When a user asks for specific details (like product details), extract the necessary 
    information (such as product IDs) from the user's input and use the corresponding tool to get 
    the details.
    Only generate a response directly if no tool is available or applicable.
    """

    response: Stream[ChatCompletionChunk] = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *chat_memory],
        stream=True,
        # tool_choice="auto",
        tools=[TOOLS[tool_name].tool for tool_name in TOOLS.keys()]
    )

    replies = ""
    func_call = {
        "name": None,
        "arguments": "",
    }

    try:
        for chunk in response:
            if chunk.choices:
                choice: Choice = chunk.choices[0]

                if choice.delta.tool_calls:
                    for tool_call in choice.delta.tool_calls:
                        if tool_call.function.name:
                            func_call["name"] = tool_call.function.name
                        if tool_call.function.arguments:
                            func_call["arguments"] += tool_call.function.arguments

                if choice.finish_reason == "tool_calls":
                    if func_call["name"] and func_call["arguments"]:
                        function_name = func_call["name"]
                        function_args = json.loads(func_call["arguments"])
                        if function_name in TOOLS:
                            yield {
                                "avatar": AVATAR_BOT,
                                "user": "Assistant",
                                "object": "Hold a moment, I am processing your request..."
                            }
                            func = TOOLS[function_name]
                            output_data = func(**function_args)
                            print(output_data)
                            content = ""
                            # if output is object, convert to string
                            if isinstance(output_data, dict):
                                content = json.dumps(output_data)
                            # Inject the tool result back into the conversation
                            chat_memory.append({
                                "role": "function",
                                "name": function_name,
                                "content": output_data
                            })
                            response_tool = client.chat.completions.create(
                                model=model,
                                messages=[
                                    {
                                        "role": "system",
                                        "content": system_prompt
                                    },
                                    *chat_memory
                                ],
                                stream=True
                            )
                            for response_chunk in response_tool:
                                if response_chunk.choices:
                                    tool_choice: Choice = response_chunk.choices[0]
                                    if tool_choice.delta.content:
                                        replies += tool_choice.delta.content
                                        yield {
                                            "avatar": AVATAR_BOT,
                                            "user": "Assistant",
                                            "object": replies
                                        }
                                if 'end' in response_chunk and response_chunk.end:
                                    break  # Exit the loop if the stream is marked as ended

                if choice.delta.content:
                    replies += choice.delta.content
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
            chat_memory.append({
                "role": "assistant",
                "content": replies
            })
        response.close()  # Ensure the stream is properly closed after processing
        # save_jsonl(chat_memory_file, chat_memory)


chat_interface = ChatInterface(
    user="You",
    avatar=AVATAR_USER,
    callback=get_response,
    callback_user="Assistant",
    callback_exception='verbose',
    show_clear=False,
    show_undo=False,
    show_rerun=False,
)

ui = pn.template.FastListTemplate(
    site="Demo App",
    title=f"Chat",
    header_background="black",
    sidebar=[],
    main=[chat_interface]
)

if __name__ == "__main__":
    ui.show(open=False)
else:
    chat_interface.send(
        value=f"""
        Hello, I will be using `{model}` LLM. 
        You can ask me anything and I will do my best to assist you
        """,
        user='Assistant',
        avatar=AVATAR_BOT,
        respond=False
    )
    ui.servable()
