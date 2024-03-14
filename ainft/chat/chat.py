from __future__ import annotations

from functools import cached_property

from ain.ain import Ain

from .threads import Threads


class Chat:
    def __init__(self, ain: Ain) -> None:
        self._ain = ain

    @cached_property
    def threads(self) -> Threads:
        return Threads(self._ain)
