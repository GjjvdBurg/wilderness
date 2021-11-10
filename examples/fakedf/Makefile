# Makefile for easier installation and cleanup.
#
# Uses self-documenting macros from here:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

PACKAGE=fakedf

.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |\
		 awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m\
		 %s\n", $$1, $$2}'

################
# Installation #
################

.PHONY: install

install: dist ## Install for the current user using the default python command
	pip install --user ./dist/*.whl

################
# Distribution #
################

.PHONY: dist

dist: man ## Make Python source distribution
	python setup.py build_ext --inplace && \
		python setup.py sdist bdist_wheel

###########
# Testing #
###########

.PHONY: test mypy

test: venv ## Run unit tests
	source $(VENV_DIR)/bin/activate && green -vv -s 1 -a ./tests

mypy: venv ## Run mypy
	source $(VENV_DIR)/bin/activate && \
	       	mypy --check-untyped-defs ./stubs $(PACKAGE)

#################
# Documentation #
#################

.PHONY: man clean_man

man: ## Build documentation with Sphinx
	python setup.py build_manpages

clean_man: ## Remove man pages
	rm -f ./man/*

############
# Clean up #
############

.PHONY: clean

clean: clean_man ## Clean build dist and egg directories left after install
	rm -rf ./dist
	rm -rf ./build
	rm -rf ./cover
	rm -rf ./$(PACKAGE).egg-info
	rm -f MANIFEST
	rm -f ./$(PACKAGE)/*.so
	rm -f ./*_valgrind.log*
	find . -type f -iname '*.pyc' -delete
	find . -type d -name '__pycache__' -empty -delete
