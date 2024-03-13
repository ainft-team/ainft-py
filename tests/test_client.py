from __future__ import annotations

from ainft.client import Ainft

from .data import *


class TestAinft:
    def test_initialization(self) -> None:
        ainft = Ainft(
            private_key=private_key,
            api_url=api_url,
            blockchain_url=blockchain_url,
            chain_id=chain_id,
        )
        assert ainft._base_url == "https://ainft-api-dev.ainetwork.ai"
        assert ainft._blockchain_url == "https://testnet-api.ainetwork.ai"
        assert ainft._chain_id == 0
        assert (
            ainft._ain.wallet.defaultAccount.address
            == "0x7ed9c30C9F3A31Daa9614b90B4a710f61Bd585c0"
        )
