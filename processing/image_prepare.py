from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from PIL import Image


BackgroundMode = Literal["black", "white", "keep"]


@dataclass(frozen=True)
class ImagePreparationResult:
    """
    Resultado completo da preparação de uma imagem para o Solaria.

    Todas as dimensões seguem o formato (largura, altura), igual ao PIL.
    """

    image: Image.Image
    mask: Image.Image

    original_size: tuple[int, int]
    object_box: tuple[int, int, int, int]
    cropped_size: tuple[int, int]
    processing_size: tuple[int, int]

    scale_x: float
    scale_y: float

    target_long_side: int | None
    multiple: int
    background_mode: BackgroundMode

    def metadata(self) -> dict[str, object]:
        """
        Retorna as informações necessárias para rastrear a transformação.
        """

        return {
            "original_size": self.original_size,
            "object_box": self.object_box,
            "cropped_size": self.cropped_size,
            "processing_size": self.processing_size,
            "scale_x": self.scale_x,
            "scale_y": self.scale_y,
            "target_long_side": self.target_long_side,
            "multiple": self.multiple,
            "background_mode": self.background_mode,
        }


def _validate_image(image: Image.Image) -> Image.Image:
    if not isinstance(image, Image.Image):
        raise TypeError("A imagem precisa ser uma instância de PIL.Image.Image.")

    return image.convert("RGB")


def _validate_mask(
    mask: Image.Image | None,
    size: tuple[int, int],
) -> Image.Image:
    if mask is None:
        return Image.new("L", size, 255)

    if not isinstance(mask, Image.Image):
        raise TypeError("A máscara precisa ser uma instância de PIL.Image.Image.")

    mask = mask.convert("L")

    if mask.size != size:
        mask = mask.resize(size, Image.Resampling.NEAREST)

    return mask


def _find_bbox(
    mask: Image.Image,
) -> tuple[int, int, int, int]:
    """
    Encontra a bounding box do objeto a partir da máscara.

    Retorna:
        (left, top, right, bottom)
    """

    mask_array = np.asarray(mask, dtype=np.uint8)

    ys, xs = np.where(mask_array > 0)

    if len(xs) == 0 or len(ys) == 0:
        raise ValueError("A máscara não contém nenhum pixel pertencente ao objeto.")

    left = int(xs.min())
    top = int(ys.min())
    right = int(xs.max()) + 1
    bottom = int(ys.max()) + 1

    return left, top, right, bottom


def _expand_bbox(
    bbox: tuple[int, int, int, int],
    image_size: tuple[int, int],
    margin: float,
) -> tuple[int, int, int, int]:
    """
    Expande a bounding box proporcionalmente ao maior lado do objeto.
    """

    if margin < 0:
        raise ValueError("margin não pode ser negativo.")

    if margin == 0:
        return bbox

    image_width, image_height = image_size

    left, top, right, bottom = bbox

    object_width = right - left
    object_height = bottom - top

    base = max(object_width, object_height)
    padding = int(round(base * margin))

    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image_width, right + padding)
    bottom = min(image_height, bottom + padding)

    return left, top, right, bottom


def _crop(
    image: Image.Image,
    mask: Image.Image,
    bbox: tuple[int, int, int, int],
) -> tuple[Image.Image, Image.Image]:
    return image.crop(bbox), mask.crop(bbox)


def _apply_background(
    image: Image.Image,
    mask: Image.Image,
    mode: BackgroundMode,
) -> Image.Image:
    """
    Aplica o tratamento do fundo mantendo a máscara separada.

    black:
        pixels fora do objeto ficam pretos.

    white:
        pixels fora do objeto ficam brancos.

    keep:
        o conteúdo original é preservado.
    """

    if mode == "keep":
        return image.copy()

    if mode == "black":
        background = Image.new("RGB", image.size, (0, 0, 0))
    elif mode == "white":
        background = Image.new("RGB", image.size, (255, 255, 255))
    else:
        raise ValueError(
            "background_mode precisa ser 'black', 'white' ou 'keep'."
        )

    return Image.composite(image, background, mask)


def _calculate_processing_size(
    size: tuple[int, int],
    target_long_side: int | None,
    multiple: int,
) -> tuple[int, int]:
    """
    Calcula a resolução final.

    Primeiro, opcionalmente, ajusta o maior lado para target_long_side.

    Depois arredonda cada dimensão para o próximo múltiplo de `multiple`.

    Isso mantém a imagem retangular e garante compatibilidade com o pipeline
    espacial usado pelo Marigold V2.
    """

    width, height = size

    if width <= 0 or height <= 0:
        raise ValueError("A imagem precisa possuir dimensões positivas.")

    if multiple <= 0:
        raise ValueError("multiple precisa ser maior que zero.")

    if target_long_side is not None:
        if target_long_side <= 0:
            raise ValueError("target_long_side precisa ser maior que zero.")

        current_long_side = max(width, height)

        scale = target_long_side / current_long_side

        width = max(1, int(round(width * scale)))
        height = max(1, int(round(height * scale)))

    processing_width = ((width + multiple - 1) // multiple) * multiple
    processing_height = ((height + multiple - 1) // multiple) * multiple

    return processing_width, processing_height


def _resize(
    image: Image.Image,
    mask: Image.Image,
    processing_size: tuple[int, int],
) -> tuple[Image.Image, Image.Image]:
    """
    Redimensiona RGB com Lanczos e máscara com nearest neighbor.
    """

    if image.size != processing_size:
        image = image.resize(
            processing_size,
            Image.Resampling.LANCZOS,
        )

    if mask.size != processing_size:
        mask = mask.resize(
            processing_size,
            Image.Resampling.NEAREST,
        )

    return image, mask


def prepare_image(
    image: Image.Image,
    mask: Image.Image | None = None,
    *,
    crop_to_mask: bool = True,
    margin: float = 0.05,
    target_long_side: int | None = None,
    multiple: int = 16,
    background_mode: BackgroundMode = "black",
) -> ImagePreparationResult:
    """
    Prepara uma imagem para futura inferência do Solaria / Marigold V2.

    Parâmetros
    ----------
    image:
        Imagem RGB original.

    mask:
        Máscara do objeto em tons de cinza.
        Pixels > 0 pertencem ao objeto.

        Quando None:
            toda a imagem é considerada objeto.

    crop_to_mask:
        Quando True e existe máscara, corta a imagem em torno do objeto.

    margin:
        Margem proporcional acrescentada ao redor da bounding box.

        Exemplo:
            0.05 = 5% do maior lado do objeto.

    target_long_side:
        Define o tamanho desejado para o maior lado.

        None:
            mantém a resolução aproximada original e apenas ajusta
            as dimensões para múltiplos de `multiple`.

    multiple:
        Múltiplo espacial exigido pelo pipeline.
        Para o Solaria / Marigold V2 usamos 16.

    background_mode:
        "black":
            remove visualmente o fundo e coloca preto.

        "white":
            remove visualmente o fundo e coloca branco.

        "keep":
            mantém o conteúdo original fora do objeto.

    Retorno
    -------
    ImagePreparationResult
        Contém:
        - imagem preparada;
        - máscara preparada;
        - bounding box;
        - dimensões originais;
        - dimensões após crop;
        - dimensões finais;
        - fatores de escala;
        - metadata para rastreamento.
    """

    image = _validate_image(image)
    mask = _validate_mask(mask, image.size)

    original_size = image.size

    if crop_to_mask and mask is not None:
        bbox = _find_bbox(mask)
        bbox = _expand_bbox(
            bbox=bbox,
            image_size=image.size,
            margin=margin,
        )
    else:
        bbox = (0, 0, image.width, image.height)

    image_cropped, mask_cropped = _crop(
        image=image,
        mask=mask,
        bbox=bbox,
    )

    image_cropped = _apply_background(
        image=image_cropped,
        mask=mask_cropped,
        mode=background_mode,
    )

    cropped_size = image_cropped.size

    processing_size = _calculate_processing_size(
        size=cropped_size,
        target_long_side=target_long_side,
        multiple=multiple,
    )

    image_processed, mask_processed = _resize(
        image=image_cropped,
        mask=mask_cropped,
        processing_size=processing_size,
    )

    scale_x = processing_size[0] / cropped_size[0]
    scale_y = processing_size[1] / cropped_size[1]

    return ImagePreparationResult(
        image=image_processed,
        mask=mask_processed,
        original_size=original_size,
        object_box=bbox,
        cropped_size=cropped_size,
        processing_size=processing_size,
        scale_x=scale_x,
        scale_y=scale_y,
        target_long_side=target_long_side,
        multiple=multiple,
        background_mode=background_mode,
    )


def image_to_tensor_range_m11(image: Image.Image) -> np.ndarray:
    """
    Converte uma imagem PIL RGB para CHW float32 em [-1, 1].

    A implementação do Marigold V2 utiliza exatamente essa faixa de entrada.
    """

    image = _validate_image(image)

    array = np.asarray(image, dtype=np.float32)

    normalized = array / 255.0 * 2.0 - 1.0

    return np.transpose(
        normalized,
        (2, 0, 1),
    ).astype(np.float32, copy=False)


def mask_to_numpy(mask: Image.Image) -> np.ndarray:
    """
    Converte a máscara para float32 em [0, 1].
    """

    if not isinstance(mask, Image.Image):
        raise TypeError("A máscara precisa ser uma instância de PIL.Image.Image.")

    array = np.asarray(
        mask.convert("L"),
        dtype=np.float32,
    )

    return array / 255.