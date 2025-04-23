import json
from typing import Any


def format_json(json_object: Any) -> str:
    return json.dumps(
        json_object,
        indent=4,
        ensure_ascii=False,
    )
