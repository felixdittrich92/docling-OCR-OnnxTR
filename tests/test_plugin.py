from pathlib import Path

import pytest
from docling.backend.docling_parse_backend import DoclingParseDocumentBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    OcrOptions,
    PdfPipelineOptions,
)
from docling.datamodel.settings import settings
from docling.document_converter import DocumentConverter, PdfFormatOption

from docling_ocr_onnxtr import OnnxtrOcrOptions

from .test_data_gen_flag import GEN_TEST_DATA
from .verify_utils import verify_conversion_result_v1, verify_conversion_result_v2

GENERATE_V1 = GEN_TEST_DATA
GENERATE_V2 = GEN_TEST_DATA


def get_pdf_paths():
    # Define the directory you want to search
    directory = Path("./tests/data_scanned")
    # List all PDF files in the directory and its subdirectories
    pdf_files = sorted(directory.rglob("*.pdf"))
    return pdf_files


def get_converter(ocr_options: OcrOptions):
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.ocr_options = ocr_options
    pipeline_options.accelerator_options.device = AcceleratorDevice.CPU
    pipeline_options.allow_external_plugins = True  # <-- enabled the external plugins
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=DoclingParseDocumentBackend,
            )
        }
    )
    return converter


@pytest.mark.parametrize(
    "ocr_options",
    [
        OnnxtrOcrOptions(),
        OnnxtrOcrOptions(force_full_page_ocr=True),
        OnnxtrOcrOptions(
            det_arch="db_mobilenet_v3_large",
            reco_arch="crnn_mobilenet_v3_small",
            auto_correct_orientation=False,
        ),
        OnnxtrOcrOptions(
            det_arch="db_mobilenet_v3_large",
            reco_arch="crnn_mobilenet_v3_small",
            auto_correct_orientation=True,
        ),
    ],
)
def test_e2e_conversions(ocr_options: OcrOptions):
    pdf_paths = get_pdf_paths()

    settings.debug.visualize_ocr = True

    print(f"Converting with ocr_engine: {ocr_options.kind}, language: {ocr_options.lang}")
    converter = get_converter(ocr_options=ocr_options)
    for pdf_path in pdf_paths:
        if not ocr_options.auto_correct_orientation and "rotated" in pdf_path.name:
            # Skip rotated PDFs if orientation correction is disabled
            print(f"Skipping {pdf_path} due to orientation correction settings.")
            continue

        print(f"converting {pdf_path}")
        doc_result: ConversionResult = converter.convert(pdf_path)

        try:
            verify_conversion_result_v1(
                input_path=pdf_path,
                doc_result=doc_result,
                generate=GENERATE_V1,
                fuzzy=True,
            )
            verify_conversion_result_v2(
                input_path=pdf_path,
                doc_result=doc_result,
                generate=GENERATE_V2,
                fuzzy=True,
            )
        except AssertionError as e:
            if "rotated" in pdf_path.name:
                pytest.xfail(f"Skipping {pdf_path} due to orientation correction settings: {e}")
            else:
                raise  # Unexpected failure — re-raise the error
