from datetime import datetime


def get_timestamp() -> str:
    """
    Get timestamp string in YYYY-MM-DD_HHMMSS format
    :return: timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")
