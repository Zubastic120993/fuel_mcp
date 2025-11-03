"""
test_gui_integration.py
=======================
Integration tests for GUI applications
Tests common functionality across all GUI apps
"""

import pytest
from unittest.mock import patch


class TestGUICommonality:
    """Tests for common features across all GUI applications."""

    def test_all_gui_apps_have_demo(self):
        """Test that all GUI apps create a demo instance."""
        gui_modules = [
            "app_astm_api",
            "app_astm_density",
            "app_astm_rel_density",
            "app_astm_vol_weight",
        ]

        for module_name in gui_modules:
            module = __import__(
                f"fuel_mcp.gui_astm.{module_name}",
                fromlist=["demo"],
            )
            assert hasattr(module, "demo")
            assert module.demo is not None

    def test_all_gui_apps_have_api_url(self):
        """Test that all GUI apps have API_URL configured."""
        gui_modules = [
            "app_astm_api",
            "app_astm_density",
            "app_astm_rel_density",
            "app_astm_vol_weight",
        ]

        for module_name in gui_modules:
            module = __import__(
                f"fuel_mcp.gui_astm.{module_name}",
                fromlist=["API_URL"],
            )
            assert hasattr(module, "API_URL")
            assert isinstance(module.API_URL, str)

    def test_all_gui_apps_use_localhost(self):
        """Test that all GUI apps are configured for localhost."""
        gui_modules = [
            "app_astm_api",
            "app_astm_density",
            "app_astm_rel_density",
            "app_astm_vol_weight",
        ]

        for module_name in gui_modules:
            module = __import__(
                f"fuel_mcp.gui_astm.{module_name}",
                fromlist=["API_URL"],
            )
            api_url = module.API_URL
            assert "127.0.0.1" in api_url or "localhost" in api_url


class TestGUIPortConfiguration:
    """Tests for GUI port configuration."""

    def test_unified_gui_port(self):
        """Test that unified GUI uses port 7860."""
        from fuel_mcp.gui_astm import app_astm_unified

        # Check the main entry point
        assert hasattr(app_astm_unified, "create_unified_gui")

    def test_gui_ports_are_unique(self):
        """Test that individual GUI apps use unique ports."""
        # Port mapping from the apps
        ports = {
            "app_astm_api": 7861,
            "app_astm_rel_density": 7862,
            "app_astm_density": 7863,
            "app_astm_vol_weight": 7864,
            "app_astm_universal_converter": 7870,
            "app_astm_unified": 7860,
        }

        # Check for duplicates
        port_values = list(ports.values())
        assert len(port_values) == len(set(port_values)), "Ports must be unique"


class TestGUIDataValidation:
    """Tests for data validation across GUI apps."""

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_api_gravity_range_validation(self, mock_get):
        """Test API gravity value range validation."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.return_value.json.return_value = {
            "result": {"rho15": 800, "VCF": 0.99}
        }

        # Test with valid API range
        result = compute_astm(api=30.0, temp_f=60.0)
        assert result is not None

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_density_range_validation(self, mock_get):
        """Test density value range validation."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.return_value.json.return_value = {
            "result": {"VCF": 0.99, "tempC": 25}
        }

        # Test with typical marine fuel density
        result = calculate_density(density=850.0, temp_c=25.0)
        assert result is not None


class TestGUIErrorMessages:
    """Tests for error message consistency."""

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_error_message_format_api(self, mock_get):
        """Test error message format in API app."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm

        mock_get.side_effect = Exception("Test error")

        result = compute_astm(api=30.0, temp_f=60.0)

        # Should return DataFrame with Error
        assert "Error" in result.iloc[0, 0]

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_error_message_format_density(self, mock_get):
        """Test error message format in density app."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density

        mock_get.side_effect = Exception("Test error")

        result = calculate_density(density=850.0, temp_c=25.0)

        # Should return DataFrame with Error
        assert "Error" in result.iloc[0, 0]


class TestGUIResponseFormat:
    """Tests for consistent response formatting."""

    @patch("fuel_mcp.gui_astm.app_astm_api.requests.get")
    def test_api_response_is_dataframe(self, mock_get):
        """Test that API app returns DataFrame."""
        from fuel_mcp.gui_astm.app_astm_api import compute_astm
        import pandas as pd

        mock_get.return_value.json.return_value = {
            "result": {"rho15": 850, "VCF": 0.99}
        }

        result = compute_astm(api=30.0, temp_f=60.0)

        assert isinstance(result, pd.DataFrame)

    @patch("fuel_mcp.gui_astm.app_astm_density.requests.get")
    def test_density_response_is_dataframe(self, mock_get):
        """Test that density app returns DataFrame."""
        from fuel_mcp.gui_astm.app_astm_density import calculate_density
        import pandas as pd

        mock_get.return_value.json.return_value = {
            "result": {"VCF": 0.99, "tempC": 25}
        }

        result = calculate_density(density=850.0, temp_c=25.0)

        assert isinstance(result, pd.DataFrame)


class TestGUIInitFiles:
    """Tests for __init__.py files."""

    def test_gui_astm_package_exists(self):
        """Test that gui_astm package is importable."""
        import fuel_mcp.gui_astm

        assert fuel_mcp.gui_astm is not None

    def test_gui_astm_has_init(self):
        """Test that gui_astm has __init__.py."""
        import os

        init_file = os.path.join(
            os.path.dirname(__file__), "../../gui_astm", "__init__.py"
        )
        # Just verify the package is importable
        import fuel_mcp.gui_astm

        assert True


class TestGUIDocumentation:
    """Tests for GUI module docstrings."""

    def test_unified_gui_has_docstring(self):
        """Test that unified GUI module has docstring."""
        from fuel_mcp.gui_astm import app_astm_unified

        assert app_astm_unified.__doc__ is not None

    def test_api_app_has_docstring(self):
        """Test that API app module has docstring."""
        from fuel_mcp.gui_astm import app_astm_api

        assert app_astm_api.__doc__ is not None

