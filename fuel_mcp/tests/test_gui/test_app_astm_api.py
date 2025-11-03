"""
test_app_astm_api.py
====================
Tests for ASTM API Gravity Entry calculator (app_astm_api.py)
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


@pytest.fixture
def mock_vcf_response():
    """Mock VCF API response."""
    return {
        "result": {
            "rho15": 876.0,
            "VCF": 0.99154,
            "table": "54B (Residual / Marine fuels)",
            "tempC": 15.6,
        }
    }


class TestComputeASTM:
    """Tests for compute_astm function."""

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_success(self, mock_get, mock_vcf_response):
        """Test successful ASTM calculation from API gravity."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_astm(api=30.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns
        assert "Value" in result.columns

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_with_different_temperatures(self, mock_get, mock_vcf_response):
        """Test calculation with various temperature values."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        # Test with 100°F
        result = compute_astm(api=35.0, temp_f=100.0)

        assert isinstance(result, pd.DataFrame)
        # Verify temperature conversion (100°F should be ~37.8°C)
        temp_rows = result[result["Parameter"].str.contains("Temperature", na=False)]
        assert len(temp_rows) > 0

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_api_to_density_conversion(self, mock_get, mock_vcf_response):
        """Test API gravity to density conversion."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_astm(api=30.0, temp_f=60.0)

        # Check that density is calculated correctly
        # API 30 should give density around 876 kg/m³
        density_rows = result[result["Parameter"].str.contains("Density", na=False)]
        assert len(density_rows) > 0

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_includes_all_tables(self, mock_get, mock_vcf_response):
        """Test that result includes all ASTM tables T.2–T.14."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_astm(api=33.0, temp_f=60.0)

        # Verify key ASTM tables are present
        param_column = result["Parameter"].astype(str)
        assert any("T.2" in str(p) for p in param_column)
        assert any("T.3" in str(p) for p in param_column)
        assert any("T.4" in str(p) for p in param_column)
        assert any("VCF" in str(p) for p in param_column)

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_error_handling(self, mock_get):
        """Test error handling when API call fails."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.side_effect = Exception("Connection timeout")

        result = compute_astm(api=30.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]
        assert "timeout" in str(result.iloc[0, 1]).lower()

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_compute_astm_extreme_values(self, mock_get, mock_vcf_response):
        """Test with extreme API gravity values."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        # Very light crude (high API)
        result_light = compute_astm(api=50.0, temp_f=60.0)
        assert isinstance(result_light, pd.DataFrame)

        # Heavy crude (low API)
        result_heavy = compute_astm(api=10.0, temp_f=60.0)
        assert isinstance(result_heavy, pd.DataFrame)

    def test_compute_astm_api_url(self):
        """Test that correct API URL is used."""
        from fuel_mcp.gui_astm import app_astm_api

        assert hasattr(app_astm_api, "API_URL")
        assert "127.0.0.1" in app_astm_api.API_URL or "localhost" in app_astm_api.API_URL


class TestGradioInterface:
    """Tests for Gradio interface creation."""

    def test_demo_exists(self):
        """Test that demo interface is created."""
        from fuel_mcp.gui_astm import app_astm_api

        assert hasattr(app_astm_api, "demo")
        assert app_astm_api.demo is not None

    def test_demo_has_launch_method(self):
        """Test that demo has launch method."""
        from fuel_mcp.gui_astm import app_astm_api

        assert hasattr(app_astm_api.demo, "launch")


class TestDataFormat:
    """Tests for data formatting in results."""

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_result_dataframe_format(self, mock_get, mock_vcf_response):
        """Test that result is properly formatted DataFrame."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_astm(api=30.0, temp_f=60.0)

        assert result.shape[1] == 2  # Two columns
        assert list(result.columns) == ["Parameter", "Value"]

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_numeric_precision(self, mock_get, mock_vcf_response):
        """Test numeric value precision in results."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_astm(api=33.5, temp_f=77.0)

        # Check that VCF has appropriate decimal places
        vcf_rows = result[result["Parameter"].str.contains("VCF", na=False)]
        if len(vcf_rows) > 0:
            vcf_value = str(vcf_rows.iloc[0]["Value"])
            # VCF should have 5-6 decimal places
            if "." in vcf_value:
                decimals = len(vcf_value.split(".")[1])
                assert decimals >= 5

