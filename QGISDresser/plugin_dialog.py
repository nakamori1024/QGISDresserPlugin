"""Plugin dialog class"""

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

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog, QColorDialog
from qgis.PyQt.QtCore import QCoreApplication, pyqtSignal, QDir, QTimer, Qt

from .qgd_props import QGISDresserProps

class QGISDresserDialog(QDialog):
    applyRequested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dialog = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "plugin_dialog.ui"), self
        )
        if self.dialog is None:
            raise RuntimeError("Failed loading UI file.")
        self._presets = self._get_presets()
        self.btnAdvancedToggle.setChecked(False)
        # initializes status
        self._on_advanced()
        self._init_widgets()
        self._connect_signals()

    def _init_widgets(self):
        self.cmbPresets.clear()
        self.cmbPresets.addItem("","")
        if self._presets is not None:
            for key, value in self._presets.items():
                if "title" in value:
                    title = value["title"]
                else:
                    title = key
                self.cmbPresets.addItem(self.tr(title), key)
        self.cmbMainScale.clear()
        self.cmbMainScale.addItem(self.tr("None"), "none")
        self.cmbMainScale.addItem(self.tr("Fit (Smaller)"), "fit_smaller")
        self.cmbMainScale.addItem(self.tr("Fit (Larger)"), "fit_larger")
        self.cmbMainScale.addItem(self.tr("Shrink (Smaller)"), "shrink_smaller")
        self.cmbMainScale.addItem(self.tr("Shrink (Larger)"), "shrink_larger")
        self.cmbMainScale.addItem(self.tr("Stretch"), "stretch")
        self.cmbMainRepeat.clear()
        self.cmbMainRepeat.addItem(self.tr("None"), "no-repeat")
        self.cmbMainRepeat.addItem(self.tr("X"), "repeat-x")
        self.cmbMainRepeat.addItem(self.tr("Y"), "repeat-y")
        self.cmbMainRepeat.addItem(self.tr("X/Y"), "repeat")
        self.cmbMainPositionX.clear()
        self.cmbMainPositionX.addItem(self.tr("Left"), "left")
        self.cmbMainPositionX.addItem(self.tr("Center"), "center")
        self.cmbMainPositionX.addItem(self.tr("Right"), "right")
        self.cmbMainPositionY.clear()
        self.cmbMainPositionY.addItem(self.tr("Top"), "top")
        self.cmbMainPositionY.addItem(self.tr("Middle"), "middle")
        self.cmbMainPositionY.addItem(self.tr("Bottom"), "bottom")

    def _on_advanced(self):
        checked = self.btnAdvancedToggle.isChecked()
        # changes button
        if checked:
            self.btnAdvancedToggle.setArrowType(Qt.ArrowType.DownArrow)
        else:
            self.btnAdvancedToggle.setArrowType(Qt.ArrowType.RightArrow)
        self.btnAdvancedToggle.setText(self.tr("Advanced Settings"))
        # shows/hide advanced settings
        self.groupAdvanced.setVisible(checked)
        self.btnAdvancedToggle.updateGeometry()
        self.updateGeometry()
        layout = self.layout()
        if layout is not None:
            layout.invalidate()
            layout.activate()
        QTimer.singleShot(0, self._adjust_dialog_size)

    def _adjust_dialog_size(self):
        w = self.width()
        h = self.sizeHint().height()
        self.setMinimumSize(0, 0)
        self.adjustSize()
        self.resize(w, h)

    def _connect_signals(self):
        self.cmbPresets.currentIndexChanged.connect(self.on_preset)
        self.btnPresets.clicked.connect(self.on_preset)
        self.btnMainImage.clicked.connect(self.on_browse_image)
        self.btnAdvancedToggle.toggled.connect(self._on_advanced)
        self.btnTextColor.clicked.connect(
            lambda: self.select_color_for(self.txtTextColor)
        )
        self.btnMenubarBackground.clicked.connect(
            lambda: self.select_color_for(self.txtMenubarBackground)
        )
        self.btnTreeviewBackground.clicked.connect(
            lambda: self.select_color_for(self.txtTreeviewBackground)
        )
        self.btnMainBackground.clicked.connect(
            lambda: self.select_color_for(self.txtMainBackground)
        )
        self.btnButtonBackground.clicked.connect(
            lambda: self.select_color_for(self.txtButtonBackground)
        )
        self.btnOk.clicked.connect(self.on_ok)
        self.btnCancel.clicked.connect(self.dialog.reject)
        self.btnApply.clicked.connect(self.on_apply)
        self.cmbMainScale.currentTextChanged.connect(self.on_style_changed)
        self.cmbMainRepeat.currentTextChanged.connect(self.on_style_changed)
        self.cmbMainPositionX.currentTextChanged.connect(self.on_style_changed)
        self.cmbMainPositionY.currentTextChanged.connect(self.on_style_changed)

    def _init_values(self):
        prop = QGISDresserProps()
        self.txtMainImage.setText(prop.main_image)
        self._set_combo_data(self.cmbMainScale, prop.main_scale)
        self._set_combo_data(self.cmbMainRepeat, prop.main_repeat)
        self._set_combo_data(self.cmbMainPositionX, prop.main_position_x)
        self._set_combo_data(self.cmbMainPositionY, prop.main_position_y)
        self.txtTextColor.setText(prop.text_color)
        self.txtMainBackground.setText(prop.main_background)
        self.txtMenubarBackground.setText(prop.menubar_background)
        self.txtTreeviewBackground.setText(prop.treeview_background)
        self.txtButtonBackground.setText(prop.button_background)
        # advanced button
        self.btnAdvancedToggle.setChecked(False)

    def _update_values(self, data):
        self.txtMainImage.setText(data["main_image"])
        self._set_combo_data(self.cmbMainScale, data["main_scale"])
        self._set_combo_data(self.cmbMainRepeat, data["main_repeat"])
        self._set_combo_data(self.cmbMainPositionX, data["main_position_x"])
        self._set_combo_data(self.cmbMainPositionY, data["main_position_y"])
        self.txtTextColor.setText(data["text_color"])
        self.txtMainBackground.setText(data["main_background"])
        self.txtMenubarBackground.setText(data["menubar_background"])
        self.txtTreeviewBackground.setText(data["treeview_background"])
        self.txtButtonBackground.setText(data["button_background"])

    # Called when the dialog shown
    def showEvent(self, event):
        super().showEvent(event)
        self.cmbPresets.setCurrentIndex(-1)
        self._init_values()

    def _set_combo_data(self, combo, value):
        index = combo.findData(value)
        if index != -1:
            combo.setCurrentIndex(index)

    def _get_combo_data(self, combo):
        data = combo.currentData()
        return data if data is not None else ""

    def tr(self, message):
        return QCoreApplication.translate("QGISDresserDialog", message)

    def on_preset(self):
        key = self._get_combo_data(self.cmbPresets)
        if not key in self._presets:
            return
        preset = self._presets[key]
        if preset is None:
            return
        self._update_values(preset)

    def on_browse_image(self):
        # gets current path -> cur
        txt = self.txtMainImage.text()
        if os.path.isdir(txt):
            cur = txt
        elif os.path.isfile(txt):
            cur = os.path.dirname(txt)
        else:
            cur = QDir.homePath()
        # opens filedialog
        path, _ = QFileDialog.getOpenFileName(
            self.dialog,
            self.tr("Choose an image"),
            cur,
            self.tr("Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        )
        if path:
            self.txtMainImage.setText(path)

    def select_color_for(self, line_edit):
        from qgis.PyQt.QtGui import QColor
        color = QColorDialog.getColor(
            parent=self.dialog,
            options=QColorDialog.ColorDialogOption.ShowAlphaChannel
        )
        if color.isValid():
            line_edit.setText(color.name(QColor.NameFormat.HexArgb))  # 例: #ff0000

    def on_style_changed(self, _value):
        # コンボ変更時の処理
        # print("スタイル設定が変更されました")
        pass

    def on_apply(self):
        prop = QGISDresserProps()
        prop.main_image = self.txtMainImage.text()
        prop.main_scale = self._get_combo_data(self.cmbMainScale)
        prop.main_repeat = self._get_combo_data(self.cmbMainRepeat)
        prop.main_position_x = self._get_combo_data(self.cmbMainPositionX)
        prop.main_position_y = self._get_combo_data(self.cmbMainPositionY)
        prop.text_color = self.txtTextColor.text()
        prop.menubar_background = self.txtMenubarBackground.text()
        prop.treeview_background = self.txtTreeviewBackground.text()
        prop.main_background = self.txtMainBackground.text()
        prop.button_background = self.txtButtonBackground.text()
        self.applyRequested.emit()
        # clears preset selection.
        self.cmbPresets.setCurrentIndex(-1)

    def on_ok(self):
        self.on_apply()
        self.dialog.accept()

    def collect_settings(self):
        return {
            "main_image": self.txtMainImage.text(),
            "main_scale": self.cmbMainScale.currentData(),
            "main_repeat": self.cmbMainRepeat.currentData(),
            "main_position_x": self.cmbMainPositionX.currentData(),
            "main_position_y": self.cmbMainPositionY.currentData(),
            "text_color": self.txtTextColor.text(),
            "menubar_background": self.txtMenubarBackground.text(),
            "treeview_background": self.txtTreeviewBackground.text(),
            "main_background": self.txtMainBackground.text(),
            "button_background": self.txtButtonBackground.text(),
        }
    #
    def _get_presets(self) -> dict:
        import json
        json_path = os.path.join(os.path.dirname(__file__), "preset", "list.json")
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if data is None:
            return None
        # filenaem to full path
        for key in data.keys():
            style = data[key]
            if style is not None:
                for subkey in ("main_image", "button_image"):
                    if subkey in style and style[subkey] is not None and style[subkey] != "":
                        path = os.path.join(os.path.dirname(__file__), "preset", "images", style[subkey])
                        if os.path.isfile(path):
                            style[subkey] = path
        return data
