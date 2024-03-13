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

    async def test_method_store(self):
        result = await self.ainft.chat.threads.store(
            thread_id="15f576b9-2bba-446b-b416-5cff3687f5da",
            object_id=object_id,
            token_id=token_id,
        )

        tx_pattern = "^0x([A-Fa-f0-9]{64})$"
        assert re.match(tx_pattern, result.tx_hash) is not None
        assert result.result is not None
        assert result.thread.id == "15f576b9-2bba-446b-b416-5cff3687f5da"
