from abc import ABC, abstractmethod
from typing import Any


class MultiViewEngine(ABC):
    name = "base-multiview"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, image: Any) -> Any:
        raise NotImplementedError
