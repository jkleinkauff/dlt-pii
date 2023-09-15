SHELL := /bin/bash

# Include the environment variables by running the script
include env.sh

cleanpipe:
	@echo "Removing directory: $(DIR_HIDDEN_DLT_PIPE_PATH)"
	@rm -rf $(DIR_HIDDEN_DLT_PIPE_PATH)
	@echo "Removing directory: $(DIR_LOCAL_EXTRACTED_DATA)"
	@rm -rf $(DIR_LOCAL_EXTRACTED_DATA)