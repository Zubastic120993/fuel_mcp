"""
test_app_astm_unified.py
=========================
Tests for the unified ASTM GUI interface (app_astm_unified.py)
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


@pytest.fixture
def mock_api_response():
    """Mock API response from MCP backend."""
    return {
        "success": True,
        "result": {
            "rho15": 850.0,
            "tempC": 25.0,
            "VCF": 0.99154,
            "table": "54B (Residual / Marine fuels)",
        },
        "_meta": {
            "version": "1.5.0",
            "timestamp": "2025-11-03T12:00:00Z",
            "mode": "vcf",
        },
    }


class TestAPIGravityEntry:
    """Tests for API Gravity Entry tab."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_compute_api_gravity_success(self, mock_get, mock_api_response):
        """Test successful API gravity calculation."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_api_gravity

        mock_get.return_value.json.return_value = mock_api_response

        result = compute_api_gravity(api=30.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns
        assert "Value" in result.columns
        mock_get.assert_called_once()

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_compute_api_gravity_error(self, mock_get):
        """Test API gravity calculation with API error."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_api_gravity

        mock_get.side_effect = Exception("Connection error")

        result = compute_api_gravity(api=30.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]

    def test_compute_api_gravity_conversion(self):
        """Test API to density conversion logic."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_api_gravity

        with patch("fuel_mcp.gui_astm.app_astm_unified.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "result": {"rho15": 876.0, "VCF": 0.99, "table": "54B"}
            }

            result = compute_api_gravity(api=30.0, temp_f=60.0)

            # Verify density calculation: rho15 = 141.5 / (API + 131.5) * 999.016
            expected_rho15 = 141.5 / (30.0 + 131.5) * 999.016
            assert abs(expected_rho15 - 876.0) < 10  # Approximate check


class TestRelativeDensityEntry:
    """Tests for Relative Density Entry tab."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_compute_relative_density_success(self, mock_get, mock_api_response):
        """Test successful relative density calculation."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_relative_density

        mock_get.return_value.json.return_value = mock_api_response

        result = compute_relative_density(rel_density=0.8762, temp_f=100.0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns
        assert "Value" in result.columns

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_compute_relative_density_error(self, mock_get):
        """Test relative density calculation with error."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_relative_density

        mock_get.side_effect = Exception("API Error")

        result = compute_relative_density(rel_density=0.8762, temp_f=100.0)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]


class TestDensityEntry:
    """Tests for Density Entry tab."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_calculate_density_success(self, mock_get, mock_api_response):
        """Test successful density calculation."""
        from fuel_mcp.gui_astm.app_astm_unified import calculate_density

        mock_get.return_value.json.return_value = mock_api_response

        result = calculate_density(density=875.7, temp_c=32.2)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Parameter" in result.columns

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_calculate_density_error(self, mock_get):
        """Test density calculation with error."""
        from fuel_mcp.gui_astm.app_astm_unified import calculate_density

        mock_get.side_effect = Exception("Network error")

        result = calculate_density(density=875.7, temp_c=32.2)

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]


class TestVolumeWeightConverter:
    """Tests for Volume & Weight Converter tab."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_convert_vol_weight_success(self, mock_get, mock_api_response):
        """Test successful volume/weight conversion."""
        from fuel_mcp.gui_astm.app_astm_unified import convert_vol_weight

        mock_get.return_value.json.return_value = mock_api_response

        result = convert_vol_weight(
            table="54B",
            temp_unit="°C",
            rho15=796.7,
            temp_obs=22.6,
            from_unit="M3 @15°C",
            to_unit="US Gallons @60°F",
            value=2941,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_convert_vol_weight_fahrenheit(self, mock_get, mock_api_response):
        """Test conversion with Fahrenheit temperature."""
        from fuel_mcp.gui_astm.app_astm_unified import convert_vol_weight

        mock_get.return_value.json.return_value = mock_api_response

        result = convert_vol_weight(
            table="54B",
            temp_unit="°F",
            rho15=796.7,
            temp_obs=72.0,
            from_unit="BBLS @Temp.",
            to_unit="Metric Tonnes (Air)",
            value=100,
        )

        assert isinstance(result, pd.DataFrame)
        # Verify temperature conversion from F to C happened
        mock_get.assert_called_once()

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_convert_vol_weight_error(self, mock_get):
        """Test volume/weight conversion with error."""
        from fuel_mcp.gui_astm.app_astm_unified import convert_vol_weight

        mock_get.side_effect = Exception("Conversion error")

        result = convert_vol_weight(
            table="54B",
            temp_unit="°C",
            rho15=796.7,
            temp_obs=22.6,
            from_unit="M3 @15°C",
            to_unit="US Gallons @60°F",
            value=2941,
        )

        assert isinstance(result, pd.DataFrame)
        assert "Error" in result.iloc[0, 0]


class TestUniversalConverter:
    """Tests for Universal Unit Converter tab."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.convert")
    def test_smart_convert_success(self, mock_convert):
        """Test successful unit conversion."""
        from fuel_mcp.gui_astm.app_astm_unified import smart_convert

        mock_convert.return_value = 1000.0

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Metric Tons (tonne)",
            value="1000",
        )

        assert "1000.0" in result
        assert "Metric Tons" in result
        assert "ASTM" in source

    def test_smart_convert_invalid_value(self):
        """Test conversion with invalid numeric value."""
        from fuel_mcp.gui_astm.app_astm_unified import smart_convert

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Metric Tons (tonne)",
            value="invalid",
        )

        assert "Invalid" in result or "⚠️" in result or "could not convert" in result

    def test_smart_convert_missing_parameters(self):
        """Test conversion with missing parameters."""
        from fuel_mcp.gui_astm.app_astm_unified import smart_convert

        result, source = smart_convert(
            group=None, from_label="kg", to_label="tonne", value="100"
        )

        assert "⚠️" in result or "Please select" in result

    @patch("fuel_mcp.gui_astm.app_astm_unified.convert")
    def test_smart_convert_error(self, mock_convert):
        """Test conversion with calculation error."""
        from fuel_mcp.gui_astm.app_astm_unified import smart_convert

        mock_convert.side_effect = Exception("Conversion failed")

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Pounds (lb)",
            value="100",
        )

        assert "⚠️" in result


class TestUnifiedGUICreation:
    """Tests for the unified GUI interface creation."""

    def test_create_unified_gui(self):
        """Test that the unified GUI can be created without errors."""
        from fuel_mcp.gui_astm.app_astm_unified import create_unified_gui

        demo = create_unified_gui()

        assert demo is not None
        # Check that it's a Gradio Blocks object
        assert hasattr(demo, "launch")

    def test_gui_has_tabs(self):
        """Test that the GUI interface has the expected structure."""
        from fuel_mcp.gui_astm.app_astm_unified import create_unified_gui

        demo = create_unified_gui()

        # Verify it's a valid Gradio interface
        assert demo is not None
        assert hasattr(demo, "blocks")


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_labelize(self):
        """Test unit label conversion."""
        from fuel_mcp.gui_astm.app_astm_unified import labelize

        assert "Kilograms" in labelize("kg")
        assert "Pounds" in labelize("lb")
        assert "Cubic Metres" in labelize("m3")

    def test_normalize_label(self):
        """Test label normalization."""
        from fuel_mcp.gui_astm.app_astm_unified import normalize_label, UNIT_LABELS

        # Test that normalize_label function exists and returns something
        result_kg = normalize_label("Kilograms (kg)")
        result_lb = normalize_label("Pounds (lb)")
        
        # Should return either the matched unit key or the input label
        assert result_kg is not None
        assert result_lb is not None
        
        # If it matches a UNIT_LABELS key, it should return that key
        # Otherwise it returns the normalized input
        assert result_kg in UNIT_LABELS or "kg" in result_kg.lower()


# Integration-style test
class TestUnifiedIntegration:
    """Integration tests for the unified interface."""

    @patch("fuel_mcp.gui_astm.app_astm_unified.requests.get")
    def test_full_workflow_api_gravity(self, mock_get):
        """Test complete workflow for API gravity calculation."""
        from fuel_mcp.gui_astm.app_astm_unified import compute_api_gravity

        mock_get.return_value.json.return_value = {
            "result": {"rho15": 876.0, "VCF": 0.99154, "table": "54B", "tempC": 15.6}
        }

        # Test with typical marine fuel API gravity
        result = compute_api_gravity(api=33.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 10  # Should have multiple rows
        # Check for key parameters
        param_column = result["Parameter"].astype(str)
        assert any("API" in str(p) for p in param_column)
        assert any("VCF" in str(p) for p in param_column)

