from dataclasses import dataclass, field
from typing import Any


@dataclass
class InputImage:
    image: Any


@dataclass
class SegmentationResult:
    mask: Any = None
    object_image: Any = None


@dataclass
class DepthResult:
    depth: Any = None
    confidence: Any = None


@dataclass
class NormalResult:
    normals: Any = None


@dataclass
class MultiViewResult:
    views: list[Any] = field(default_factory=list)


@dataclass
class ReconstructionResult:
    point_cloud: Any = None
    mesh: Any = None


@dataclass
class PipelineState:
    input_image: Any = None
    segmentation: SegmentationResult | None = None
    depth: DepthResult | None = None
    normals: NormalResult | None = None
    multiview: MultiViewResult | None = None
    reconstruction: ReconstructionResult | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
