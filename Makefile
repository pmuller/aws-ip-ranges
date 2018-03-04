# Project configuration
PROJECT_NAME = aws-ip-ranges
PACKAGE_NAME = aws_ip_ranges
TESTS_DIRECTORY = tests
VIRTUALENV_DIR = ${CURDIR}/.env

# Call these functions before/after each target to maintain a coherent display
START_TARGET = @printf "[$(shell date +"%H:%M:%S")] %-40s" "$(1)"
END_TARGET = @printf "\033[32;1mOK\033[0m\n"

# Parameter expansion
PYTEST_OPTS ?=

ENV_RUN =

.PHONY: help check_code_style check_doc_style check_pylint check_xenon \
        check_lint check_test check clean dist \
        env ci_check

help: ## Display list of targets and their documentation
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
		'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

check_code_style: ## Check code style
	$(call START_TARGET,Checking code style)
	@$(ENV_RUN) pycodestyle $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_doc_style: ## Check documentation style
	$(call START_TARGET,Checking doc style)
	@$(ENV_RUN) pydocstyle $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_pylint: ## Run pylint
	$(call START_TARGET,Checking pylint)
	@$(ENV_RUN) pylint --reports=no --jobs=2 $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_xenon: ## Run xenon (code complexity)
	$(call START_TARGET,Checking xenon)
	@$(ENV_RUN) xenon $(PACKAGE_NAME) --no-assert
	$(call END_TARGET)

check_lint: check_code_style check_doc_style check_pylint check_xenon ## Check code style, documentation style, pylint and xenon

check_test: ## Run py.test
	$(call START_TARGET,Checking $(TESTS_DIRECTORY))
	@$(ENV_RUN) py.test --cov=$(PACKAGE_NAME) --cov-fail-under=0 --duration=10 $(PYTEST_OPTS) $(TESTS_DIRECTORY)

check: check_lint check_test ## Run all checks (lint and tests)

clean: ## Remove temporary and build files
	$(call START_TARGET,Cleaning)
	@find . -type f -name '*.pyc' -delete
	@rm -rf dist/ .cache .eggs
	@rm -rf htmlcov .coverage junit.xml coverage.xml
	@rm -rf *.egg-info
	@rm -rf $(VIRTUALENV_DIR)
	@rm -rf .pytest_cache/
	$(call END_TARGET)

dist: ## Create a source distribution
	$(call START_TARGET,Creating distribution)
	@$(ENV_RUN) python setup.py --quiet sdist --dist-dir _tmp_dist
	@mkdir -p dist
	@mv _tmp_dist/*.tar.gz dist/$(PROJECT_NAME)-$$(git describe).tar.gz
	@rm -rf _tmp_dist
	$(call END_TARGET)

env: $(VIRTUALENV_DIR) ## Build a development environment

ci_env: clean env ## Build a clean environment for CI

$(VIRTUALENV_DIR):
	virtualenv --system-site-packages $(VIRTUALENV_DIR)
	$(VIRTUALENV_DIR)/bin/pip install -U pip setuptools wheel
	$(VIRTUALENV_DIR)/bin/pip install -r ${CURDIR}/requirements/tests.txt
	$(VIRTUALENV_DIR)/bin/pip install -e ${CURDIR}

ci_check: ci_env ## Run all checks in the CI environment
	bash -c ". $(VIRTUALENV_DIR)/bin/activate && $(MAKE) -f Makefile check \
	PYTEST_OPTS='-vv --junit-xml=junit.xml --cov $(PACKAGE_NAME) \
				--cov-report xml:${CURDIR}/coverage.xml'"
