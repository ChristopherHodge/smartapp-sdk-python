PYTHON_VERSION = python3.9
PYTHON_PACKAGE = smartapp-sdk
PYTHON_MODULE  = smartapp

include wheel.mk

doc: install
	$(PYTHON_BIN)/pdoc --html $(PYTHON_MODULE)
