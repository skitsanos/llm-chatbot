"""
Mock openai_tools for testing
"""
import json
from typing import Any, Dict, Annotated

from chat_utils.decorators import openai_tool


@openai_tool
def get_product_details(
        product_id: Annotated[str, "Product ID, ex.: 'SKU-12345'"]
) -> Annotated[str, "Get product details for the given product_id and return in JSON format"]:
    """Get product details by product ID."""
    return json.dumps({
        "product_id": product_id,
        "name": "Product Name",
        "description": "Product Description",
        "price": 100.0
    })


@openai_tool
def send_email(
        email: Annotated[str, "Recipient email address"],
        subject: Annotated[str, "Email subject"],
        message: Annotated[str, "Email message"]
) -> Annotated[Dict[str, Any], "Send an email to the recipient"]:
    """Send an email to the recipient."""
    return {
        "email": email,
        "subject": subject,
        "message": message
    }


@openai_tool
def get_current_weather(
        location: Annotated[str, "Location name"]
) -> Annotated[str, "Get current weather details for the given location in JSON format"]:
    """Get current weather details by location."""
    return json.dumps({
        "location": location,
        "temperature": 25.0,
        "description": "Sunny"
    })
