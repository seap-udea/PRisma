# PRisma — repository maintenance
#
#   make clean   remove caches and other regenerable junk
#                (keeps .venv/, versioned pipeline results/, papers/)

.PHONY: clean

clean:
	@echo "Cleaning Python / Jupyter / OS junk…"
	@find . \
		\( -path './.git' -o -path './.git/*' -o -path './.venv' -o -path './.venv/*' -o -path './venv' -o -path './venv/*' \) -prune \
		-o \( -type d \( \
			-name '__pycache__' -o \
			-name '.ipynb_checkpoints' -o \
			-name '.pytest_cache' -o \
			-name '.mypy_cache' -o \
			-name '.ruff_cache' -o \
			-name 'tmp' -o \
			-name '.tmp' \
		\) -print \) \
		| tee /dev/stderr \
		| while IFS= read -r d; do rm -rf "$$d"; done
	@find . \
		\( -path './.git' -o -path './.git/*' -o -path './.venv' -o -path './.venv/*' -o -path './venv' -o -path './venv/*' \) -prune \
		-o \( -type f \( \
			-name '*.py[cod]' -o \
			-name '*$$py.class' -o \
			-name '.DS_Store' -o \
			-name 'Thumbs.db' -o \
			-name 'desktop.ini' -o \
			-name '*.swp' -o \
			-name '*~' \
		\) -print -delete \)
	@echo "Done."
