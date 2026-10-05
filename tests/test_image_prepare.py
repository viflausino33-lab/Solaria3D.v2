from PIL import Image, ImageDraw

from processing.image_prepare import (
    image_to_tensor_range_m11,
    mask_to_numpy,
    prepare_image,
)


def criar_imagem_teste():
    imagem = Image.new(
        "RGB",
        (501, 337),
        (120, 140, 160),
    )

    mascara = Image.new(
        "L",
        (501, 337),
        0,
    )

    desenho = ImageDraw.Draw(mascara)

    desenho.rectangle(
        (100, 50, 400, 280),
        fill=255,
    )

    return imagem, mascara


def test_prepare_image():
    imagem, mascara = criar_imagem_teste()

    resultado = prepare_image(
        imagem,
        mascara,
        crop_to_mask=True,
        margin=0.05,
        multiple=16,
        background_mode="black",
    )

    assert resultado.original_size == (501, 337)

    assert resultado.cropped_size == (331, 261)

    largura, altura = resultado.processing_size

    assert largura % 16 == 0
    assert altura % 16 == 0

    assert resultado.image.size == resultado.processing_size
    assert resultado.mask.size == resultado.processing_size


def test_image_to_tensor_range_m11():
    imagem = Image.new(
        "RGB",
        (32, 48),
        (255, 128, 0),
    )

    tensor = image_to_tensor_range_m11(imagem)

    assert tensor.shape == (3, 48, 32)

    assert tensor.dtype.name == "float32"

    assert tensor.min() >= -1.0
    assert tensor.max() <= 1.0

    assert abs(float(tensor[0].max()) - 1.0) < 1e-6


def test_mask_to_numpy():
    mascara = Image.new(
        "L",
        (32, 16),
        255,
    )

    array = mask_to_numpy(mascara)

    assert array.shape == (16, 32)

    assert array.dtype.name == "float32"

    assert array.min() == 1.0
    assert array.max() == 1.0


def test_mask_without_object_fails():
    imagem = Image.new(
        "RGB",
        (128, 128),
        "white",
    )

    mascara = Image.new(
        "L",
        (128, 128),
        0,
    )

    try:
        prepare_image(
            imagem,
            mascara,
        )
    except ValueError as erro:
        assert "nenhum pixel" in str(erro)
    else:
        raise AssertionError(
            "Era esperado ValueError para uma mascara sem objeto."
        )
