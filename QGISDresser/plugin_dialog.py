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

        resized_image = self._resize_image(mode="main", file_path=image_path)
        main_image = f"url({resized_image})"

        style_dict = self._generate_style_dict(
            char_color=char_color,
            treeview_color=tree_color,
            main_image=main_image,
        )

        return style_dict

    def _generate_style_dict(
        self,
        char_color: str,
        treeview_color: str,
        main_color: str = "transparent",
        main_image: str = "transparent",
        main_position: str = "left",
        button_color: str = "rgba(255, 255, 255, 0)",
        button_image: str = "transparent",
        button_position: str = "center",
    ) -> dict:
        """
        Generate a style dictionary for the QGISDresser plugin dialog.
        Arguments:
            main_image (str): Path to the main background image.
            char_color (str): Character color for the text.
            treeview_color (str): Background color for the tree view.
        Returns:
            dict: A dictionary containing style properties for various widgets.
        """
        # Icons
        clicked_image: str = os.path.join(
            os.path.dirname(__file__), "images", "icon-check.png"
        ).replace("\\", "/")
        toggle_image_closed: str = os.path.join(
            os.path.dirname(__file__),
            "images",
            f"icon-arrow-right-{char_color}.svg",
        ).replace("\\", "/")
        toggle_image_opened: str = os.path.join(
            os.path.dirname(__file__), "images", f"icon-arrow-down-{char_color}.svg"
        ).replace("\\", "/")

        # Style dictionary
        style_dict = {
            "QMainWindow": {
                "background-color": main_color,
                "background-image": main_image,
                "background-position": main_position,
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
                "background-color": button_color,
                "background-image": button_image,
                "background-position": button_position,
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
                "background-color": treeview_color,
            },
            "QTreeView:branch:selected:active": {
                "background-color": "rgba(0, 105, 255, 1.0)",
            },
            "QTreeView:branch:selected:!active": {
                "background-color": "rgba(200, 200, 200, 1.0)",
            },
            "QTreeView:branch:has-children:closed": {
                "image": f"url({toggle_image_closed})",
            },
            "QTreeView:branch:open:has-children": {
                "image": f"url({toggle_image_opened})",
            },
            "QTreeView:item": {
                "color": char_color,
            },
            "QTreeView:item:selected:active": {
                "color": "white",
                "background-color": "rgba(0, 105, 255, 1.0)",
            },
            "QTreeView:item:selected:!active": {
                "background-color": "rgba(200, 200, 200, 1.0)",
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

        style_dict = self._generate_style_dict(
            char_color=properties["char-color"],
            treeview_color=properties["treeview-color"],
            main_color=properties["main-color"],
            main_image=main_image,
            main_position=properties["main-position"],
            button_color=properties["btn-color"],
            button_image=btn_image,
            button_position=properties["btn-position"],
        )

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
