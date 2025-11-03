"""
test_app_astm_universal_converter.py
=====================================
Tests for Universal ASTM Converter (app_astm_universal_converter.py)
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestSmartConvert:
    """Tests for smart_convert function."""

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_smart_convert_mass_units(self, mock_convert):
        """Test conversion between mass units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_convert.return_value = 1.0

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Metric Tons (tonne)",
            value="1000",
        )

        assert isinstance(result, str)
        assert "1.0" in result
        assert source is not None

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_smart_convert_volume_units(self, mock_convert):
        """Test conversion between volume units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_convert.return_value = 264.172

        result, source = smart_convert(
            group="Volume / Capacity 🧴",
            from_label="Cubic Metres (m³)",
            to_label="US Gallons",
            value="1",
        )

        assert "264.172" in result
        assert "ASTM" in source

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_smart_convert_length_units(self, mock_convert):
        """Test conversion between length units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_convert.return_value = 3.28084

        result, source = smart_convert(
            group="Length 📏",
            from_label="Metres (m)",
            to_label="Feet (ft)",
            value="1",
        )

        assert "3.28" in result

    def test_smart_convert_invalid_value(self):
        """Test conversion with invalid numeric value."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Pounds (lb)",
            value="not_a_number",
        )

        assert "Invalid" in result or "❌" in result

    def test_smart_convert_missing_group(self):
        """Test conversion with missing group."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        result, source = smart_convert(
            group=None,
            from_label="Kilograms (kg)",
            to_label="Pounds (lb)",
            value="100",
        )

        assert "⚠️" in result or "Please select" in result

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_smart_convert_api_density_correlation(self, mock_convert):
        """Test API/Density correlation."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        with patch("fuel_mcp.gui_astm.app_astm_universal_converter.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                "result": {
                    "outputs": {
                        "density_15c_kg_per_m3": 876.0,
                        "relative_density_60f": 0.8762,
                        "api_gravity_60f": 30.0,
                    }
                }
            }

            result, source = smart_convert(
                group="API & Density 🧪",
                from_label="API Gravity (60°F)",
                to_label="Density (kg/m³)",
                value="30",
            )

            # Should return density value
            assert "876" in result or "kg/m³" in result


class TestListEquivalents:
    """Tests for list_equivalents function."""

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_list_equivalents_mass(self, mock_convert):
        """Test listing equivalent mass units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import list_equivalents

        mock_convert.side_effect = [2204.62, 1.0, 1.102, 0.984]  # Mock conversions

        result = list_equivalents(
            group="Mass / Weight ⚖️", from_label="Kilograms (kg)", value="1000"
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_list_equivalents_invalid_value(self):
        """Test list equivalents with invalid value."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import list_equivalents

        result = list_equivalents(
            group="Mass / Weight ⚖️", from_label="Kilograms (kg)", value="invalid"
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0  # Should return empty DataFrame

    def test_list_equivalents_missing_group(self):
        """Test list equivalents with missing group."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import list_equivalents

        result = list_equivalents(group=None, from_label="Kilograms (kg)", value="100")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 0


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_labelize(self):
        """Test unit labeling."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import labelize

        assert "Kilograms" in labelize("kg")
        assert "Pounds" in labelize("lb")
        assert "Cubic Metres" in labelize("m3")
        assert "Litres" in labelize("litre")

    def test_normalize_label(self):
        """Test label normalization."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import normalize_label, UNIT_LABELS

        # Test that normalize_label function exists and processes labels
        result_kg = normalize_label("Kilograms (kg)")
        result_lb = normalize_label("Pounds (lb)")
        result_m3 = normalize_label("Cubic Metres (m³)")
        
        # Function should return some normalized form
        assert result_kg is not None
        assert result_lb is not None
        assert result_m3 is not None
        
        # Results should be usable (either matched key or normalized label)
        assert len(result_kg) > 0
        assert len(result_lb) > 0
        assert len(result_m3) > 0


class TestUnitGroups:
    """Tests for unit group configuration."""

    def test_unit_groups_defined(self):
        """Test that unit groups are properly defined."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import UNIT_GROUPS

        assert "Mass / Weight ⚖️" in UNIT_GROUPS
        assert "Volume / Capacity 🧴" in UNIT_GROUPS
        assert "Length 📏" in UNIT_GROUPS
        assert "API & Density 🧪" in UNIT_GROUPS

    def test_mass_units_complete(self):
        """Test that mass units group contains expected units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import UNIT_GROUPS

        mass_units = UNIT_GROUPS["Mass / Weight ⚖️"]
        assert "kg" in mass_units
        assert "lb" in mass_units
        assert "tonne" in mass_units

    def test_volume_units_complete(self):
        """Test that volume units group contains expected units."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import UNIT_GROUPS

        volume_units = UNIT_GROUPS["Volume / Capacity 🧴"]
        assert "litre" in volume_units
        assert "usg" in volume_units
        assert "barrel" in volume_units
        assert "m3" in volume_units

    def test_unit_labels_complete(self):
        """Test that all units have readable labels."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import (
            UNIT_GROUPS,
            UNIT_LABELS,
        )

        for group_units in UNIT_GROUPS.values():
            for unit in group_units:
                if unit not in ["API", "Density", "Rel.Density"]:  # Special cases
                    assert unit in UNIT_LABELS


class TestGradioInterface:
    """Tests for Gradio interface."""

    def test_gui_function_exists(self):
        """Test that GUI function exists."""
        from fuel_mcp.gui_astm import app_astm_universal_converter

        assert hasattr(app_astm_universal_converter, "gui")

    def test_gui_creates_demo(self):
        """Test that GUI function creates a demo."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import gui

        demo = gui()
        assert demo is not None
        assert hasattr(demo, "launch")


class TestAPIIntegration:
    """Tests for API integration."""

    def test_api_base_configured(self):
        """Test that API base URL is configured."""
        from fuel_mcp.gui_astm import app_astm_universal_converter

        assert hasattr(app_astm_universal_converter, "API_BASE")
        assert isinstance(app_astm_universal_converter.API_BASE, str)

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.requests.get")
    def test_api_correlation_endpoint_called(self, mock_get):
        """Test that correlation endpoint is called for API/Density conversions."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "outputs": {"density_15c_kg_per_m3": 876.0}
            }
        }

        smart_convert(
            group="API & Density 🧪",
            from_label="API Gravity (60°F)",
            to_label="Density (kg/m³)",
            value="30",
        )

        # Verify API was called
        mock_get.assert_called()


class TestErrorHandling:
    """Tests for error handling."""

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.convert")
    def test_conversion_error_handling(self, mock_convert):
        """Test error handling in conversion."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_convert.side_effect = Exception("Conversion error")

        result, source = smart_convert(
            group="Mass / Weight ⚖️",
            from_label="Kilograms (kg)",
            to_label="Pounds (lb)",
            value="100",
        )

        assert "⚠️" in result

    @patch("fuel_mcp.gui_astm.app_astm_universal_converter.requests.get")
    def test_api_error_handling(self, mock_get):
        """Test API error handling for density correlation."""
        from fuel_mcp.gui_astm.app_astm_universal_converter import smart_convert

        mock_get.side_effect = Exception("API error")

        result, source = smart_convert(
            group="API & Density 🧪",
            from_label="API Gravity (60°F)",
            to_label="Density (kg/m³)",
            value="30",
        )

        # Should handle error gracefully
        assert result is not None

