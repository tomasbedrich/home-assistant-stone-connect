.PHONY: help install test lint format type-check clean build docs
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies for development
	uv sync --dev

lint: ## Run linting
	uv run ruff check custom_components

format: ## Format code
	uv run ruff format custom_components

type-check: ## Run type checking
	uv run mypy custom_components

check: lint type-check ## Run all checks (lint + type)

clean: ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info/
	rm -rf .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build the package
	uv build
