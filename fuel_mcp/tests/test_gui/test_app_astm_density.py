"""
test_app_astm_density.py
=========================
Tests for ASTM Density Entry calculator (app_astm_density.py)
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


@pytest.fixture
def mock_vcf_response():
    """Mock VCF API response."""
    return {
        "result": {
            "VCF": 0.99154,
            "tempC": 32.2,
            "table": "54B",
        }
    }


class TestCalculateDensity:
    """Tests for calculate_density function."""

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_success(self, mock_get, mock_vcf_response):
        """Test successful density calculation."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = calculate_density(density=875.7, temp_c=32.2)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns
        assert "Value" in result.columns

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_with_api_call(self, mock_get, mock_vcf_response):
        """Test that API is called with correct parameters."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_response = MagicMock()
        mock_response.json.return_value = mock_vcf_response
        mock_get.return_value = mock_response

        calculate_density(density=875.7, temp_c=32.2)

        # Verify API was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "params" in call_args.kwargs
        assert "rho15" in call_args.kwargs["params"]
        assert "tempC" in call_args.kwargs["params"]

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_includes_all_tables(self, mock_get, mock_vcf_response):
        """Test that result includes ASTM tables 54A/B/C and Volume XII."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = calculate_density(density=875.7, temp_c=32.2)

        # Check for ASTM table references
        param_column = result["Parameter"].astype(str)
        assert any("T.54" in str(p) for p in param_column)
        assert any("VCF" in str(p) for p in param_column)

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_error_handling(self, mock_get):
        """Test error handling when API call fails."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.side_effect = Exception("Network error")

        result = calculate_density(density=875.7, temp_c=32.2)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_various_fuels(self, mock_get, mock_vcf_response):
        """Test with various fuel density values."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        # Test diesel density
        result_diesel = calculate_density(density=850.0, temp_c=25.0)
        assert isinstance(result_diesel, pd.DataFrame)

        # Test HFO density
        result_hfo = calculate_density(density=980.0, temp_c=50.0)
        assert isinstance(result_hfo, pd.DataFrame)

        # Test gasoline density
        result_gasoline = calculate_density(density=740.0, temp_c=20.0)
        assert isinstance(result_gasoline, pd.DataFrame)

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_temperature_range(self, mock_get, mock_vcf_response):
        """Test with different temperature values."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        # Low temperature
        result_low = calculate_density(density=875.7, temp_c=-10.0)
        assert isinstance(result_low, pd.DataFrame)

        # High temperature
        result_high = calculate_density(density=875.7, temp_c=80.0)
        assert isinstance(result_high, pd.DataFrame)

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_calculate_density_timeout(self, mock_get):
        """Test API timeout handling."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.side_effect = TimeoutError("Request timeout")

        result = calculate_density(density=875.7, temp_c=32.2)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]


class TestGradioInterface:
    """Tests for Gradio interface."""

    def test_demo_exists(self):
        """Test that demo interface is created."""
        from fuel_mcp.gui_astm import app_astm_density

        assert hasattr(app_astm_density, "demo")
        assert app_astm_density.demo is not None

    def test_api_url_configured(self):
        """Test that API URL is configured."""
        from fuel_mcp.gui_astm import app_astm_density

        assert hasattr(app_astm_density, "API_URL")
        assert isinstance(app_astm_density.API_URL, str)


class TestResultFormat:
    """Tests for result formatting."""

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_result_has_correct_structure(self, mock_get, mock_vcf_response):
        """Test that result DataFrame has correct structure."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = calculate_density(density=875.7, temp_c=32.2)

        assert result.shape[1] == 2
        assert list(result.columns) == ["Parameter", "Value"]

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_result_contains_required_parameters(self, mock_get, mock_vcf_response):
        """Test that result contains all required parameters."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = calculate_density(density=875.7, temp_c=32.2)

        param_column = result["Parameter"].astype(str)
        # Should include VCF and temperature
        assert any("VCF" in str(p) for p in param_column)
        assert any("Temperature" in str(p) or "T.2" in str(p) for p in param_column)

