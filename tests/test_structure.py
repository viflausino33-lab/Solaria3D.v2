from core.config import SolariaConfig
from core.registry import EngineRegistry


def test_project_structure():
    config = SolariaConfig()

    assert config.project_root.exists()
    assert config.models_dir.exists()
    assert config.examples_dir.exists()


def test_registry():
    registry = EngineRegistry()
    engine = object()

    registry.register("teste", engine)

    assert registry.has("teste")
    assert registry.get("teste") is engine
    assert registry.names() == ["teste"]
