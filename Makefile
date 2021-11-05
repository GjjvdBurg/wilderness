# Makefile for easier installation and cleanup.
#
# Uses self-documenting macros from here:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

PACKAGE=wilderness
DOC_DIR='./docs/'
VENV_DIR=/tmp/wilderness_venv/

.PHONY: help dist venv

.DEFAULT_GOAL := help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		 awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m\
		 %s\n", $$1, $$2}'

################
# Installation #
################

.PHONY: install

install: ## Install for the current user using the default python command
	python setup.py build_ext --inplace && \
		python setup.py install --user

################
# Distribution #
################

.PHONY: release dist

release: ## Make a release
	python make_release.py

dist: ## Make Python source distribution
	python setup.py sdist

###########
# Testing #
###########

.PHONY: test integration integration_partial

test: venv ## Run unit tests
	source $(VENV_DIR)/bin/activate && green -vv -s 1 -a ./tests

#################
# Documentation #
#################

.PHONY: man

man: ## Build documentation with Sphinx
	python setup.py build_manpages

#######################
# Virtual environment #
#######################

.PHONY: venv clean_venv

venv: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	test -d $(VENV_DIR) || python -m venv $(VENV_DIR)
	source $(VENV_DIR)/bin/activate && pip install -e .[dev]
	touch $(VENV_DIR)/bin/activate

clean_venv:
	rm -rf $(VENV_DIR)

############
# Clean up #
############

.PHONY: clean

clean: clean_venv ## Clean build dist and egg directories left after install
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./$(PACKAGE).egg-info
	rm -rf ./cover
	rm -f MANIFEST
	rm -f ./$(PACKAGE)/*.so
	rm -f ./*_valgrind.log*
	find . -type f -iname '*.pyc' -delete
	find . -type d -name '__pycache__' -empty -delete