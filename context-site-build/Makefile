PYTHON ?= python3
META   := ../context-meta-pipeline

.PHONY: help verify validate audit lint typecheck install-deps clean coverage-check snapshot-diff

help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk -F':.*?##' '{printf "  %-22s %s\n", $$1, $$2}'

verify: ## Run verify.sh — full self-check
	@./verify.sh

validate: ## Validate every live SKILL.md (uses meta-pipeline scripts)
	@$(PYTHON) $(META)/scripts/validate-metadata.py --all

audit: ## Run audit-skill on every live skill (uses meta-pipeline scripts)
	@$(PYTHON) $(META)/scripts/audit-skill.py --all

coverage-check: ## Validate coverage.md schema
	@$(PYTHON) $(META)/scripts/coverage-check.py --file coverage.md

snapshot-diff: ## Diff two SNAPSHOT.lock states (requires --old + --new args)
	@$(PYTHON) $(META)/scripts/snapshot-diff.py $(ARGS)

install-deps: ## Install runtime dependencies
	@$(PYTHON) -m pip install -r requirements.txt

clean: ## Remove generated artifacts
	@find . -type d \( -name '__pycache__' -o -name '.mypy_cache' -o -name '.ruff_cache' \) -exec rm -rf {} + 2>/dev/null || true
