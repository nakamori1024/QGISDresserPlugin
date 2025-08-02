"""Main plugin class"""

# Copyright (C) 2025 Shinsuke Nakamori
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os

from qgis.gui import QgisInterface
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .plugin_dialog import QGISDresserGUI

PLUGIN_NAME = "QGISDresser"


class QGISDresser:
    """QGIS plugin for dressing up its GUI."""

    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self.win = self.iface.mainWindow()
        self.action = QAction()

    def initGui(self):
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.add_action(
            callback=self.show_dialog, icon_path=icon_path, text="Open", parent=self.win
        )

    def unload(self):
        self.iface.removePluginMenu(PLUGIN_NAME, self.action)

    def add_action(self, callback, icon_path: str, text: str, parent):
        icon = QIcon(icon_path)
        self.action = QAction(icon, text, parent)
        self.action.triggered.connect(callback)
        self.iface.addPluginToMenu(PLUGIN_NAME, self.action)

    def show_dialog(self):
        self.dlg = QGISDresserGUI(iface=self.iface)
        self.dlg.show()
