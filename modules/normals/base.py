from abc import ABC, abstractmethod
from typing import Any


class NormalEngine(ABC):
    name = "base-normals"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, image: Any) -> Any:
        raise NotImplementedError
