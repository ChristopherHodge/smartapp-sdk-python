SHELL       := /bin/bash
PYTHON       = python3
PYTHON_PATH  = .python/$(PYTHON_PACKAGE)
PYTHON_BIN   = $(PYTHON_PATH)/bin
PIP          = $(PYTHON_BIN)/pip
PYTEST       = IS_TEST=1 $(PYTHON_BIN)/pytest
TESTS        = ./tests/test_*.py
NO_CACHE     = PYTHONDONTWRITEBYTECODE=1
WITH_VERSION = BUILD_VERSION=$(BUILD_VERSION)
DOT          = .

BUILD_VERSION := $(shell git describe --always --tags)

PACKAGE_VERSION = ${BUILD_VERSION}

all: wheel

.PHONY: venv dev test build clean clean_build clean_dist

.python:
	[ -d $(PYTHON_PATH) ] || \
		$(shell which $(PYTHON_VERSION) || which $(PYTHON)) -m venv $(PYTHON_PATH)
	$(DOT) $(PYTHON_BIN)/activate

venv: .python

.dev_install: .python
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch .dev_install

dev: .dev_install

.install: .dev_install
	$(WITH_VERSION) $(PIP) install --no-cache-dir --editable $(DOT)
	@touch .install

install: .install

test: .install
	$(PYTEST) $(TESTS)

build_wheel: dev
	$(WITH_VERSION) $(PIP) wheel --wheel-dir=dist --no-deps $(DOT)

build: build_wheel

clean_egg:
	rm -rf *.egg-info

wheel: build_wheel clean_egg

clean_dist:
	rm -rf dist

clean_build: clean_egg
	rm -rf $(PYTHON_PATH) .pytest_cache build

clean: clean_egg clean_build clean_dist
	rm -rf .install .dev_install .python

