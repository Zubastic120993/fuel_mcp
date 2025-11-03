# GUI Test Suite

This directory contains comprehensive tests for all Fuel MCP Gradio GUI applications.

## Test Files

### Individual GUI Application Tests

| Test File | Target Application | Description |
|-----------|-------------------|-------------|
| `test_app_astm_unified.py` | `app_astm_unified.py` | Tests for unified ASTM interface (all-in-one) |
| `test_app_astm_api.py` | `app_astm_api.py` | Tests for API Gravity Entry calculator |
| `test_app_astm_rel_density.py` | `app_astm_rel_density.py` | Tests for Relative Density Entry calculator |
| `test_app_astm_density.py` | `app_astm_density.py` | Tests for Density Entry calculator |
| `test_app_astm_vol_weight.py` | `app_astm_vol_weight.py` | Tests for Volume & Weight Converter |
| `test_app_astm_universal_converter.py` | `app_astm_universal_converter.py` | Tests for Universal Unit Converter |
| `test_gui_integration.py` | All GUI apps | Integration tests for common functionality |

## Test Coverage

### What Is Tested

1. **API Integration**
   - Mock API calls to MCP backend
   - Request parameter validation
   - Response handling
   - Error handling for API failures

2. **Calculation Functions**
   - API gravity → Density conversion
   - Relative density → Density conversion  
   - Temperature conversions (°F ↔ °C)
   - VCF calculations
   - Unit conversions

3. **Data Validation**
   - Input parameter validation
   - Output format verification
   - Numeric precision checks
   - Edge case handling

4. **Gradio Interface**
   - Demo creation
   - Component existence
   - Launch method availability

5. **Error Handling**
   - Network errors
   - Invalid inputs
   - API timeout
   - Conversion errors

6. **Integration Tests**
   - Common features across all GUI apps
   - Port configuration
   - API URL consistency
   - Response format standardization

## Running Tests

### Run All GUI Tests
```bash
cd /Users/vladymyrzub/Desktop/fuel_mcp
pytest fuel_mcp/tests/test_gui/ -v
```

### Run Specific Test File
```bash
# Test unified GUI
pytest fuel_mcp/tests/test_gui/test_app_astm_unified.py -v

# Test API gravity calculator
pytest fuel_mcp/tests/test_gui/test_app_astm_api.py -v

# Test density calculator
pytest fuel_mcp/tests/test_gui/test_app_astm_density.py -v

# Run integration tests
pytest fuel_mcp/tests/test_gui/test_gui_integration.py -v
```

### Run Specific Test Class
```bash
pytest fuel_mcp/tests/test_gui/test_app_astm_unified.py::TestAPIGravityEntry -v
```

### Run with Coverage
```bash
pytest fuel_mcp/tests/test_gui/ --cov=fuel_mcp.gui_astm --cov-report=html
```

### Run with Verbose Output
```bash
pytest fuel_mcp/tests/test_gui/ -vv -s
```

## Test Structure

Each test file follows this structure:

```python
# Fixtures
@pytest.fixture
def mock_api_response():
    """Mock API response."""
    return {...}

# Test Classes
class TestFunctionName:
    """Tests for specific function."""
    
    def test_success_case(self):
        """Test successful execution."""
        ...
    
    def test_error_case(self):
        """Test error handling."""
        ...

class TestGradioInterface:
    """Tests for Gradio interface."""
    ...
```

## Mocking Strategy

All tests use `unittest.mock.patch` to mock external dependencies:

- **API Calls**: Mock `requests.get()` to avoid actual HTTP calls
- **Unit Conversions**: Mock `convert()` function for predictable results
- **Gradio Interface**: Test interface creation without launching

Example:
```python
@patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
def test_compute_astm_success(self, mock_get, mock_vcf_response):
    mock_get.return_value.json.return_value = mock_vcf_response
    result = compute_astm(api=30.0, temp_f=60.0)
    assert isinstance(result, pd.DataFrame)
```

## Test Statistics

### Expected Test Counts

| Test File | Approximate Tests |
|-----------|------------------|
| `test_app_astm_unified.py` | 20+ tests |
| `test_app_astm_api.py` | 10+ tests |
| `test_app_astm_density.py` | 10+ tests |
| `test_app_astm_rel_density.py` | 10+ tests |
| `test_app_astm_vol_weight.py` | 12+ tests |
| `test_app_astm_universal_converter.py` | 15+ tests |
| `test_gui_integration.py` | 15+ tests |
| **Total** | **90+ tests** |

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

- No actual GUI windows opened
- No browser automation required
- Fast execution (all mocked)
- Deterministic results

## Dependencies

Tests require:
- `pytest`
- `pandas`
- `gradio`
- `requests`
- `unittest.mock` (standard library)

## Contributing

When adding new GUI applications:

1. Create corresponding test file in `test_gui/`
2. Follow existing test structure
3. Mock all external dependencies
4. Test success and error cases
5. Add integration tests if needed

## Notes

- Tests do NOT launch actual Gradio interfaces
- All API calls are mocked - no actual backend required
- Tests can run offline
- Fast execution (< 5 seconds for all GUI tests)

---

**Maintainer:** Chief Engineer Volodymyr Zub  
**Version:** 1.5.0  
**Last Updated:** 2025-11-03

