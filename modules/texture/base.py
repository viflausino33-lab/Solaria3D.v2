from abc import ABC, abstractmethod
from typing import Any


class TextureEngine(ABC):
    name = "base-texture"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, mesh: Any, images: Any = None) -> Any:
        raise NotImplementedError
