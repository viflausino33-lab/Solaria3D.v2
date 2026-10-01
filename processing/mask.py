from PIL import Image


def validate_mask(mask: Image.Image) -> Image.Image:
    if not isinstance(mask, Image.Image):
        raise TypeError("A máscara precisa ser uma imagem PIL.Image.")

    return mask.convert("L")
