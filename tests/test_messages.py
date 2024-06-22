from __future__ import annotations

import re

from ainft.client import Ainft
from ainft.types import Message

from .data import *


class TestMessages:
    ainft = Ainft(
        private_key=private_key,
        api_url=api_url,
        blockchain_url=blockchain_url,
        chain_id=chain_id,
    )

    async def test_method_add(self):
        messages = [
            Message(
                id="1",
                thread_id=thread_id,
                role="user",
                content="What is your name?",
                assistant_id=None,
                created_at=1687578250,
            ),
            Message(
                id="2",
                thread_id=thread_id,
                role="assistant",
                content="I am aina from ai network.",
                assistant_id="asst_000000000000000000000001",
                created_at=1691639048,
            ),
        ]

        result = await self.ainft.chat.messages.add(
            messages=messages,
            object_id=object_id,
            token_id=token_id,
        )

        assert re.match(tx_pattern, result.tx_hash) is not None
        assert result.result is not None
        assert len(result.messages) == 2

    async def test_method_add_with_emojis(self):
        message = Message(
            id="3",
            thread_id=thread_id,
            role="user",
            content="How are you today? 😊",
            assistant_id=None,
            created_at=1710748302,
        )

        result = await self.ainft.chat.messages.add(
            messages=[message],
            object_id=object_id,
            token_id=token_id,
        )
        path = f"apps/{app_id}/tokens/{token_id}/ai/history/{address}/threads/{thread_id}/messages/{message.created_at}"
        escaped_message = await self.ainft._ain.db.ref(path).getValue()

        assert re.match(tx_pattern, result.tx_hash) is not None
        assert result.result is not None
        assert len(result.messages) == 1
        assert (
            escaped_message["content"].encode("ASCII").decode("unicode-escape")
            == message.content
        )
