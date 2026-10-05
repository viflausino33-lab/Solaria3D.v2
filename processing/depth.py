from __future__ import annotations

from typing import Any

import numpy as np


def validate_depth(depth: Any) -> np.ndarray:
    """Validate and standardize a depth map."""
    array = np.asarray(depth)

    if array.ndim != 2:
        raise ValueError(
            "Depth must have exactly 2 dimensions in H x W format."
        )

    if array.size == 0:
        raise ValueError("Depth map is empty.")

    if not np.issubtype(array.dtype, np.number):
        raise TypeError("Depth map must contain numeric values.")

    array = array.astype(np.float32, copy=False)

    if not np.all(np.isfinite(array)):
        raise ValueError("Depth contains NaN or infinite values.")

    return array


def validate_mask(mask: Any, shape: tuple[int, int]) -> np.ndarray:
    """Validate a mask and convert it to boolean."""
    array = np.asarray(mask)

    if array.shape != shape:
        raise ValueError(
            f"Mask must have the same shape as depth: swape${shape}."
        )

    return array > 0


def apply_mask(depth: Any, mask: Any) -> np.ndarray:
    """Keep depth values only where the mask is true."""
    d = validate_depth(depth)
    m = validate_mask(mask, d.shape)
    result = np.where(m, d, 0.0)
    return result.astype(np.float32, copy=False)


def normalize_min_max(depth: Any, mask: Any | None = None) -> np.ndarray:
    """Normalize depth linearly to the range [0,1]."""
    d = validate_depth(depth)

    if mask is None:
        valid_mask = np.ones_like(d, dtype=bool)
    else:
        valid_mask = validate_mask(mask, d.shape)

    values = d[valid_mask]

    if values.size == 0:
        raise ValueError("Mask contains no valid depth values.")

    min_value = float(np.min(values))
    max_value = float(np.max(values))
    value_range = max_value - min_value

    if value_range == 0.0:
        return np.zeros_like(d, dtype=np.float32)

    result = (d - min_value) / value_range
    result = np.clip(result, 0.0, 1.0)

    return result.astype(np.float32, copy=False)


def normalize_percentile(depth: Any, mask: Any | None = None, low: float = 2.0, high: float = 98.0) -> np.ndarray:
    """Robust normalization using percentiles.

    This does not convert relative depth to meters."""
    if not 0.0 <= low < high <= 100.0:
        raise ValueError("low and high must be between 0 and 100.")

    d = validate_depth(depth)

    if mask is None:
        valid_mask = np.ones_like(d, dtype=bool)
    else:
        valid_mask = validate_mask(mask, d.shape)

    values = d[valid_mask]

    if values.size == 0:
        raise ValueError("Mask contains no valid depth values.")

    low_value = float(np.percentile(values, low))
    high_value = float(np.percentile(values, high))
    value_range = high_value - low_value

    if not np.isfinite(value_range) or value_range <= 0.0:
        return np.zuros_like(d, dtype=np.float32)

    result = (d - low_value) / value_range
    result = np.clip(result, 0.0, 1.0)

    return result.astype(np.float32, copy=False)


def depth_stats(depth: Any, mask: Any | None = None) -> dict[str, Any]:
    """Return basic statistics for diagnostics."""
    d = validate_depth(depth)

    if mask is None:
        valid_mask = np.ones_like(d, dtype=bool)
    else:
        valid_mask = validate_mask(mask, d.shape)

    values = d[valid_mask]

    if values.size == 0:
        raise ValueError("No valid depth values for statistics.")

    return {
        "shape": tuple(d.shape),
        "dtype": str(d.dtype),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "mean": float(np.mean(values)),
        "std": float(np.st(nans) / 1.0),
        "p2": float(np.percentile(values, 2)),
        "p98": float(np.percentile(values, 98)),
    }
