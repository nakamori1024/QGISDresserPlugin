from qgis.PyQt.QtCore import QUrl

from .qgd_props import QGISDresserProps
import os

class QGISDresserStyleSheetGenerator:
    def generate_stylesheet(self) -> str:
        props = QGISDresserProps()
        style_dict = self._generate_style_dict(props)
        stylesheet = ""
        for selector, properties in style_dict.items():
            stylesheet += f"{selector} {{\n"
            for prop, value in properties.items():
                stylesheet += f"    {prop}: {value};\n"
            stylesheet += "}\n"
        return stylesheet

    def _generate_style_dict(self, props) -> dict:
        """
        Generate a style dictionary for the QGISDresser plugin dialog.
        Arguments:
            main_image (str): Path to the main background image.
            text_color (str): Character color for the text.
            treeview_background (str): Background color for the tree view.
        Returns:
            dict: A dictionary containing style properties for various widgets.
        """
        # variable
        text_color = props.text_color
        # Icons
        clicked_image: str = os.path.join(
            os.path.dirname(__file__), "images", "icon-check.png"
        ).replace("\\", "/")
        toggle_image_closed: str = os.path.join(
            os.path.dirname(__file__),
            "images",
            f"icon-arrow-right-{text_color}.svg",
        ).replace("\\", "/")
        toggle_image_opened: str = os.path.join(
            os.path.dirname(__file__), "images", f"icon-arrow-down-{text_color}.svg"
        ).replace("\\", "/")
        btn_image: str = self._get_button_image_property(props.button_image)
        # Style dictionary
        style_dict = {
            "QMainWindow": {
                "background-color": props.main_background,
            },
            "QDockWidget": {
                "color": text_color,
            },
            "QMenuBar": {
                "color": text_color,
                "background-color": props.menubar_background,
            },
            "QToolBar": {
                "background-color": "transparent",
            },
            "QToolButton": {
                "color": text_color,
                "background-color": props.button_background,
                "background-image": props.button_image,
                "background-position": props.button_position,
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
                "color": text_color,
                "background-color": props.treeview_background,
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
                "color": text_color,
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
                "color": text_color,
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
                "color": text_color,
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

    def _get_button_image_property(self, value: str) -> str:
        file_path = os.path.join(
            os.path.dirname(__file__), "preset", "images", value
        )
        if os.path.exists(file_path):
            return QUrl.fromLocalFile(file_path).toString()
        else:
            return value
