"""Test configuration for QGISDresser plugin"""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def qgis_iface():
    """Create mock QGIS interface for testing"""
    iface = MagicMock()
    iface.mainWindow.return_value = MagicMock()
    return iface
