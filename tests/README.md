# FastAPI Tests

This directory contains comprehensive tests for the Mergington High School Activities API.

## Overview

The test suite provides 100% code coverage for all API endpoints and includes:

- **Root Endpoint Tests**: Verify redirect functionality
- **Activities Endpoint Tests**: Test activity data retrieval and structure
- **Signup Endpoint Tests**: Test student registration functionality
- **Unregister Endpoint Tests**: Test participant removal functionality
- **Edge Cases**: Test error conditions and invalid inputs
- **Data Persistence**: Test complex scenarios with multiple operations

## Test Structure

```
tests/
├── __init__.py          # Package initialization
├── conftest.py          # Test configuration and fixtures
└── test_api.py          # Main test cases
```

## Running Tests

### Method 1: Using the test runner script
```bash
python run_tests.py
```

### Method 2: Using pytest directly
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run with HTML coverage report
pytest tests/ --cov=src --cov-report=html
```

### Method 3: Run specific test classes
```bash
# Run only signup tests
pytest tests/test_api.py::TestSignupEndpoint -v

# Run only unregister tests
pytest tests/test_api.py::TestUnregisterEndpoint -v
```

## Test Coverage

Current coverage: **100%** of the FastAPI application code

The tests cover:
- ✅ All HTTP endpoints (GET, POST, DELETE)
- ✅ Success and error scenarios
- ✅ URL encoding/decoding
- ✅ Data validation
- ✅ State management
- ✅ Edge cases and error conditions

## Test Features

### Fixtures
- `client`: FastAPI TestClient for making HTTP requests
- `reset_activities`: Resets activity data before each test

### Test Categories
1. **TestRootEndpoint**: Tests the `/` redirect
2. **TestActivitiesEndpoint**: Tests `/activities` GET endpoint
3. **TestSignupEndpoint**: Tests `/activities/{name}/signup` POST endpoint
4. **TestUnregisterEndpoint**: Tests `/activities/{name}/unregister` DELETE endpoint
5. **TestEdgeCases**: Tests error conditions and validation
6. **TestDataPersistence**: Tests complex multi-operation scenarios

## Dependencies

The following packages are required for testing:
- `pytest`: Test framework
- `httpx`: HTTP client for testing
- `pytest-asyncio`: Async test support
- `pytest-cov`: Coverage reporting

Install with:
```bash
pip install -r requirements.txt
```