setup:
	@echo "Creating directory of venvs"
	@mkdir -p venv
.PHONY: setup


venvSimpleEventWorker:
	@echo "Setting up simple-event-worker venv"
	@(cd simple-event-worker && make venv)
.PHONY: venvSimpleEventWorker

runSimpleEventWorker:
	@echo "Running SimpleEventWorker"
	@(cd simple-event-worker && make run)
	@echo "SimpleEventWorker finished"
.PHONY: runSimpleEventWorker
