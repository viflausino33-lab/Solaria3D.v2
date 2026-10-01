from typing import Any


class EngineRegistry:
    """Registro de motores substituíveis do Solaria."""

    def __init__(self) -> None:
        self._engines: dict[str, Any] = {}

    def register(self, name: str, engine: Any) -> None:
        self._engines[name] = engine

    def get(self, name: str) -> Any:
        if name not in self._engines:
            raise KeyError(f"Motor não registrado: {name}")

        return self._engines[name]

    def has(self, name: str) -> bool:
        return name in self._engines

    def names(self) -> list[str]:
        return sorted(self._engines.keys())
