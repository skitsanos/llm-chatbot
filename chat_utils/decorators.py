import inspect
from typing import Any, Dict, Annotated

# Mapping Python types to JSON schema types
TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object"
}


def openai_tool(
        func
        ):
    signature = inspect.signature(func)
    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }

    for name, param in signature.parameters.items():
        param_type = TYPE_MAP.get(param.annotation.__origin__, "string") if hasattr(
            param.annotation, '__origin__') else TYPE_MAP.get(param.annotation, "string")
        if hasattr(param.annotation, '__metadata__'):
            description = param.annotation.__metadata__[0]
            parameters["properties"][name] = {
                "type": param_type,
                "description": description
            }
            parameters["required"].append(name)

    func.tool = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": parameters
        }
    }
    return func
