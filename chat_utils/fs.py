import json
import os
from typing import List, Dict


def prepare_folders(folders: List[str]):
    """
    Prepare folders for saving files
    :param folders: List of folder paths
    :return: None
    """
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)


def save_jsonl(file_path: str, data: List[Dict]):
    """
    Save a list of dictionaries to a jsonl file
    :param file_path: Path to the file
    :param data: List of dictionaries
    :return: None
    """
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def load_jsonl(file_path: str) -> List[Dict]:
    """
    Load a list of dictionaries from a jsonl file
    :param file_path: Path to the file
    :return: List of dictionaries
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data
