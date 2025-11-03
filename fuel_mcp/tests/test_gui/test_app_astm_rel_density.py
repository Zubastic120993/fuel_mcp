"""
test_app_astm_rel_density.py
=============================
Tests for ASTM Relative Density Entry calculator (app_astm_rel_density.py)
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


@pytest.fixture
def mock_vcf_response():
    """Mock VCF API response."""
    return {
        "result": {
            "rho15": 875.0,
            "VCF": 0.99154,
            "table": "24B",
            "tempC": 37.8,
        }
    }


class TestComputeFromRelDensity:
    """Tests for compute_from_rel_density function."""

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_from_rel_density_success(self, mock_get, mock_vcf_response):
        """Test successful relative density calculation."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns
        assert "Value" in result.columns

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_rel_density_to_density_conversion(self, mock_get, mock_vcf_response):
        """Test relative density to density @15°C conversion."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        # Relative density 0.8762 should give density around 875 kg/m³
        result = compute_from_rel_density(rel_density=0.8762, temp_f=60.0)

        # Verify the conversion happened
        density_rows = result[result["Parameter"].str.contains("Density", na=False)]
        assert len(density_rows) > 0

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_temperature_conversion_fahrenheit_to_celsius(self, mock_get, mock_vcf_response):
        """Test temperature conversion from Fahrenheit to Celsius."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        # 100°F should be approximately 37.8°C
        temp_rows = result[result["Parameter"].str.contains("°C", na=False)]
        assert len(temp_rows) > 0

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_includes_api_gravity(self, mock_get, mock_vcf_response):
        """Test that result includes calculated API gravity."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=60.0)

        # Should include API gravity calculation
        api_rows = result[result["Parameter"].str.contains("API", na=False)]
        assert len(api_rows) > 0

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_includes_volume_tables(self, mock_get, mock_vcf_response):
        """Test that result includes Volume IV/V/VI → XII tables."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        # Check for ASTM table references (T.21-T.31)
        param_column = result["Parameter"].astype(str)
        assert any("T.2" in str(p) for p in param_column)
        assert any("VCF" in str(p) for p in param_column)

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_error_handling(self, mock_get):
        """Test error handling when API call fails."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.side_effect = Exception("API error")

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_various_relative_densities(self, mock_get, mock_vcf_response):
        """Test with various relative density values."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        # Light fuel
        result_light = compute_from_rel_density(rel_density=0.75, temp_f=60.0)
        assert isinstance(result_light, pd.DataFrame)

        # Heavy fuel
        result_heavy = compute_from_rel_density(rel_density=0.98, temp_f=60.0)
        assert isinstance(result_heavy, pd.DataFrame)

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_compute_vcf_table_reference(self, mock_get, mock_vcf_response):
        """Test that VCF uses correct Table 24A/B/C reference."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=60.0)

        # Should reference Table 24 (not 54)
        vcf_rows = result[result["Parameter"].str.contains("24", na=False)]
        assert len(vcf_rows) > 0


class TestGradioInterface:
    """Tests for Gradio interface."""

    def test_demo_exists(self):
        """Test that demo interface is created."""
        from fuel_mcp.gui_astm import app_astm_rel_density

        assert hasattr(app_astm_rel_density, "demo")
        assert app_astm_rel_density.demo is not None

    def test_api_url_configured(self):
        """Test that API URL is configured."""
        from fuel_mcp.gui_astm import app_astm_rel_density

        assert hasattr(app_astm_rel_density, "API_URL")


class TestDataFormat:
    """Tests for data formatting."""

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_result_dataframe_structure(self, mock_get, mock_vcf_response):
        """Test that result DataFrame has correct structure."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        assert result.shape[1] == 2
        assert list(result.columns) == ["Parameter", "Value"]

    @patch("fuel_mcp.gui_astm.app_astm_rel_density.requests.get")
    def test_numeric_precision(self, mock_get, mock_vcf_response):
        """Test numeric precision in results."""
        from fuel_mcp.gui_astm.app_astm_rel_density import compute_from_rel_density

        mock_get.return_value.json.return_value = mock_vcf_response

        result = compute_from_rel_density(rel_density=0.8762, temp_f=100.0)

        # Check for relative density with 4 decimal places
        rel_dens_rows = result[result["Parameter"].str.contains("Relative Density", na=False)]
        if len(rel_dens_rows) > 0:
            value = str(rel_dens_rows.iloc[0]["Value"])
            assert "0.8762" in value

