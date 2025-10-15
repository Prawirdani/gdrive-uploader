import json
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    client_id: str
    client_secret: str
    refresh_token: str
    scopes: List[str]
    folder_id: str


def load_config(filepath: str) -> Config:
    with open(filepath, "r") as file:
        data = json.load(file)
    return Config(**data)


if __name__ == "__main__":
    cfg = load_config("config.json")
    print(cfg)
