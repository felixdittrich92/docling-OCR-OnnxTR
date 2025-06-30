<p align="center">
  <img src="https://github.com/felixdittrich92/docling-OCR-OnnxTR/raw/main/docs/images/onnxtr_docling_merged.png" width="40%">
</p>

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Build Status](https://github.com/felixdittrich92/docling-OCR-OnnxTR/actions/workflows/builds.yml/badge.svg)](https://github.com/felixdittrich92/docling-OCR-OnnxTR/actions/workflows/builds.yml)
[![codecov](https://codecov.io/gh/felixdittrich92/docling-OCR-OnnxTR/graph/badge.svg?token=L3AHXKV86A)](https://codecov.io/gh/felixdittrich92/docling-OCR-OnnxTR)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0d250447650240ee9ca573950fea8b99)](https://app.codacy.com/gh/felixdittrich92/docling-OCR-OnnxTR/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![CodeFactor](https://www.codefactor.io/repository/github/felixdittrich92/docling-ocr-onnxtr/badge)](https://www.codefactor.io/repository/github/felixdittrich92/docling-ocr-onnxtr)
[![Pypi](https://img.shields.io/badge/pypi-v0.2.0-blue.svg)](https://pypi.org/project/docling-ocr-onnxtr/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/docling-ocr-onnxtr)

The `docling-OCR-OnnxTR` repository provides a plugin that integrates the [OnnxTR OCR engine](https://github.com/felixdittrich92/OnnxTR) into the [Docling framework](https://github.com/docling-project/docling), enhancing document processing capabilities with efficient and accurate text recognition.

**Key Features:**

- **Seamless Integration:** Easily incorporate OnnxTR's OCR functionalities into your Docling workflows for improved document parsing and analysis.

- **Optimized Performance:** Leverages OnnxTR's lightweight architecture to deliver faster inference times and reduced resource consumption compared to traditional OCR engines.

- **Flexible Deployment:** Supports various hardware configurations, including CPU, GPU, and OpenVINO, allowing you to choose the best setup for your needs.

**Installation:**

To install the plugin, use one of the following commands based on your hardware:

For GPU support please take a look at: [ONNX Runtime](https://onnxruntime.ai/getting-started).

- **Prerequisites:** CUDA & cuDNN needs to be installed before [Version table](https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html).

```bash
# For CPU
pip install "docling-ocr-onnxtr[cpu]"
# For Nvidia GPU
pip install "docling-ocr-onnxtr[gpu]"
# For Intel GPU / Integrated Graphics
pip install "docling-ocr-onnxtr[openvino]"

# Headless mode (no GUI)
# For CPU
pip install "docling-ocr-onnxtr[cpu-headless]"
# For Nvidia GPU
pip install "docling-ocr-onnxtr[gpu-headless]"
# For Intel GPU / Integrated Graphics
pip install "docling-ocr-onnxtr[openvino-headless]"
```

By integrating OnnxTR with Docling, users can achieve more efficient and accurate OCR results, enhancing the overall document processing experience.

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

It is also possible to load the models from local files instead of using the Hugging Face Hub or downloading them from the repo:

```python
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    ConversionResult,
    DocumentConverter,
    InputFormat,
    PdfFormatOption,
)
from docling_ocr_onnxtr import OnnxtrOcrOptions
from onnxtr.models import db_mobilenet_v3_large, parseq


def main():
    # Source document to convert
    source = "https://arxiv.org/pdf/2408.09869v4"

    # Load models from local files
    # NOTE: You need to download the models first and then adjust the paths accordingly.
    det_model = db_mobilenet_v3_large("/home/felix/.cache/onnxtr/models/db_mobilenet_v3_large-1866973f.onnx")
    reco_model = parseq("/home/felix/.cache/onnxtr/models/parseq-00b40714.onnx")

    ocr_options = OnnxtrOcrOptions(
        # Text detection model
        det_arch=det_model,
        # Text recognition model
        reco_arch=reco_model,
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

## Configuration

The configuration of the OCR engine is done via the `OnnxtrOcrOptions` class. The following options are available:

- `lang`: List of languages to use for OCR. Default is `["en", "fr"]`.
- `confidence_score`: Word confidence threshold for the recognition model. Default is `0.5`.
- `objectness_score`: Detection model objectness score threshold. Default is `0.3`.
- `det_arch`: Detection model architecture. Default is `"fast_base"`.
- `reco_arch`: Recognition model architecture. Default is `"crnn_vgg16_bn"`.
- `reco_bs`: Batch size for the recognition model. Default is `512`.
- `auto_correct_orientation`: Whether to auto-correct the orientation of the pages. Default is `False`.
- `preserve_aspect_ratio`: Whether to preserve the aspect ratio of the images. Default is `True`.
- `symmetric_pad`: Whether to use symmetric padding. Default is `True`.
- `paragraph_break`: Paragraph break threshold. Default is `0.035`.
- `load_in_8_bit`: Whether to load the model in 8-bit. Default is `False`. (Not supported for Hugging Face loaded models yet)
- `providers`: List of providers to use for the Onnxruntime. Default is `None` which means auto-select.
- `session_options`: Session options for the Onnxruntime. Default is `None` which means default OnnxTR session options.

Available Hugging Face models can be found at [Hugging Face](https://huggingface.co/collections/Felix92/onnxtr-66bf213a9f88f7346c90e842).

**Further information:**

Please take a look at [OnnxTR](https://github.com/felixdittrich92/OnnxTR).

## Contributing

Contributions are welcome!

Before opening a pull request, please ensure that your code passes the tests and adheres to the project's coding standards.

You can run the tests and checks using:

```bash
make style
make quality
make test
```

## License

Distributed under the Apache 2.0 License. See [`LICENSE`](https://github.com/felixdittrich92/OnnxTR?tab=Apache-2.0-1-ov-file#readme) for more information.
