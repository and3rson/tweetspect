PYTHON = .venv/bin/python

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run:  ## Run in docker
	docker-compose up --build

.PHONY: venv
init: ## Initialize virtual env & install requirements
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements/dev.txt

.PHONY: licenses
licenses: ## Print licenses of used packages
	$(PYTHON) -m piplicenses

.PHONY: check
check: lint metrics test ## Run code checks

.PHONY: lint
lint: ## Check code style
	$(PYTHON) -m pylint tweetspect

.PHONY: cc
metrics: ## Check cyclomatic complexity & code maintability
	$(PYTHON) -m radon cc tweetspect
	$(PYTHON) -m radon mi tweetspect

.PHONY: test
test: ## Run unit tests
	$(PYTHON) -m pytest tweetspect --doctest-modules --verbose -x --cov=. --cov-report html
