.PHONY: quality style test

# this target runs checks on all files
quality:
	ruff check .
	mypy docling_ocr_onnxtr/

# this target runs checks on all files and potentially modifies some of them
style:
	ruff format .
	ruff check --fix .

# Run tests for the library
# NOTE: We download docling related files from the docling repo - in this case we can verify to be always up to date
test:
	# Download the testing files from the docling repo
	curl -L https://raw.githubusercontent.com/docling-project/docling/main/tests/verify_utils.py -o tests/verify_utils.py
	curl -L https://raw.githubusercontent.com/docling-project/docling/main/tests/test_data_gen_flag.py -o tests/test_data_gen_flag.py

	# Download the testing documents directly from the docling/tests folder
	rm -rf temp_repo
	git clone --filter=blob:none --no-checkout https://github.com/docling-project/docling.git temp_repo
	cd temp_repo && git sparse-checkout init --cone
	cd temp_repo && git sparse-checkout set tests/data_scanned
	cd temp_repo && git checkout main  # <-- This is the missing piece
	mkdir -p tests/data_scanned
	cp -r temp_repo/tests/data_scanned/* tests/data_scanned/
	rm -rf temp_repo

	coverage run -m pytest tests/ -rs
	coverage report --fail-under=80 --show-missing
