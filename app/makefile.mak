# Variables
VENV_DIR = ../venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
STREAMLIT = $(VENV_DIR)/bin/streamlit

# Default target
all: setup run

# Create virtual environment
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Install dependencies
install: $(VENV_DIR)
	$(PIP) install -r ../app/requirements.txt

# Run the Streamlit app
run: install
	$(STREAMLIT) run ../app/main.py

# Clean up temporary files
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type d -name '.ipynb_checkpoints' -exec rm -r {} +
	rm -rf $(VENV_DIR)

# Set up the environment (create virtual environment and install dependencies)
setup: install

# Show help
help:
	@echo "Usage:"
	@echo "  make all       - Set up the environment and run the Streamlit app"
	@echo "  make setup     - Set up the environment (create virtual environment and install dependencies)"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the Streamlit app"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make help      - Show this help message"

.PHONY: all install run clean setup help