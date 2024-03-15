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

    async def test_method_store(self):
        messages = [
            Message(
                id="1",
                thread_id="15f576b9-2bba-446b-b416-5cff3687f5da",
                role="user",
                content="What is your name?",
                assistant_id=None,
                created_at=1687578250,
            ),
            Message(
                id="2",
                thread_id="15f576b9-2bba-446b-b416-5cff3687f5da",
                role="assistant",
                content="I am aina from ai network.",
                assistant_id="asst_000000000000000000000001",
                created_at=1691639048,
            ),
        ]

        result = await self.ainft.chat.messages.store(
            messages=messages,
            object_id=object_id,
            token_id=token_id,
        )

        assert re.match(tx_pattern, result.tx_hash) is not None
        assert result.result is not None
        assert len(result.messages) == 2
