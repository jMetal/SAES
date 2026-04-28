.PHONY: help install lint format format-check typecheck test coverage ci clean \
        release-dry-run release-stamp version branch

# ── Variables ────────────────────────────────────────────────
UV        := uv run
SRC_DIRS  := src/ tests/
BUMP      ?= minor
AUTHOR    ?=

# ── Default ──────────────────────────────────────────────────
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────
install: ## Install all dependencies (dev included)
	uv sync --dev

# ── Quality ──────────────────────────────────────────────────
lint: ## Run ruff linter
	$(UV) ruff check $(SRC_DIRS)

format: ## Auto-format code with ruff
	$(UV) ruff format $(SRC_DIRS)

format-check: ## Check formatting without modifying files
	$(UV) ruff format --check $(SRC_DIRS)

typecheck: ## Run mypy strict type-checking
	$(UV) mypy src/

test: ## Run pytest test suite
	$(UV) pytest tests/ -v

coverage: ## Run tests and generate HTML coverage report
	$(UV) pytest --cov=src/saes tests/ -v
	$(UV) coverage html
	@echo "Coverage report generated: htmlcov/index.html"

# ── CI (all quality gates) ───────────────────────────────────
ci: lint format-check typecheck test ## Run full CI pipeline (lint + format + types + tests)

# ── Release ──────────────────────────────────────────────────
version: ## Show current version from version.txt
	@cat version.txt

release-dry-run: ## Preview release stamp without modifying files
	@python3 scripts/release_stamp.py --dry-run --bump $(BUMP) $(if $(AUTHOR),--author $(AUTHOR),)

release-stamp: ## Stamp changelog and bump version (BUMP=major|minor|patch AUTHOR=@user)
	@python3 scripts/release_stamp.py --bump $(BUMP) $(if $(AUTHOR),--author $(AUTHOR),)

# ── Branching ────────────────────────────────────────────────
branch: ## Create a new branch with the correct version prefix (interactive)
	@echo ""; \
	echo "Select version bump type for this branch:"; \
	echo "  1) minor  (default — new feature, X.Y+1.0)"; \
	echo "  2) patch  (bugfix / hotfix, X.Y.Z+1)"; \
	echo "  3) major  (breaking change, X+1.0.0)"; \
	echo ""; \
	printf "Choice [1]: "; \
	read CHOICE; \
	case "$${CHOICE:-1}" in \
		1) PREFIX="feat" ;; \
		2) PREFIX="fix" ;; \
		3) PREFIX="major" ;; \
		*) echo "Invalid choice"; exit 1 ;; \
	esac; \
	echo ""; \
	printf "Branch name (e.g. add-visualization): "; \
	read NAME; \
	if [ -z "$$NAME" ]; then \
		echo "ERROR: branch name cannot be empty"; \
		exit 1; \
	fi; \
	BRANCH="$$PREFIX/$$NAME"; \
	echo ""; \
	echo "Creating branch: $$BRANCH"; \
	git checkout -b "$$BRANCH"; \
	echo ""; \
	echo "✅ Branch '$$BRANCH' created."; \
	echo "📝 Remember to add your changes to CHANGELOG.md under ## [Unreleased]"

# ── Cleanup ──────────────────────────────────────────────────
clean: ## Remove build artifacts and caches
	rm -rf .mypy_cache .pytest_cache .ruff_cache __pycache__ htmlcov .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
