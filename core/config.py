from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class SolariaConfig:
    """Configurações gerais do projeto."""

    project_root: Path = PROJECT_ROOT
    models_dir: Path = PROJECT_ROOT / "models"
    examples_dir: Path = PROJECT_ROOT / "examples"

    device: str = "auto"

    segmentation_model: str = ""
    depth_model: str = ""
    normals_model: str = ""
    multiview_model: str = ""
    reconstruction_model: str = ""
    texture_model: str = ""
