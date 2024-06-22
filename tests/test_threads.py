from __future__ import annotations

import re
from ainft.client import Ainft

from .data import *


class TestThreads:
    ainft = Ainft(
        private_key=private_key,
        api_url=api_url,
        blockchain_url=blockchain_url,
        chain_id=chain_id,
    )

    async def test_method_add(self):
        result = await self.ainft.chat.threads.add(
            thread_id=thread_id,
            object_id=object_id,
            token_id=token_id,
        )

        assert re.match(tx_pattern, result.tx_hash) is not None
        assert result.result is not None
        assert result.thread.id == thread_id
