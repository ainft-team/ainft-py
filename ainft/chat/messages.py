from __future__ import annotations

import json
from typing import List

from ain.ain import Ain

from ..types import (
    SetOperation,
    SetMultiOperation,
    TransactionInput,
    Message,
    MessageTransactionResult,
)
from ..utils import *


class Messages:
    _max_content_length = 200

    def __init__(self, ain: Ain):
        self._ain = ain

    async def store(
        self,
        *,
        messages: List[Message],
        object_id: str,
        token_id: str,
    ) -> MessageTransactionResult:
        """
        Store a list of messages.

        Args:
            messages: The list of messages.

            object_id: The ID of the AINFT object.

            token_id: The ID of the AINFT token.
        """
        app_id = get_app_id(object_id)
        user_addr = validate_user_address(self._ain.wallet)

        await self._validate(app_id, token_id, user_addr, messages)

        return await self._send_tx_for_store_message(
            **dict(
                messages=messages,
                app_id=app_id,
                token_id=token_id,
                address=user_addr,
            )
        )

    async def _validate(
        self, app_id: str, token_id: str, address: str, messages: List[Message]
    ):
        await validate_app(app_id, self._ain.db)
        await validate_token(app_id, token_id, self._ain.db)
        for message in messages:
            await validate_thread(
                app_id, token_id, address, message.thread_id, self._ain.db
            )
            validate_message_id(message.id)

    async def _send_tx_for_store_message(self, **kwargs) -> MessageTransactionResult:
        timestamp = int(now())
        tx_body = self._build_tx_body_for_store_message(timestamp=timestamp, **kwargs)
        tx_result = await self._ain.sendTransaction(tx_body)

        if not is_tx_success(tx_result):
            raise RuntimeError(f"Failed to send transaction: {json.dumps(tx_result)}")

        return self._format_tx_result(tx_result=tx_result, **kwargs)

    def _build_tx_body_for_store_message(
        self,
        app_id: str,
        token_id: str,
        messages: List[Message],
        address: str,
        timestamp: int,
    ) -> TransactionInput:
        op_list = []
        for msg in messages:
            msg_key = str(msg.created_at)
            msg_path = join_paths(
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
                    msg.thread_id,
                    "messages",
                    msg_key,
                ]
            )
            trimmed_content = msg.content[: self._max_content_length]
            message = {
                "id": msg.id,
                "role": msg.role,
                "content": trimmed_content,
                **({"metadata": msg.metadata} if msg.metadata else {}),
            }
            op = SetOperation(type="SET_VALUE", ref=msg_path, value=message)
            op_list.append(op)

        multi_op = SetMultiOperation(type="SET", op_list=op_list)
        return TransactionInput(
            operation=multi_op,
            timestamp=timestamp,
            nonce=-1,
            address=address,
            gas_price=500,
        )

    def _format_tx_result(
        self, tx_result: dict, messages: List[Message], **kwargs
    ) -> MessageTransactionResult:
        return MessageTransactionResult(messages=messages, **tx_result)
