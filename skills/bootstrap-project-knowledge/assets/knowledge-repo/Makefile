.PHONY: lint status

UV_CACHE_DIR ?= .uv-cache
export UV_CACHE_DIR

lint:
	uv run python scripts/check_knowledge.py

status:
	uv run python scripts/knowledge_status.py
