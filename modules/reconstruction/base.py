from abc import ABC, abstractmethod
from typing import Any


class ReconstructionEngine(ABC):
    name = "base-reconstruction"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, data: Any) -> Any:
        raise NotImplementedError
