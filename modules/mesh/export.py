from pathlib import Path
from typing import Any


SUPPORTED_FORMATS = {
    ".obj",
    ".ply",
    ".stl",
    ".glb",
    ".gltf",
}


def export_mesh(mesh: Any, output_path: str | Path) -> Path:
    """Placeholder para futura exportação de mesh."""

    output_path = Path(output_path)

    if output_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Formato não suportado: {output_path.suffix}"
        )

    raise NotImplementedError(
        "Exportação de mesh ainda não implementada."
    )
