import numpy as np
import pytest

from modules.depth.base import DepthEngine, DepthResult


class DummyDepthEngine(DepthEngine):
    name = "dummy-depth"

    def load(self) -> None:
        self.loaded = True

    def run(self, image):
        self.ensure_loaded()

        depth = np.ones((4, 6), dtype=np.float32)

        return self.create_result(
            depth=depth,
            source_size=(6, 4),
            metadata={"test": True},
        )


def test_depth_engine_loads_on_demand():
    engine = DummyDepthEngine()

    assert engine.loaded is False

    result = engine.run(None)

    assert engine.loaded is True
    assert isinstance(result, DepthResult)
    assert result.depth.shape == (4, 6)
    assert result.depth.dtype == np.float32
    assert result.source_size == (6, 4)
    assert result.model_name == "dummy-depth"
    assert result.metadata["test"] is True


def test_validate_depth_converts_to_float32():
    depth = np.array(
        [[1, 2], [3, 4]],
        dtype=np.float64,
    )

    result = DepthEngine.validate_depth(depth)

    assert result.shape == (2, 2)
    assert result.dtype == np.float32
    np.testing.assert_array_equal(
        result,
        depth,
    )


def test_validate_depth_rejects_wrong_dimensions():
    depth = np.ones(
        (2, 3, 4),
        dtype=np.float32,
    )

    with pytest.raises(ValueError, match="2 dimensões"):
        DepthEngine.validate_depth(depth)


def test_validate_depth_rejects_nan():
    depth = np.array(
        [[1.0, np.nan]],
        dtype=np.float32,
    )

    with pytest.raises(ValueError, match="NaN"):
        DepthEngine.validate_depth(depth)


def test_validate_depth_rejects_empty():
    depth = np.empty(
        (0, 4),
        dtype=np.float32,
    )

    with pytest.raises(ValueError, match="vazio"):
        DepthEngine.validate_depth(depth)


def test_create_result_rejects_invalid_source_size():
    engine = DummyDepthEngine()

    with pytest.raises(
        ValueError,
        match="dimensões positivas",
    ):
        engine.create_result(
            depth=np.ones((2, 2), dtype=np.float32),
            source_size=(0, 2),
        )
