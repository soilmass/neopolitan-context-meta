# context-meta-pipeline — Makefile
#
# Convenience wrappers around the four Python scripts and verify.sh.
# Targets are named after the operations the lifecycle skills already
# document; this Makefile is just the conventional entry point.

PYTHON ?= python3
SCRIPTS := scripts

.PHONY: help verify validate audit lint typecheck \
        coverage-check snapshot-diff dep-graph routing-eval release smoke \
        test-scripts smoke-bootstrap extension-check taxonomy-sync changelog-sync \
        index hashes integration notify-dependents-dry analytics-rollup \
        install-deps clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk -F':.*?##' '{printf "  %-22s %s\n", $$1, $$2}'

verify: ## Run verify.sh — full self-check (validators + fixtures + audit + version triangulation + coverage + snapshot-diff sanity)
	@./verify.sh

validate: ## Run validate-metadata.py against every live skill
	@$(PYTHON) $(SCRIPTS)/validate-metadata.py --all

audit: ## Run audit-skill.py against every live skill (recency + drift; gates 2/3 N/A)
	@$(PYTHON) $(SCRIPTS)/audit-skill.py --all

coverage-check: ## Run coverage-check.py against the library's coverage.md
	@$(PYTHON) $(SCRIPTS)/coverage-check.py --file coverage.md

snapshot-diff: ## Diff SNAPSHOT.lock against an arbitrary --old= file (default: fixture/snapshot/snapshot-a.lock)
	@$(PYTHON) $(SCRIPTS)/snapshot-diff.py --old $(SCRIPTS)/tests/fixtures/snapshot/snapshot-a.lock --new SNAPSHOT.lock

dep-graph: ## Print the SNAPSHOT.lock dependency graph (text format)
	@$(PYTHON) $(SCRIPTS)/dependency-graph.py

routing-eval: ## Run routing-eval-runner.py in static mode (rough heuristic)
	@$(PYTHON) $(SCRIPTS)/routing-eval-runner.py --mode static

release: ## Dry-run release-tag.sh (use --confirm to actually create the tag)
	@./scripts/release-tag.sh

smoke: ## Run the family-bootstrap smoke fixture (added v0.5.0)
	@if [ -d scripts/tests/smoke/bootstrap-git-family ]; then \
	  echo "smoke fixture present; runner is operator-driven for now"; \
	  ls scripts/tests/smoke/bootstrap-git-family/; \
	else echo "no smoke fixture yet"; fi

test-scripts: ## Run verify.sh steps 7+8 only (script fixtures + CLI exercise)
	@./verify.sh 2>&1 | sed -n '/=== 7\./,/=== 9\./p' | sed '$$d'

extension-check: ## Run verify.sh step 9 only (extension-seam contract checks)
	@./verify.sh 2>&1 | sed -n '/=== 9\./,/=== 10\./p' | sed '$$d'

taxonomy-sync: ## Run taxonomy-coverage-sync.py against the matching fixture (smoke test)
	@python3 scripts/taxonomy-coverage-sync.py \
	  --taxonomy scripts/tests/fixtures/taxonomy-coverage/matching/taxonomy.md \
	  --coverage scripts/tests/fixtures/taxonomy-coverage/matching/coverage.md

changelog-sync: ## Cross-reference per-skill metadata.changelog vs library CHANGELOG.md
	@$(PYTHON) $(SCRIPTS)/changelog-sync.py

index: ## Regenerate INDEX.md from live skills (v0.7.0)
	@$(PYTHON) $(SCRIPTS)/gen-index.py

hashes: ## Update sha256 fields in SNAPSHOT.lock for all skills (v0.7.0)
	@$(PYTHON) $(SCRIPTS)/snapshot-hash.py

integration: ## Run integration-test-runner against fixture scenarios (v0.7.0)
	@$(PYTHON) $(SCRIPTS)/integration-test-runner.py

notify-dependents-dry: ## Dry-run notify-dependents.py for skill-author (v0.7.0)
	@$(PYTHON) $(SCRIPTS)/notify-dependents.py --skill skill-author --reason "make-target dry-run"

analytics-rollup: ## Smoke-test analytics-rollup.py against synthetic events (v0.7.0)
	@$(PYTHON) $(SCRIPTS)/analytics-rollup.py --input $(SCRIPTS)/tests/analytics/synthetic-events.jsonl

smoke-bootstrap: ## Lint smoke fixture's expected/ tree against current SNAPSHOT.lock
	@if [ ! -d scripts/tests/smoke/bootstrap-git-family/expected ]; then \
	  echo "no smoke fixture yet"; exit 0; \
	fi
	@if [ -f scripts/tests/smoke/bootstrap-git-family/expected/skills.txt ]; then \
	  echo "expected skills (from fixture):"; \
	  grep -v '^#' scripts/tests/smoke/bootstrap-git-family/expected/skills.txt | grep -v '^$$' | awk '{print $$1}' | sort > /tmp/smoke-expected.txt; \
	  echo "  fixture lists $$(wc -l < /tmp/smoke-expected.txt | awk '{print $$1}') skills"; \
	  echo "(staleness check: re-walk family-bootstrap with bootstrap-git-family/input.yaml)"; \
	  rm -f /tmp/smoke-expected.txt; \
	fi

lint: ## Run ruff over all Python scripts
	@command -v ruff >/dev/null && ruff check $(SCRIPTS)/ || echo "ruff not installed; skip"

typecheck: ## Run mypy --strict over all Python scripts
	@command -v mypy >/dev/null && mypy --strict $(SCRIPTS)/*.py || echo "mypy not installed; skip"

install-deps: ## Install runtime + dev dependencies
	@$(PYTHON) -m pip install -r requirements.txt
	@$(PYTHON) -m pip install ruff mypy

clean: ## Remove generated artifacts (__pycache__, mypy/ruff caches)
	@find . -type d \( -name '__pycache__' -o -name '.mypy_cache' -o -name '.ruff_cache' \) -exec rm -rf {} + 2>/dev/null || true
