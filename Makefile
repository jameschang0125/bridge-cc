SHELL := /bin/bash
.DEFAULT_GOAL := all
.NOTPARALLEL:

PYTHON ?= python
DOCS := main opening conventions principles defensive summary
TEX_TMP := tex-tmp
TEX_RESULT := tex-result
BOOK_DIR := tex-book
LOG_DIR := $(TEX_TMP)/log

.PHONY: all clean prepare gen $(DOCS)

all: $(DOCS)
	@echo "compile done"

gen:
	rm -f $(BOOK_DIR)/*.tex
	cd src && $(PYTHON) gen.py

prepare: gen
	rm -rf $(TEX_TMP)
	mkdir -p $(TEX_TMP)
	cp -r tex $(TEX_TMP)
	cp -r $(BOOK_DIR) $(TEX_TMP)
	mkdir -p $(LOG_DIR)
	mkdir -p $(TEX_RESULT)

$(DOCS): prepare
	@doc="$@.tex"; \
	pdf="$${doc%.tex}.pdf"; \
	echo; \
	echo "===== compiling $$doc ====="; \
	cd "$(TEX_TMP)/$(BOOK_DIR)" || exit 1; \
	echo X | time xelatex --halt-on-error "$$doc" > "../log/$$doc.log1"; \
	if (( $$? )); then \
		echo "error when compiling $$doc, exiting..."; \
		cat "../log/$$doc.log1"; \
		exit 1; \
	fi; \
	echo X | time xelatex --halt-on-error "$$doc" > "../log/$$doc.log2"; \
	if (( $$? )); then \
		echo "error when compiling $$doc, exiting..."; \
		cat "../log/$$doc.log2"; \
		exit 1; \
	fi; \
	echo X | time xelatex --halt-on-error "$$doc" > "../log/$$doc.log3"; \
	if (( $$? )); then \
		echo "error when compiling $$doc, exiting..."; \
		cat "../log/$$doc.log3"; \
		exit 1; \
	fi; \
	cp "$$pdf" "../../$(TEX_RESULT)/"

clean:
	rm -rf $(TEX_TMP)
