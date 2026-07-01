.PHONY: env lint repro clean shots manifest

export PLAYWRIGHT_BROWSERS_PATH := /mnt/projects/.playwright-browsers

shots:
	uv run python tools/screenshot.py --all

manifest:
	uv run python tools/build_manifest.py

env:
	uv sync

lint:
	@echo "Run the /lint skill in Claude Code for full checks."
	@grep -rIl --include='*.md' '\[\[' . | head -20 || true

repro:
	dvc repro

clean:
	rm -rf .venv __pycache__ .pytest_cache
