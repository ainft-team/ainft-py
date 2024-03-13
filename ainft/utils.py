from __future__ import annotations

from datetime import datetime
from typing import Any


def get_app_id(object_id: str) -> str:
    return f"ainft721_{object_id.lower()}"


def is_tx_success(tx_result: Any) -> bool:
    result = tx_result.get("result", {})
    if result.get("code") is not None and result["code"] != 0:
        return False
    if "result_list" in result:
        results = result["result_list"].values()
        return all(r.get("code") == 0 for r in results)
    return True


def join_paths(paths: list) -> str:
    return "/".join(paths)


def now() -> float:
    return datetime.now().timestamp()
