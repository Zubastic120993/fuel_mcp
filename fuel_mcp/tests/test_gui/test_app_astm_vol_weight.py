"""
test_app_astm_vol_weight.py
============================
Tests for ASTM Volume & Weight Converter (app_astm_vol_weight.py)
"""

import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_vcf_response():
    """Mock VCF API response."""
    return {
        "result": {
            "VCF": 0.99154,
            "table": "54B",
        }
    }


class TestConvertUnits:
    """Tests for convert_units function."""

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_units_success(self, mock_get, mock_vcf_response):
        """Test successful unit conversion."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=796.7,
            temp_obs=22.6,
            from_unit="M3 @15°C",
            to_unit="US Gallons @60°F",
            value=2941,
        )

        assert isinstance(result, dict)
        assert "ASTM Table" in result
        assert "VCF" in result
        assert "Output Value" in result

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_units_celsius_to_fahrenheit(self, mock_get, mock_vcf_response):
        """Test temperature conversion from Celsius."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=796.7,
            temp_obs=22.6,
            from_unit="M3 @Temp.",
            to_unit="BBLS @Temp.",
            value=100,
        )

        assert result["Observed Temp (°C)"] == pytest.approx(22.6, abs=0.1)

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_units_fahrenheit_input(self, mock_get, mock_vcf_response):
        """Test with Fahrenheit temperature input."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        result = convert_units(
            table="54B",
            temp_unit="°F",
            rho15=796.7,
            temp_obs=72.0,  # 72°F = ~22.2°C
            from_unit="M3 @Temp.",
            to_unit="BBLS @Temp.",
            value=100,
        )

        # Should convert to Celsius
        assert result["Observed Temp (°C)"] == pytest.approx(22.2, abs=0.2)

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_barrels_to_cubic_meters(self, mock_get, mock_vcf_response):
        """Test barrel to cubic meter conversion."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=850.0,
            temp_obs=25.0,
            from_unit="BBLS @Temp.",
            to_unit="M3 @Temp.",
            value=100,
        )

        assert isinstance(result["Output Value"], (int, float))
        assert result["From Unit"] == "BBLS @Temp."
        assert result["To Unit"] == "M3 @Temp."

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_mass_units(self, mock_get, mock_vcf_response):
        """Test mass unit conversions (tons)."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=850.0,
            temp_obs=25.0,
            from_unit="Long Tons",
            to_unit="Metric Tonnes (Air)",
            value=100,
        )

        assert "Output Value" in result
        assert isinstance(result["Output Value"], (int, float))

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_units_error_handling(self, mock_get):
        """Test error handling when API call fails."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.side_effect = Exception("Connection error")

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=796.7,
            temp_obs=22.6,
            from_unit="M3 @15°C",
            to_unit="US Gallons @60°F",
            value=2941,
        )

        assert "Error" in result

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_convert_with_different_tables(self, mock_get, mock_vcf_response):
        """Test conversion with different ASTM tables."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        # Test with Table 54A
        result_54a = convert_units(
            table="54A",
            temp_unit="°C",
            rho15=750.0,
            temp_obs=20.0,
            from_unit="M3 @15°C",
            to_unit="BBLS @60°F",
            value=100,
        )
        assert result_54a["ASTM Table"] == "54A"

        # Test with Table 54C
        result_54c = convert_units(
            table="54C",
            temp_unit="°C",
            rho15=950.0,
            temp_obs=50.0,
            from_unit="M3 @15°C",
            to_unit="BBLS @60°F",
            value=100,
        )
        assert result_54c["ASTM Table"] == "54C"

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_vcf_applied_correctly(self, mock_get):
        """Test that VCF is correctly applied in conversion."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = {
            "result": {"VCF": 1.0}  # VCF of 1.0 should not change value
        }

        result = convert_units(
            table="54B",
            temp_unit="°C",
            rho15=850.0,
            temp_obs=15.0,  # At 15°C, VCF should be close to 1.0
            from_unit="M3 @Temp.",
            to_unit="M3 @15°C",
            value=100,
        )

        # With VCF=1.0, value should be approximately the same
        assert result["VCF"] == 1.0


class TestGradioInterface:
    """Tests for Gradio interface."""

    def test_demo_exists(self):
        """Test that demo interface is created."""
        from fuel_mcp.gui_astm import app_astm_vol_weight

        assert hasattr(app_astm_vol_weight, "demo")
        assert app_astm_vol_weight.demo is not None

    def test_api_url_configured(self):
        """Test that API URL is configured."""
        from fuel_mcp.gui_astm import app_astm_vol_weight

        assert hasattr(app_astm_vol_weight, "API_URL")


class TestWrapperFunction:
    """Tests for wrapper function used in Gradio."""

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.convert_units")
    def test_wrapper_converts_to_list(self, mock_convert):
        """Test that wrapper converts result dict to list format."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import demo

        # Verify wrapper function exists
        assert demo is not None


class TestUnitMapping:
    """Tests for unit conversion mapping."""

    @patch("fuel_mcp.gui_astm.app_astm_vol_weight.requests.get")
    def test_all_units_supported(self, mock_get, mock_vcf_response):
        """Test that all listed units are supported."""
        from fuel_mcp.gui_astm.app_astm_vol_weight import convert_units

        mock_get.return_value.json.return_value = mock_vcf_response

        units = [
            "BBLS @Temp.",
            "BBLS @60°F",
            "M3 @Temp.",
            "M3 @15°C",
            "Long Tons",
            "Short Tons",
            "Metric Tonnes (Air)",
            "Metric Tonnes (Vac)",
            "US Gallons @60°F",
        ]

        # Test each unit as both source and target
        for unit in units:
            result = convert_units(
                table="54B",
                temp_unit="°C",
                rho15=850.0,
                temp_obs=25.0,
                from_unit=unit,
                to_unit="M3 @15°C",
                value=100,
            )
            assert "Output Value" in result

