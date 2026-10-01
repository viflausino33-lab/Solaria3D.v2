from abc import ABC, abstractmethod
from typing import Any


class SegmentationEngine(ABC):
    name = "base-segmentation"

    @abstractmethod
    def load(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def run(self, image: Any) -> Any:
        raise NotImplementedError
