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

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QTimer

from .qgd_bgwidget import BackgroundWidget, MainWindowResizeFilter
from .qgd_props import QGISDresserProps
from .qgd_stylegen import QGISDresserStyleSheetGenerator

from .plugin_dialog import QGISDresserDialog

PLUGIN_NAME = "QGISDresser"


class QGISDresser:
    """QGIS plugin for dressing up its GUI."""

    def __init__(self, iface: QgisInterface):
        self.iface = iface
        self._init_locale()
        self.win = self.iface.mainWindow()
        self.action = QAction()

    def initGui(self):
        # reads property
        props = QGISDresserProps()
        props.reload()
        # reads icon in menu
        icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        self.add_action(
            callback=self.show_dialog, icon_path=icon_path, text="Open", parent=self.win
        )
        # BackgroundWidget
        mw = self.iface.mainWindow()
        self.bg_widget = BackgroundWidget(mw)
        self.bg_widget.setGeometry(mw.rect())
        self.bg_widget.show()
        self.bg_widget.lower()
        self.resize_filter = MainWindowResizeFilter(self.bg_widget)
        self.dlg = None
        QTimer.singleShot(0, self.apply_style)
        mw.installEventFilter(self.resize_filter)

    def unload(self):
        # removes a menu
        self.iface.removePluginMenu(PLUGIN_NAME, self.action)
        # purges styles
        self.iface.mainWindow().setStyleSheet("")
        # BackgroundWidget
        mw = self.iface.mainWindow()
        if getattr(self,"resize_filter", None) is not  None:
            mw.removeEventFilter(self.resize_filter)
            self.resize_filter = None
        if getattr(self,"bg_widget", None) is not  None:
            self.bg_widget.hide()
            self.bg_widget.deleteLater()
            self.bg_widget = None
        # dialog
        if getattr(self, "dlg", None) is not None:
            try:
                self.dlg.close()
            except Exception:
                pass
            try:
                self.dlg.deleteLater()
            except Exception:
                pass
            self.dlg = None

    def add_action(self, callback, icon_path: str, text: str, parent):
        icon = QIcon(icon_path)
        self.action = QAction(icon, text, parent)
        self.action.triggered.connect(callback)
        self.iface.addPluginToMenu(PLUGIN_NAME, self.action)

    def show_dialog(self):
        if self.dlg is None:
            self.dlg = QGISDresserDialog()
            self.dlg.applyRequested.connect(self.apply_style)
        self.dlg.show()

    def apply_style(self):
        gen = QGISDresserStyleSheetGenerator()
        stylesheet:str = gen.generate_stylesheet()
        self.iface.mainWindow().setStyleSheet(stylesheet)
        if self.bg_widget is not None:
            self.bg_widget.update()

    def _init_locale(self):
        locale = str(QSettings().value("locale/userLocale", "en"))[0:2]
        locale_path = os.path.join(
            os.path.dirname(__file__),
            "i18n",
            f"qgisdresser_{locale}.qm"
        )
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)
