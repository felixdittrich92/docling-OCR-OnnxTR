<p align="center">
  <img src="https://github.com/felixdittrich92/OnnxTR/raw/main/docs/images/logo.jpg" width="40%">
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Test Status](https://github.com/felixdittrich92/docling-OCR-OnnxTR/actions/workflows/main.yml/badge.svg)](https://github.com/felixdittrich92/docling-OCR-OnnxTR/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/felixdittrich92/OnnxTR/graph/badge.svg?token=WVFRCQBOLI)](https://codecov.io/gh/felixdittrich92/OnnxTR)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d250447650240ee9ca573950fea8b99)](https://app.codacy.com/gh/felixdittrich92/docling-OCR-OnnxTR/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeFactor](https://www.codefactor.io/repository/github/felixdittrich92/docling-ocr-onnxtr/badge)](https://www.codefactor.io/repository/github/felixdittrich92/docling-ocr-onnxtr)
[![Pypi](https://img.shields.io/badge/pypi-v0.6.2-blue.svg)](https://pypi.org/project//)
![PyPI - Downloads](https://img.shields.io/pypi/dm/docling-ocr-onnxtr)

# docling-OCR-OnnxTR

docling plugin for OnnxTR OCR

## Installation

```bash
pip install docling-ocr-onnxtr[cpu] # for CPU
pip install docling-ocr-onnxtr[gpu] # for Nvidia GPU
pip install docling-ocr-onnxtr[openvino] # for Intel GPU / Integrated Graphics
pip install docling-ocr-onnxtr[cpu-headless] # for CPU without GUI
pip install docling-ocr-onnxtr[gpu-headless] # for Nvidia GPU without GUI
pip install docling-ocr-onnxtr[openvino-headless] # for Intel GPU / Integrated Graphics without GUI
```

## Usage

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    ConversionResult,
    DocumentConverter,
    InputFormat,
    PdfFormatOption,
)
from docling_ocr_onnxtr import OnnxtrOcrOptions


def main():
    # Source document to convert
    source = "https://arxiv.org/pdf/2408.09869v4"

    # Available detection & recognition models can be found at
    # https://github.com/felixdittrich92/OnnxTR

    # Or you choose a model from Hugging Face Hub
    # Collection: https://huggingface.co/collections/Felix92/onnxtr-66bf213a9f88f7346c90e842

    ocr_options = OnnxtrOcrOptions(
        # Text detection model
        det_arch="db_mobilenet_v3_large",
        # Text recognition model - from Hugging Face Hub
        reco_arch="Felix92/onnxtr-parseq-multilingual-v1",
        # This can be set to `True` to auto-correct the orientation of the pages
        auto_correct_orientation=False,
    )

    pipeline_options = PdfPipelineOptions(
        ocr_options=ocr_options,
    )
    pipeline_options.allow_external_plugins = True  # <-- enabled the external plugins

    # Convert the document
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            ),
        },
    )

    conversion_result: ConversionResult = converter.convert(source=source)
    doc = conversion_result.document
    md = doc.export_to_markdown()
    print(md)


if __name__ == "__main__":
    main()
```

## License

Distributed under the Apache 2.0 License. See [`LICENSE`](https://github.com/felixdittrich92/OnnxTR?tab=Apache-2.0-1-ov-file#readme) for more information.
