from __future__ import annotations

from datetime import datetime
import re
import uuid
from typing import Any


from ain.ain import Database


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


async def validate_app(app_id: str, db: Database):
    app_path = join_paths(["apps", app_id])
    app = await db.ref(app_path).getValue()
    if app is None:
        raise ValueError(f"The app {app_id} does not exist.")


async def validate_token(app_id: str, token_id: str, db: Database):
    token_path = join_paths(["apps", app_id, "tokens", token_id])
    token = await db.ref(token_path).getValue()
    if token is None:
        raise ValueError(f"The token {token_id} does not exist.")


def validate_thread_id(thread_id: str):
    if not is_valid_thread_id(thread_id):
        raise ValueError(f"Invalid thread ID.")


def is_valid_thread_id(thread_id: str) -> bool:
    try:
        return str(uuid.UUID(thread_id, version=4)) == thread_id
    except ValueError:
        pass
    pattern = r"thread_[A-Za-z0-9]{20}$"
    if re.match(pattern, thread_id):
        return True
    return False
