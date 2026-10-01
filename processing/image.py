from PIL import Image


def validate_image(image: Image.Image) -> Image.Image:
    if not isinstance(image, Image.Image):
        raise TypeError("A entrada precisa ser uma imagem PIL.Image.")

    return image.convert("RGBA")


def get_image_size(image: Image.Image) -> tuple[int, int]:
    image = validate_image(image)
    return image.size
