from __future__ import annotations

from typing_extensions import Literal
from ain.ain import Ain


class Ainft:
    def __init__(
        self,
        *,
        private_key: str,
        api_url: str,
        blockchain_url: str,
        chain_id: Literal[0, 1],
    ) -> None:
        self._base_url = api_url
        self._blockchain_url = blockchain_url
        self._chain_id = chain_id

        self._ain = Ain(self._blockchain_url, self._chain_id)
        self._add_user_account(private_key)

    def _add_user_account(self, private_key: str) -> None:
        self._ain.wallet.clear()
        self._ain.wallet.addAndSetDefaultAccount(private_key)
