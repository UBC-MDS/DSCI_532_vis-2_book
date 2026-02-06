.PHONY: setup-quarto
setup-quarto:
	quarto add --no-prompt coatless-quarto/embedio && \
	quarto add --no-prompt gadenbuie/countdown/quarto && \
	quarto add --no-prompt quarto-ext/shinylive && \
	quarto add --no-prompt shafayetShafee/line-highlight

.PHONY: setup-python
setup-python:
	rm -rf venv .venv
	uv venv venv
	source venv/bin/activate && uv pip install -r requirements.txt

.PHONY: preview
preview:
	rm -rf _site .quarto
	quarto preview
