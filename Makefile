.PHONY: env init tests shell

# Setup the environment. Installs Python, git, and make.
# Assumes DevBox is installed.
env:
	devbox shell

# Create a project specific Python virtual environment, upgrade pip, and install dependencies in the venv.
init:
	@( \
	set -e ; \
	python -m venv ./.venv; \
	source .venv/bin/activate; \
	python -m ensurepip --upgrade; \
	python -m pip install --upgrade pip; \
	pip install .; \
	)

tests:
	@( \
	source .venv/bin/activate; \
	python -m pytest; \ 
	)

shell:
	@( \
	source .venv/bin/activate; \
	bpython; \
	)

