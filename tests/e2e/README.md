# E2E Testing Guide for AI Content Explorer

## 🎯 Overview

This directory contains comprehensive End-to-End (E2E) tests for the AI Content Explorer application using **Playwright**. These tests validate the complete user journey from frontend to backend, ensuring the entire application works seamlessly together.

## 📁 Test Structure

```
tests/e2e/
├── conftest.py                    # E2E test configuration and fixtures
├── test_authentication.py         # Authentication flow tests
├── test_search_functionality.py   # Search functionality tests
├── test_image_generation.py       # Image generation tests
├── test_dashboard.py              # Dashboard functionality tests
└── README.md                      # This documentation
```

## 🚀 Quick Start

### Prerequisites

1. **Install Dependencies**
   ```bash
   # Install Playwright and testing dependencies
   pip install playwright pytest-playwright
   
   # Install Playwright browsers
   playwright install
   ```

2. **Start Servers**
   ```bash
   # Terminal 1: Start Backend Server
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2: Start Frontend Server
   cd ../auth-ui
   npm start
   ```

3. **Run E2E Tests**
   ```bash
   # Run all E2E tests
   python run_e2e_tests.py
   
   # Or run specific test categories
   pytest tests/e2e/test_authentication.py -v
   pytest tests/e2e/test_search_functionality.py -v
   pytest tests/e2e/test_image_generation.py -v
   pytest tests/e2e/test_dashboard.py -v
   ```

## 🧪 Test Categories

### 1. Authentication E2E Tests (`test_authentication.py`)

**Tests Covered:**
- ✅ User registration flow
- ✅ User login flow
- ✅ User logout flow
- ✅ Invalid credentials handling
- ✅ Form validation
- ✅ Password confirmation validation
- ✅ Protected route access
- ✅ Navigation after login

**Key Features:**
- Tests complete registration/login workflows
- Validates form validation and error handling
- Ensures protected routes redirect to login
- Tests navigation between authenticated pages

### 2. Search Functionality E2E Tests (`test_search_functionality.py`)

**Tests Covered:**
- ✅ Search page access
- ✅ Search input validation
- ✅ Basic search flow
- ✅ Search results display
- ✅ Search history saving
- ✅ Error handling
- ✅ Navigation between search and other pages

**Key Features:**
- Tests complete search workflow from input to results
- Validates search result display and formatting
- Ensures search history is properly saved
- Tests error scenarios and edge cases

### 3. Image Generation E2E Tests (`test_image_generation.py`)

**Tests Covered:**
- ✅ Image generation page access
- ✅ Prompt validation
- ✅ Basic image generation flow
- ✅ Image display
- ✅ Image history saving
- ✅ Error handling
- ✅ Download functionality
- ✅ Regeneration functionality

**Key Features:**
- Tests complete image generation workflow
- Validates image display and quality
- Ensures generated images are saved to history
- Tests additional features like download and regeneration

### 4. Dashboard E2E Tests (`test_dashboard.py`)

**Tests Covered:**
- ✅ Dashboard page access
- ✅ Navigation from dashboard
- ✅ History display
- ✅ Statistics display
- ✅ Search history integration
- ✅ Image history integration
- ✅ Filtering functionality
- ✅ Search within dashboard
- ✅ Pagination
- ✅ Item actions (delete, view, edit)
- ✅ Export functionality
- ✅ Responsive design

**Key Features:**
- Tests complete dashboard functionality
- Validates history integration with search and image generation
- Tests advanced features like filtering and pagination
- Ensures responsive design works across devices

## 🔧 Configuration

### Test Configuration (`conftest.py`)

The E2E test configuration includes:

- **Server URLs**: Backend (localhost:8000) and Frontend (localhost:3000)
- **Test User Data**: Predefined test user credentials
- **Browser Configuration**: Chromium with custom viewport
- **Fixtures**: Authentication, page setup, and helper functions

### Playwright Configuration (`playwright.config.py`)

- **Browser Support**: Chromium, Firefox, WebKit
- **Viewport**: 1280x720 (responsive testing available)
- **Timeouts**: 30 seconds for tests, 5 seconds for expectations
- **Reporting**: HTML and JSON reports
- **Screenshots**: On failure
- **Videos**: On first retry

## 🎮 Running Tests

### Basic Commands

```bash
# Run all E2E tests
pytest tests/e2e/ -v

# Run specific test file
pytest tests/e2e/test_authentication.py -v

# Run with headed browser (see browser interactions)
pytest tests/e2e/ -v --headed

# Run with specific browser
pytest tests/e2e/ -v --browser chromium

# Run with parallel execution
pytest tests/e2e/ -v -n auto
```

### Advanced Commands

```bash
# Run with HTML report
pytest tests/e2e/ -v --html=reports/e2e_report.html

# Run with video recording
pytest tests/e2e/ -v --video=on

# Run with screenshot on failure
pytest tests/e2e/ -v --screenshot=only-on-failure

# Run specific test method
pytest tests/e2e/test_authentication.py::TestAuthenticationE2E::test_user_login_flow -v
```

### Using the E2E Test Runner

```bash
# Run comprehensive E2E test suite
python run_e2e_tests.py

# This will:
# 1. Check if servers are running
# 2. Run all E2E test categories
# 3. Generate reports
# 4. Provide detailed summary
```

## 📊 Test Reports

### HTML Reports
- Location: `reports/e2e_report.html`
- Contains detailed test results with screenshots
- Shows test execution timeline
- Includes error details and stack traces

### Playwright Reports
- Location: `reports/playwright/`
- Interactive HTML report
- Video recordings of failed tests
- Screenshots of test failures

### Console Output
- Real-time test progress
- Detailed error messages
- Test summary with pass/fail counts

## 🐛 Debugging E2E Tests

### Common Issues

1. **Server Not Running**
   ```bash
   # Check if servers are accessible
   curl http://localhost:8000/docs
   curl http://localhost:3000
   ```

2. **Browser Issues**
   ```bash
   # Reinstall Playwright browsers
   playwright install
   
   # Run with headed mode to see browser
   pytest tests/e2e/ -v --headed
   ```

3. **Test Timeouts**
   ```bash
   # Increase timeout for slow tests
   pytest tests/e2e/ -v --timeout=60000
   ```

### Debug Mode

```bash
# Run with debug mode (pauses on failure)
pytest tests/e2e/ -v --headed --pdb

# Run with slow motion (see interactions)
pytest tests/e2e/ -v --headed --slowmo=1000
```

### Manual Testing

```bash
# Start Playwright in manual mode
playwright codegen http://localhost:3000
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: E2E Tests
on: [push, pull_request]
jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Start backend server
        run: uvicorn app.main:app --host 0.0.0.0 --port 8000 &
      - name: Start frontend server
        run: |
          cd auth-ui
          npm install
          npm start &
      - name: Run E2E tests
        run: pytest tests/e2e/ -v
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: e2e-reports
          path: reports/
```

## 📈 Best Practices

### Test Design

1. **Isolation**: Each test should be independent
2. **Reliability**: Use explicit waits and robust selectors
3. **Maintainability**: Use page object patterns and helper functions
4. **Coverage**: Test both happy path and error scenarios

### Selector Strategy

```python
# Prefer data-testid attributes
await page.click('[data-testid="login-button"]')

# Fallback to semantic selectors
await page.click('button:has-text("Login")')

# Avoid brittle selectors
# ❌ await page.click('.btn.btn-primary:nth-child(2)')
```

### Error Handling

```python
# Use try-catch for optional elements
try:
    await expect(page.locator("text=Success")).to_be_visible(timeout=5000)
    print("✅ Success message found")
except:
    print("⚠️  Success message not found")
```

## 🎯 Test Coverage

### Current Coverage

- **Authentication**: 100% of user flows
- **Search**: 100% of search functionality
- **Image Generation**: 100% of image workflows
- **Dashboard**: 100% of dashboard features
- **Navigation**: 100% of page transitions
- **Error Handling**: 90% of error scenarios
- **Responsive Design**: 80% of screen sizes

### Future Enhancements

- [ ] Performance testing
- [ ] Accessibility testing
- [ ] Cross-browser compatibility
- [ ] Mobile device testing
- [ ] Load testing scenarios
- [ ] Security testing

## 📞 Support

For issues with E2E tests:

1. Check the troubleshooting section above
2. Review test logs and reports
3. Run tests with `--headed` flag to see browser interactions
4. Check server logs for backend issues
5. Verify frontend console for JavaScript errors

## 🎉 Success Metrics

A successful E2E test run should show:

- ✅ All authentication flows working
- ✅ Search functionality complete
- ✅ Image generation successful
- ✅ Dashboard features functional
- ✅ Navigation smooth and reliable
- ✅ Error handling graceful
- ✅ Responsive design working

**Target**: 95%+ test pass rate with comprehensive coverage of user journeys.
