from typing_extensions import Annotated

from chat_utils.decorators import openai_tool
from datetime import datetime


@openai_tool
def today() -> Annotated[str, "Current date and time in ISO format"]:
    """Return the current date and time in ISO format."""
    return f"{datetime.now().isoformat()}Z"
