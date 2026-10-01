from abc import ABC, abstractmethod
from typing import Any


class DepthEngine(ABC):
    name = "base-depth"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, image: Any) -> Any:
        raise NotImplementedError
