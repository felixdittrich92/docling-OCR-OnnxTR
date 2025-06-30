# Copyright (C) 2021-2025, Felix Dittrich.

# This program is licensed under the Apache License 2.0.
# See LICENSE or go to <https://opensource.org/licenses/Apache-2.0> for full license details.

from typing import Any, ClassVar, Literal

from docling.datamodel.pipeline_options import OcrOptions
from pydantic import ConfigDict

__all__ = ["OnnxtrOcrOptions"]


class OnnxtrOcrOptions(OcrOptions):
    """Options for the Onnxtr engine."""

    kind: ClassVar[Literal["onnxtr"]] = "onnxtr"

    lang: list[str] = ["en", "fr"]
    # word confidence threshold for the recognition model
    confidence_score: float = 0.5
    # detection model objectness score threshold 'fast algorithm'
    objectness_score: float = 0.3

    # NOTE: This can be also a hf hub model or an instance of a model class.
    det_arch: Any = "fast_base"
    reco_arch: Any = "crnn_vgg16_bn"
    reco_bs: int = 512
    auto_correct_orientation: bool = False
    preserve_aspect_ratio: bool = True
    symmetric_pad: bool = True
    paragraph_break: float = 0.035
    load_in_8_bit: bool = False
    # Ref.: https://onnxruntime.ai/docs/api/python/api_summary.html
    providers: list[tuple[str, dict[str, Any]]] | None = None
    session_options: Any | None = None

    model_config = ConfigDict(
        extra="forbid",
    )
