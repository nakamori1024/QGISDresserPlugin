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

import yaml
from PIL import Image
from PyQt5.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic


class QGISDresserGUI(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.ui = uic.loadUi(
            os.path.join(os.path.dirname(__file__), "plugin_dialog.ui"), self
        )

        # connect
        self.ui.buttonBox.rejected.connect(self.close)
        self.ui.buttonBox.accepted.connect(self.accept_style)
        self.ui.pushButtonApply.clicked.connect(self.apply_style)
        self.ui.radioButtonPreset.toggled.connect(self.change_groupbox_status)

        # load
        self.set_style_list()
        self.change_groupbox_status()

    def accept_style(self):
        self.apply_style()
        self.close()

    def apply_style(self):
        if self.ui.radioButtonPreset.isChecked():
            style_name: str = self.ui.comboBoxPreset.currentText()

            if style_name == "default":
                self.iface.mainWindow().setStyleSheet("")
                return

            style_dict: dict = self._get_style_properties(style_name)
        else:
            image_path: str = self.ui.qgsFileWidgetImage.filePath()

            if self.ui.radioButtonFontBlack.isChecked():
                char_color: str = "black"
            else:
                char_color: str = "white"

            if not os.path.exists(image_path):
                QMessageBox.information(self, "Message", "Image file not found.")
                return

            style_dict: dict = self._generate_image_properties(image_path, char_color)

        style_str: str = self._generate_stylesheet(style_dict)
        self.iface.mainWindow().setStyleSheet(style_str)

    def change_groupbox_status(self):
        checked = self.ui.radioButtonPreset.isChecked()

        self.ui.groupBoxPreset.setEnabled(checked)
        self.ui.groupBoxImage.setEnabled(not checked)

    def set_style_list(self):
        self.ui.comboBoxPreset.clear()
        self.ui.comboBoxPreset.addItem("default")

        style_list: list = self._load_list()
        self.ui.comboBoxPreset.addItems(style_list)

    def _generate_image_properties(self, image_path: str, char_color: str) -> dict:
        if char_color == "black":
            tree_color = "rgba(230, 230, 230, 0.6)"
        else:
            tree_color = "rgba(64, 64, 64, 0.6)"
        # todo: ツリー内の選択色、アクティブ/非アクティブの設定を入れる

        resized_image = self._resize_image(mode="main", file_path=image_path)
        main_image = f"url({resized_image})"

        clicked_image: str = os.path.join(
            os.path.dirname(__file__), "images", "icon-check.png"
        ).replace("\\", "/")

        style_dict = {
            "QMainWindow": {
                "background-color": "transparent",
                "background-image": main_image,
                "background-position": "left",
                "background-repeat": "no-repeat",
            },
            "QDockWidget": {
                "color": char_color,
            },
            "QMenuBar": {
                "color": char_color,
                "background-color": "transparent",
            },
            "QToolBar": {"background-color": "transparent"},
            "QToolButton": {
                "color": char_color,
                "background-color": "rgba(255, 255, 255, 0)",
                "background-image": "transparent",
                "background-position": "center",
            },
            "QToolButton:hover": {
                "background-color": "rgba(230, 230, 230, 0.6)",
            },
            "QToolButton:pressed": {
                "background-color": "rgba(220, 220, 220, 0.6)",
            },
            "QToolButton:checked": {
                "background-color": "rgba(220, 220, 220, 0.6)",
            },
            "QTreeView": {
                "color": char_color,
                "background-color": tree_color,
            },
            "QTreeView:branch": {"background-color": tree_color},
            "QTreeView:branch:selected:active": {
                "background-color": "rgba(255, 255, 0, 1.0)",
            },
            "QTreeView:branch:selected:!active": {
                "background-color": "rgba(255, 0, 0, 1.0)",
            },
            "QTreeView:item": {
                "color": char_color,
            },
            "QTreeView:item:selected:active": {
                "background-color": "rgba(255, 255, 0, 1.0)",
            },
            "QTreeView:item:selected:!active": {
                "background-color": "rgba(255, 0, 0, 1.0)",
            },
            "QTreeView:indicator:checked": {
                "background-color": "white",
                "border": "1px solid gray",
                "image": f"url({clicked_image})",
            },
            "QTreeView:indicator:unchecked": {
                "background-color": "white",
                "border": "1px solid gray",
            },
            "QLabel": {
                "color": char_color,
            },
            "QLineEdit": {
                "color": "black",
                "background-color": "rgba(255, 255, 255, 0.9)",
            },
            "QComboBox": {
                "color": "black",
                "background-color": "rgba(255, 255, 255, 0.9)",
            },
            "QDoubleSpinBox": {
                "color": "black",
                "background-color": "rgba(255, 255, 255, 0.9)",
            },
            "QCheckBox": {
                "color": char_color,
                "background-color": "transparent",
            },
        }

        return style_dict

    def _generate_stylesheet(self, styles: dict) -> str:
        stylesheet = ""
        for selector, properties in styles.items():
            stylesheet += f"{selector} {{\n"
            for prop, value in properties.items():
                stylesheet += f"    {prop}: {value};\n"
            stylesheet += "}\n"
        return stylesheet

    def _get_image_property(self, mode: str, property: str) -> str:
        file_path = os.path.join(
            os.path.dirname(__file__), "preset", "images", property
        )

        if os.path.exists(file_path):
            resized_image = self._resize_image(mode=mode, file_path=file_path)
            return_image = f"url({resized_image})"
        else:
            return_image = property

        return return_image

    def _get_style_properties(self, style_name: str) -> dict:
        yaml_file = os.path.join(os.path.dirname(__file__), "preset", "list.yml")
        with open(yaml_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        styles: list = data.get("styles", [])
        properties: dict = next(
            (item for item in styles if item["name"] == style_name), {}
        )

        main_image: str = self._get_image_property(
            mode="main", property=properties["main-image"]
        )
        btn_image: str = self._get_image_property(
            mode="btn", property=properties["btn-image"]
        )

        clicked_image: str = os.path.join(
            os.path.dirname(__file__), "images", "icon-check.png"
        ).replace("\\", "/")

        style_dict = {
            "QMainWindow": {
                "background-color": properties["main-color"],
                "background-image": main_image,
                "background-position": properties["main-position"],
                "background-repeat": "no-repeat",
            },
            "QDockWidget": {
                "color": properties["char-color"],
            },
            "QMenuBar": {
                "color": properties["char-color"],
                "background-color": "transparent",
            },
            "QToolBar": {"background-color": "transparent"},
            "QToolButton": {
                "background-color": properties["btn-color"],
                "background-image": btn_image,
                "background-position": properties["btn-position"],
            },
            "QToolButton:hover": {
                "background-color": "rgba(255, 255, 255, 0.6)",
            },
            "QToolButton:pressed": {
                "background-color": "rgba(128, 128, 128, 0.6)",
            },
            "QToolButton:checked": {
                "background-color": "rgba(255, 255, 255, 0.6)",
            },
            "QTreeView": {
                "color": properties["char-color"],
                "background-color": "rgba(128, 128, 128, 0.6)",
            },
            "QTreeView:item": {
                "color": properties["char-color"],
            },
            "QTreeView:indicator:checked": {
                "background-color": "white",
                "border": "1px solid gray",
                "image": f"url({clicked_image})",
            },
            "QTreeView:indicator:unchecked": {
                "background-color": "white",
                "border": "1px solid gray",
            },
            "QLabel": {
                "color": properties["char-color"],
            },
            "QLineEdit": {
                "color": "black",
                "background-color": "rgba(255, 255, 255, 0.9)",
            },
        }
        return style_dict

    def _image_url(self, file_name: str) -> str:
        file_path = os.path.join(
            os.path.dirname(__file__), "preset", "images", file_name
        )
        image_url = f"url({file_path})"
        return image_url

    def _load_list(self) -> list:
        preset_list = []

        yaml_file = os.path.join(os.path.dirname(__file__), "preset", "list.yml")
        with open(yaml_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        styles: list = data.get("styles", [])
        for style in styles:
            preset_list.append(style["name"])

        return preset_list

    def _resize_image(self, mode: str, file_path: str) -> str:
        # current window size
        size = self.iface.mainWindow().size()

        # get image
        image = Image.open(file_path)

        # resize
        resized_image = image.resize((size.width(), size.height()))
        resized_path = os.path.join(
            os.path.dirname(__file__), f"image_{mode}.png"
        ).replace("\\", "/")
        resized_image.save(resized_path)

        return resized_path
