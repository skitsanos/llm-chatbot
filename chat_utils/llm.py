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
        "GPT-4o":
            {
                "model": "gpt-4o",
                "base_url": "https://api.openai.com/v1",
                "provider": "openai",
                "context_window": 128000
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
