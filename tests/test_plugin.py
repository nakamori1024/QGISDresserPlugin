"""Tests for QGISDresser plugin"""

from QGISDresser.plugin import QGISDresser


def test_plugin_initialization(qgis_iface):
    """Test plugin initialization"""
    plugin = QGISDresser(qgis_iface)
    assert plugin.iface == qgis_iface
    assert plugin.win == qgis_iface.mainWindow()
