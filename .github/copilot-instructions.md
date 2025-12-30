# Copilot Instructions for amzsc

## Repository Overview

**amzsc** is a Python library for scraping Amazon product data using Selenium WebDriver. It supports multiple Amazon marketplaces (US, UK, DE, FR, ES, IT) and provides multi-threaded scraping capabilities with optional proxy support.

**Project Type**: Python package/library
**Size**: ~200KB of source code across 15 Python files (~500 lines total)
**Languages**: Python 3.9+
**Framework**: Selenium 4.x for web scraping, setuptools for packaging
**Package Manager**: uv (modern Python package manager)

## Build System & Environment Setup

### Prerequisites
- Python 3.9 or higher (specified in `.python-version` and `pyproject.toml`)
- uv package manager (install via: `pip install uv`)
- Chrome/Chromium browser (required for Selenium tests, but not for builds/linting)

### Initial Setup
**Always run this first when working with the repository:**
```bash
uv sync
```

This command:
- Creates a virtual environment in `.venv/`
- Installs all dependencies from `uv.lock` (including dev dependencies)
- Builds and installs the local `amzsc` package
- Takes approximately 30-60 seconds on first run

**Note**: `uv sync` must be run before any other commands (build, test, lint) to ensure dependencies are available.

### Build Commands

**Build the package:**
```bash
uv build
```
- Creates both source distribution (`.tar.gz`) and wheel (`.whl`) in `dist/` directory
- Takes approximately 10-20 seconds
- Outputs: `dist/amzsc-0.1.0-py3-none-any.whl` and `dist/amzsc-0.1.0.tar.gz`
- Note: You may see warnings about "toml section missing" for setuptools_scm - these are harmless

**Clean build artifacts:**
```bash
rm -rf dist build src/*.egg-info .pytest_cache .ruff_cache
```
- Always clean before a fresh build if you encounter issues
- The `.venv/` directory should NOT be deleted unless you want to reinstall all dependencies

### Linting & Code Quality

**Run ruff linter:**
```bash
uv run ruff check .
```
- Checks all Python files for style and common errors
- Takes approximately 5-10 seconds
- Should pass with "All checks passed!" on clean code
- Configuration is in `pyproject.toml` (uses default Ruff rules)

**Run ruff formatter:**
```bash
uv run ruff format .
```
- Auto-formats Python code to match project style
- Use this before committing code changes

**Run isort import sorter:**
```bash
uv run isort --check-only .
```
- Checks import statement ordering
- Takes approximately 5 seconds
- To auto-fix imports: `uv run isort .`

**Always run both ruff and isort before committing code changes.**

### Testing

**Run all tests:**
```bash
uv run pytest tests/ -v
```
- Tests are in `tests/` directory
- Currently has 1 test: `test_instance.py::test_result_data_type`
- **WARNING**: Tests require Chrome/Chromium and actually scrape Amazon, so they take 30+ seconds
- Tests may fail in headless/CI environments without proper Chrome setup
- Test configuration in `pyproject.toml`: `addopts = "--maxfail=1 --cov=testing_demo"`

**Run tests with coverage:**
```bash
uv run pytest tests/ --cov=amzsc --cov-report=html
```

**Important**: The test suite actually performs live Amazon scraping, so:
- Tests are slow (30+ seconds minimum)
- Tests require internet connectivity
- Tests may fail if Amazon blocks the request
- For development, consider mocking the scraper or skipping tests

### Import Validation
```bash
uv run python -c "from amzsc import AmazonScraper; print('Import successful')"
```
- Quick check that the package is importable after changes

## Project Architecture & Layout

### Directory Structure
```
amzsc/
├── .github/                  # GitHub configuration (workflows, copilot instructions)
├── src/amzsc/               # Main source code
│   ├── __init__.py          # Package entry point, exports AmazonScraper
│   ├── scraper.py           # Main AmazonScraper class (193 lines)
│   ├── handlers/            # Error handling utilities
│   │   ├── __init__.py      # Exports safe_method decorator
│   │   └── error_handler.py # @safe_method decorator for exception handling
│   ├── modules/             # Core functionality modules
│   │   ├── driver/          # Selenium WebDriver configuration
│   │   │   ├── driver_config.py      # ChromeDriverConfig with options setup
│   │   │   ├── driver_amazon.py      # AmazonDriver with scraping methods
│   │   │   └── driver_manipulator.py # ChromeManipulator base class
│   │   └── proxy/           # Proxy management
│   │       ├── __init__.py
│   │       ├── proxy.py            # get_proxy() function
│   │       └── proxy_request.py    # ProxyRequest class
│   └── utils/               # Utility functions and constants
│       ├── __init__.py
│       ├── constants.py     # Constants class with URLs and selectors
│       ├── custom_types.py  # Type definitions
│       ├── file_worker.py   # JSON file operations
│       └── marketplace.py   # get_zone() for marketplace domains
├── tests/
│   └── test_instance.py     # Basic integration test
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Locked dependency versions (662 lines)
├── .python-version          # Python version (3.9)
├── .gitignore               # Standard Python gitignore
└── README.md                # Usage example
```

### Key Files & Their Purpose

**src/amzsc/scraper.py** (193 lines):
- `AmazonScraper` class: Main public API
- `scrape_one()`: Scrapes a single ASIN
- `scrape_all()`: Multi-threaded scraping with ThreadPoolExecutor
- Configurable: proxy, headless mode, thread count, batch size, Selenium Grid support

**src/amzsc/modules/driver/driver_config.py**:
- `ChromeDriverConfig.get_options()`: Configures Chrome with anti-detection settings
- `ChromeDriverConfig.get_chrome_driver()`: Creates local Chrome driver
- `ChromeDriverConfig.get_remote_driver()`: Creates remote Selenium Grid driver
- Important anti-detection flags: `--disable-blink-features=AutomationControlled`, `--no-sandbox`

**src/amzsc/modules/driver/driver_amazon.py**:
- `AmazonDriver` class: Extends ChromeManipulator
- `get_product_overview()`: Scrapes from `productOverview_hoc_view_div` element
- `get_product_specs()`: Scrapes from `productSpecifications-content` table
- `get_product_micro()`: Scrapes from `.a-normal.a-spacing-micro` CSS selector
- All methods use `@safe_method` decorator for error handling

**src/amzsc/utils/constants.py**:
- Amazon element IDs and selectors (PRODUCT_OVERVIEW, PRODUCT_SPECS, etc.)
- Proxy API endpoints
- Monitor dimensions for window positioning (1920x1080)

**src/amzsc/handlers/error_handler.py**:
- `@safe_method` decorator: Catches exceptions, logs errors, returns None
- Used throughout the codebase for graceful failure handling

### Dependencies

**Core Dependencies** (from pyproject.toml):
- `selenium>=4.34.2`: Web automation
- `requests>=2.32.4`: HTTP requests for proxy management
- `bs4>=0.0.2`: BeautifulSoup for HTML parsing
- `fake-useragent>=2.2.0`: Random user agent generation

**Dev Dependencies**:
- `pytest>=8.4.1`: Testing framework
- `pytest-cov>=6.2.1`: Coverage reporting
- `ruff>=0.12.8`: Fast Python linter/formatter
- `isort>=6.0.1`: Import statement sorting

## Validation & CI/CD

### No Pre-commit Hooks
This repository does not have pre-commit hooks configured. Always manually run linting before committing:
```bash
uv run ruff check . && uv run isort --check-only .
```

### No GitHub Actions CI (Currently)
There are currently no automated CI workflows for builds or tests. The repository has one Copilot coding agent workflow but no standard CI/CD pipeline. **When making changes, you are responsible for:**
1. Running lints manually
2. Running tests manually (if applicable)
3. Building the package to verify no errors

### Manual Validation Checklist
Before finalizing any code change:
1. ✓ Run `uv sync` to ensure dependencies are current
2. ✓ Run `uv run ruff check .` - must pass
3. ✓ Run `uv run isort --check-only .` - must pass
4. ✓ Run `uv build` - must complete without errors
5. ✓ Run `uv run python -c "from amzsc import AmazonScraper"` - must import successfully
6. ⚠ Run `uv run pytest tests/ -v` - optional (requires Chrome and is slow)

## Common Issues & Workarounds

### Issue: "uv: command not found"
**Solution**: Install uv first: `pip install uv`

### Issue: Build shows "toml section missing" warnings
**Status**: Harmless warning about setuptools_scm configuration
**Action**: Ignore - builds still succeed

### Issue: Tests hang or timeout
**Cause**: Tests perform actual Amazon scraping and require Chrome
**Solutions**:
- Ensure Chrome/Chromium is installed
- Run tests with more time: `uv run pytest tests/ -v --timeout=60`
- In CI environments, tests may need to be skipped or mocked

### Issue: Import fails with "No module named 'amzsc'"
**Solution**: Run `uv sync` to install the package in development mode

### Issue: Ruff or other tools not found
**Solution**: Always prefix commands with `uv run` to use the virtual environment

## Development Workflow

1. **Start**: Run `uv sync` (only needed once per session or after dependency changes)
2. **Make changes**: Edit Python files in `src/amzsc/`
3. **Format code**: `uv run ruff format . && uv run isort .`
4. **Lint**: `uv run ruff check .`
5. **Build**: `uv build` (to verify package builds correctly)
6. **Test** (if relevant): `uv run pytest tests/ -v`
7. **Commit**: After all checks pass

## Important Notes

- **Always use `uv run` prefix** for Python commands to ensure the correct virtual environment
- **The test suite is slow** - it actually scrapes Amazon and takes 30+ seconds minimum
- **Chrome is required** for tests but NOT for linting or building
- **Build artifacts** (dist/, build/) are gitignored - clean them with `rm -rf dist build src/*.egg-info`
- **The .venv/ directory** should not be committed (it's in .gitignore)
- **No type checking configured** - pyproject.toml doesn't specify mypy or similar
- **Selenium requires Chrome** - tests will fail without Chrome/Chromium installed

## Trust These Instructions

These instructions were validated by running each command and verifying the output. Only explore or search for alternative approaches if:
- A command fails with an unexpected error
- You need to understand implementation details beyond what's documented here
- The instructions appear outdated (e.g., file paths don't exist)

Always start with `uv sync` and the documented commands above before exploring alternatives.
