from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class DepthResult:
    """
    Resultado padronizado de um motor de profundidade.

    depth:
        Mapa de profundidade em formato H x W.

    source_size:
        Dimensão da imagem que originou o resultado,
        no formato (largura, altura).

    model_name:
        Nome do motor responsável pela inferência.

    metadata:
        Informações adicionais específicas do motor.
    """

    depth: np.ndarray
    source_size: tuple[int, int]
    model_name: str
    metadata: dict[str, Any]


class DepthEngine(ABC):
    """
    Interface base para qualquer motor de profundidade do Solaria.

    O restante do sistema não deve depender diretamente do Marigold,
    Depth Anything ou outro modelo específico.

    Cada implementação deverá apenas:
        1. carregar o modelo;
        2. receber uma imagem preparada;
        3. produzir um DepthResult.
    """

    name = "base-depth"

    def __init__(self) -> None:
        self.loaded = False

    @abstractmethod
    def load(self) -> None:
        """
        Carrega pesos, modelo e recursos necessários.
        """
        raise NotImplementedError

    @abstractmethod
    def run(self, image: Any) -> DepthResult:
        """
        Executa a inferência de profundidade.

        Parameters
        ----------
        image:
            Imagem já preparada pelo pipeline do Solaria.
        """
        raise NotImplementedError

    def ensure_loaded(self) -> None:
        """
        Garante que m motor esteja carregado antes da inferencia.
        """

        if not self.loaded:
            self.load()

    @staticmethod
    def validate_depth(
        depth: Any,
    ) -> np.ndarray:
        """
        Valida e padroniza um mapa de profundidade.

        O Solaria trabalha internamente com:
            H x W
            float32
        """

        array = np.asarray(depth)

        if array.ndim != 2:
            raise ValueError(
                "O mapa de profundidade precisa possuir exatamente "
                "2 dimensões no formato H x W."
            )

        if array.size == 0:
            raise ValueError(
                "O mapa de profundidade está vazio."
            )

        if not np.issubdtype(array.dtype, np.number):
            raise TypeError(
                "O mapa de profundidade precisa conter valores numéricos."
            )

        array = array.astype(
            np.float32,
            copy=False,
        )

        if not np.all(np.isfinite(array)):
            raise ValueError(
                "O mapa de profundidade contém valores NaN ou infinitos."
            )

        return array

    def create_result(self, depth: Any, source_size: tuple[int, int], metadata: dict[str, Any] | None = None) -> DepthResult:
        validated_depth = self.validate_depth(depth)
        if len(source_size) != 2:
            raise ValueError("source_size precisa estar no formato (largura, altura).")
        width, height = source_size
        if width <= 0 or height <= 0:
            raise ValueError("source_size precisa possuir dimensões positivas.")
        return DepthResult(depth=validated_depth,source_size=(int(width), int(height)),model_name=self.name,metadata=metadata or {})