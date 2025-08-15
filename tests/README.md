# Testing Guide for AI Content Explorer

This directory contains comprehensive tests for the AI Content Explorer backend application.

## 🏗️ Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_auth.py        # Authentication tests
│   ├── test_search.py      # Search functionality tests
│   ├── test_image.py       # Image generation tests
│   └── test_dashboard.py   # Dashboard functionality tests
├── integration/            # Integration tests
│   └── test_mcp_integration.py  # MCP service integration tests
└── e2e/                    # End-to-end tests
    ├── conftest.py         # E2E test configuration
    ├── test_authentication.py      # Authentication E2E tests
    ├── test_search_functionality.py # Search E2E tests
    ├── test_image_generation.py    # Image generation E2E tests
    ├── test_dashboard.py           # Dashboard E2E tests
    └── README.md                   # E2E testing guide
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run All Tests
```bash
# Using the test runner script
python run_tests.py

# Or using pytest directly
pytest tests/ -v

# Run E2E tests (requires servers running)
python run_e2e_tests.py
```

### 3. Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only (requires servers running)
pytest tests/e2e/ -v

# Tests with coverage report
pytest tests/ -v --cov=app --cov-report=html:htmlcov
```

## 📋 Test Categories

### 🔐 Authentication Tests (`test_auth.py`)
- **Password hashing and verification**
- **JWT token creation and validation**
- **User registration and login**
- **Authentication middleware**
- **Protected route access**

### 🔍 Search Tests (`test_search.py`)
- **Web search functionality**
- **Query validation**
- **MCP service integration**
- **Error handling**
- **History saving**

### 🎨 Image Generation Tests (`test_image.py`)
- **Image generation functionality**
- **Prompt validation**
- **MCP service integration**
- **Error handling**
- **History saving**

### 📊 Dashboard Tests (`test_dashboard.py`)
- **History retrieval**
- **Filtering and pagination**
- **CRUD operations**
- **Statistics calculation**
- **Soft delete functionality**

### 🔗 Integration Tests (`test_mcp_integration.py`)
- **MCP service communication**
- **Tavily search integration**
- **Flux image generation integration**
- **Error handling and recovery**
- **End-to-end workflows**

### 🌐 E2E Tests (`tests/e2e/`)
- **Complete user journeys**
- **Frontend-to-backend integration**
- **Cross-page navigation**
- **User experience validation**
- **Responsive design testing**
- **Real browser interactions**

## 🛠️ Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Test discovery patterns**
- **Coverage reporting**
- **Custom markers**
- **Output formatting**

### Test Fixtures (`conftest.py`)
- **Database setup and teardown**
- **Test user creation**
- **Authentication tokens**
- **MCP service mocking**
- **Sample data creation**

## 📊 Coverage Reports

The tests generate multiple coverage reports:

1. **Terminal Report**: Shows missing lines in terminal
2. **HTML Report**: Detailed coverage in `htmlcov/` directory
3. **XML Report**: For CI/CD integration

### View HTML Coverage Report
```bash
# After running tests with coverage
open htmlcov/index.html  # On macOS
start htmlcov/index.html  # On Windows
```

## 🏷️ Test Markers

Use pytest markers to run specific test categories:

```bash
# Run only authentication tests
pytest -m auth

# Run only search tests
pytest -m search

# Run only image generation tests
pytest -m image

# Run only dashboard tests
pytest -m dashboard

# Run only MCP integration tests
pytest -m mcp

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## 🔧 Test Database

Tests use SQLite in-memory database for:
- **Fast execution**
- **Isolation between tests**
- **No external dependencies**
- **Automatic cleanup**

## 🎯 Test Coverage Goals

- **Authentication**: 100%
- **Search functionality**: 95%+
- **Image generation**: 95%+
- **Dashboard operations**: 95%+
- **MCP integration**: 90%+
- **E2E user journeys**: 95%+
- **Overall coverage**: 90%+

## 🚨 Common Issues

### 1. Import Errors
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Connection Issues
- Tests use SQLite, no external database needed
- Check that `conftest.py` is properly configured

### 3. MCP Service Errors
- Integration tests mock MCP services
- Real MCP calls are not made during testing

### 4. Coverage Report Not Generated
```bash
# Install coverage dependencies
pip install pytest-cov

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 📝 Adding New Tests

### 1. Unit Tests
Create new test files in `tests/unit/`:
```python
import pytest

class TestNewFeature:
    def test_feature_functionality(self, client):
        # Test implementation
        pass
```

### 2. Integration Tests
Create new test files in `tests/integration/`:
```python
import pytest

class TestNewIntegration:
    def test_integration_flow(self, authenticated_client):
        # Integration test implementation
        pass
```

### 3. Test Fixtures
Add new fixtures to `conftest.py`:
```python
@pytest.fixture
def new_test_data():
    # Fixture implementation
    return test_data
```

## 🔄 Continuous Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd backend
    pip install -r requirements.txt
    pytest tests/ --cov=app --cov-report=xml
```

## 📚 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear test and function names
3. **Arrange-Act-Assert**: Structure tests clearly
4. **Mock External Services**: Don't make real API calls
5. **Cover Edge Cases**: Test error conditions
6. **Maintain Coverage**: Keep coverage above 90%

## 🎉 Success Criteria

A successful test run should show:
- ✅ All tests passing
- ✅ Coverage above 90%
- ✅ No external service calls
- ✅ Fast execution (< 30 seconds)
- ✅ Clear error messages
