ENVIRONMENT="."$(shell basename $(PWD))
PYTHON=python3

######################################################################
# Basic commands
######################################################################
show:
	@echo "Python command: $(PYTHON)"
	@$(PYTHON) --version
	@echo "Environment: $(ENVIRONMENT)"

environment:
	@if [ ! -d "$(ENVIRONMENT)" ]; then \
		echo "Creating python environment..."; \
		$(PYTHON) -m venv $(ENVIRONMENT); \
	else \
		echo "Environment $(ENVIRONMENT) already exists..."; \
	fi

install:environment
	@echo "Installing editable..."
	@$(ENVIRONMENT)/bin/pip install -e .

clean:
	@echo "Cleaning crap"
	@-find . -name "*~" -exec rm {} \;
	@-find . -name "#*#" -exec rm -rf {} \;
	@-find . -name ".DS_Store" -exec rm -rf {} \;

cleanall:
	@echo "Cleaning python"
	@-find . -name "__pycache__" -path "$(ENVIRONMENT)" -prune -exec rm -rf {} \;
	@-find . -name "*.pyc" -exec rm -rf {} \;

pack:
	@echo "Packing data..."
	@sh .pack/pack.sh pack

unpack:
	@echo "Unpacking data..."
	@bash .pack/pack.sh unpack

######################################################################
# Git commands
######################################################################
commit:
	@echo "Commiting changes..."
	@-git commit -am "[FIX] Some fixes"
	@git push

pull:
	@echo "Pulling from repository..."
	@git reset --hard HEAD	
	@git pull
	
prune:
	@echo "Prunning (cleaning all temporary files)"
	@-git gc --aggressive --prune

######################################################################
# Package specifics
######################################################################

