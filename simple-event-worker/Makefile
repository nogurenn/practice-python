VENV_DIR := ../venv/simple-event-worker
PYTHON := $(VENV_DIR)/bin/python3
PIP := $(VENV_DIR)/bin/pip3
REQ_FILE := requirements.txt

venv:
	@echo "Creating simple-event-worker venv"
	@python3 -m venv $(VENV_DIR)
	@echo "Installing requirements"
	@$(PIP) install -r $(REQ_FILE)
	@echo "Venv created"
.PHONY: venv

freeze:
	@echo "Freezing requirements"
	@$(PIP) freeze > $(REQ_FILE)
	@echo "Requirements frozen"
.PHONY: freeze

test:
	@$(PYTHON) -m unittest discover -s . -p "*_test.py"
.PHONY: test

run:
	@$(PYTHON) main.py
.PHONY: run
