from __future__ import annotations

import json
import re
import uuid
from typing import Dict, Optional

from ain.ain import Ain

from ..types import SetOperation, TransactionInput, Thread, ThreadTransactionResult
from ..utils import get_app_id, is_tx_success, join_paths, now


class Threads:
    def __init__(self, ain: Ain):
        self._ain = ain

    async def store(
        self,
        *,
        thread_id: str,
        object_id: str,
        token_id: str,
        metadata: Optional[object] = None,
    ) -> ThreadTransactionResult:
        """
        Store a thread.

        Args:
            thread_id: The ID of the thread,
                must be a 20-character alphanumeric starting with 'thread_' or a uuid4.

            object_id: The ID of the AINFT object.

            token_id: The ID of the AINFT token.

            metadata: The metadata can contain up to 16 key-value pairs,
                with the keys limited to 64 characters and the values to 512 characters.
        """
        app_id = get_app_id(object_id)
        user_addr = self._ain.wallet.defaultAccount.address

        await self._validate_app(app_id)
        await self._validate_token(app_id, token_id)
        self._validate_thread_id(thread_id)

        return await self._send_tx_for_store_thread(**dict(
            thread_id=thread_id,
            app_id=app_id,
            token_id=token_id,
            address=user_addr,
            metadata=metadata,
        ))

    async def _validate_app(self, app_id: str):
        app_path = join_paths(["apps", app_id])
        app = await self._ain.db.ref(app_path).getValue()
        if app is None:
            raise ValueError(f"The app {app_id} does not exist.")

    async def _validate_token(self, app_id: str, token_id: str):
        token_path = join_paths(["apps", app_id, "tokens", token_id])
        token = await self._ain.db.ref(token_path).getValue()
        if token is None:
            raise ValueError(f"The token {token_id} does not exist.")

    def _validate_thread_id(self, thread_id: str):
        if not self._is_valid_thread_id(thread_id):
            raise ValueError(f"Invalid thread ID.")

    def _is_valid_thread_id(self, thread_id: str) -> bool:
        try:
            thread_uuid = uuid.UUID(thread_id, version=4)
            return str(thread_uuid) == thread_id
        except ValueError:
            pass
        pattern = r"thread_[A-Za-z0-9]{20}$"
        if re.match(pattern, thread_id):
            return True
        return False

    async def _send_tx_for_store_thread(self, **kwargs) -> ThreadTransactionResult:
        timestamp = int(now())
        tx_body = self._build_tx_body_for_store_thread(timestamp=timestamp, **kwargs)
        tx_result = await self._ain.sendTransaction(tx_body)

        if not is_tx_success(tx_result):
            raise RuntimeError(f"Failed to send transaction: {json.dumps(tx_result)}")

        return self._format_tx_result(tx_result, timestamp, **kwargs)

    def _build_tx_body_for_store_thread(
        self,
        app_id: str,
        token_id: str,
        address: str,
        thread_id: str,
        timestamp: int,
        metadata: Optional[object],
    ) -> TransactionInput:
        thread_path = join_paths(
            [
                "apps",
                app_id,
                "tokens",
                token_id,
                "ai",
                "ainize_openai",
                "history",
                address,
                "threads",
                thread_id,
            ]
        )
        value = {"messages": True}
        if metadata:
            value["metadata"] = metadata
        operation = SetOperation(type="SET_VALUE", ref=thread_path, value=value)
        return TransactionInput(
            operation=operation,
            timestamp=timestamp,
            nonce=-1,
            address=address,
            gas_price=500,
        )

    def _format_tx_result(
        self,
        tx_result: dict,
        timestamp: int,
        thread_id: str,
        **kwargs,
    ) -> ThreadTransactionResult:
        metadata = kwargs.get("metadata", {})
        thread = Thread(id=thread_id, metadata=metadata, created_at=timestamp)
        return ThreadTransactionResult(
            tx_hash=tx_result["tx_hash"], result=tx_result["result"], thread=thread
        )
