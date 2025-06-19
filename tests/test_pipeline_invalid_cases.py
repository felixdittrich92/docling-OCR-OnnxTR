from unittest.mock import MagicMock, patch

from docling.datamodel.base_models import Page
from docling.datamodel.pipeline_options import AcceleratorOptions
from docling.document_converter import ConversionResult

from docling_ocr_onnxtr.onnxtr_model import OnnxtrOcrModel
from docling_ocr_onnxtr.options import OnnxtrOcrOptions


def make_mock_page(valid=True):
    page = MagicMock(spec=Page)
    backend = MagicMock()
    backend.is_valid.return_value = valid
    page._backend = backend
    page.cells = []
    return page


@patch("onnxtr.models.ocr_predictor")
@patch("onnxtr.models.from_hub", side_effect=lambda x: x)
@patch("onnxtr.models.EngineConfig")
def test_call_enabled_skips_invalid_page(mock_engine_config, mock_from_hub, mock_ocr_predictor):
    options = OnnxtrOcrOptions(
        det_arch="det",
        reco_arch="reco",
        auto_correct_orientation=False,
    )

    mock_ocr_predictor.return_value = MagicMock()

    model = OnnxtrOcrModel(
        enabled=True,
        artifacts_path=None,
        options=options,
        accelerator_options=AcceleratorOptions(),
    )

    invalid_page = make_mock_page(valid=False)
    conv_res = MagicMock(spec=ConversionResult)

    result = list(model(conv_res, [invalid_page]))

    assert result == [invalid_page]


@patch("onnxtr.models.ocr_predictor")
@patch("onnxtr.models.from_hub", side_effect=lambda x: x)
@patch("onnxtr.models.EngineConfig")
def test_call_skips_zero_area_rects(mock_engine_config, mock_from_hub, mock_ocr_predictor):
    mock_predictor = MagicMock()
    mock_ocr_predictor.return_value = mock_predictor

    # Mock an OCR rect with area 0
    mock_rect = MagicMock()
    mock_rect.area.return_value = 0
    # Force get_ocr_rects to return our mocked zero-area rect
    model = OnnxtrOcrModel(
        enabled=True,
        artifacts_path=None,
        options=OnnxtrOcrOptions(
            det_arch="det",
            reco_arch="reco",
            auto_correct_orientation=False,
        ),
        accelerator_options=AcceleratorOptions(),
    )
    model.get_ocr_rects = MagicMock(return_value=[mock_rect])

    mock_page = make_mock_page(valid=True)
    mock_page.size = (1000, 1000)
    mock_page.image = MagicMock()
    mock_page.page_idx = 0
    mock_page.rotation = 0
    mock_page.parsed_page = MagicMock()

    conv_res = MagicMock(spec=ConversionResult)

    result = list(model(conv_res, [mock_page]))

    assert len(result) == 1
    assert result[0] is mock_page
    model.get_ocr_rects.assert_called_once()
    mock_rect.area.assert_called_once()


def test_call_disabled_returns_input():
    options = OnnxtrOcrOptions(
        det_arch="det",
        reco_arch="reco",
        auto_correct_orientation=False,
    )
    model = OnnxtrOcrModel(
        enabled=False,
        artifacts_path=None,
        options=options,
        accelerator_options=AcceleratorOptions(),
    )

    page = make_mock_page(valid=True)
    conv_res = MagicMock(spec=ConversionResult)
    result = list(model(conv_res, [page]))

    assert result == [page]


def test_call_skips_invalid_page():
    options = OnnxtrOcrOptions(
        det_arch="det",
        reco_arch="reco",
        auto_correct_orientation=False,
    )

    model = OnnxtrOcrModel(
        enabled=False,
        artifacts_path=None,
        options=options,
        accelerator_options=AcceleratorOptions(),
    )

    invalid_page = make_mock_page(valid=False)
    conv_res = MagicMock(spec=ConversionResult)
    result = list(model(conv_res, [invalid_page]))

    assert result == [invalid_page]
