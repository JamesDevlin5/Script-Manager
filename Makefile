
RUNNER=python3
FORMATTER=black
TEST_RUNNER=pytest

SRC_DIR=script_manager
MAIN_FILE=$(SRC_DIR)/manager.py

default:
	@echo "Nothing to do..."

run:
	$(RUNNER) $(MAIN_FILE)

fmt:
	$(FORMATTER) $(SRC_DIR)

test:
	$(TEST_RUNNER) $(TEST_DIR)

.PHONY: default fmt test
