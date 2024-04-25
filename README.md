# llm-chatbot

> This repo is a collection of examples showcasing how to use HoloViz components and various LLMs to create a chat
> interface similar to the one you might be familiar with at ChatGPT

### Install dependencies

```bash
pip install -r requirements.txt
```

It will install the following packages:

- `openai` for OpenAI API
- `panel` for creating interactive dashboards and Chat UIs
- `watchfiles` for watching file changes and reloading the server

### Running with Taskfile

Taskfile is a simple way to manage tasks in a project. It is similar to Makefile but with a simpler syntax. Please refer
to https://taskfile.dev/installation/ for installation instructions.

Taskfile example for this project:

```yaml
version: 3

env:
  OPENAI_API_KEY: <YOUR_OPEN_AI_KEY>
  GROQ_API_KEY: <YOUR_GROQ_KEY>

tasks:
  chat-single-model:
    cmds:
      - panel serve chat-single-model.py --autoreload

  chat-model-switcher:
    cmds:
      - panel serve chat-model-switcher.py --autoreload

  chat-contexts:
    cmds:
      - panel serve chat-contexts.py --autoreload
```

### Available examples

- `chat-single-model` showcasing a single model chat interface.
- `chat-model-switcher` showcasing a chat interface with model switching.
- `chat-contexts` showcasing a chat interface with chat history switching.