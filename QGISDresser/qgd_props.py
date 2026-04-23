from qgis.PyQt.QtCore import QSettings
from qgis.PyQt.QtGui import QPixmap
import os.path

class QGISDresserProps:
    PREFIX = "QGISDresser"
    _instance = None

    DEFAULTS = {
        "main_image": "",
        "main_scale": "none",
        "main_repeat": "no-repeat",
        "main_position_x": "left",
        "main_position_y": "bottom",
        # styles
        "text_color": "",
        "menubar_background": "",
        "treeview_background": "rgba(255, 255, 255, 0.6)",
        "main_background": "",
        "button_background": "rgba(255, 255, 255, 0)",
        "button_image": "transparent",
        "button_position": "center",
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def __init__(self):
        pass

    def _init_once(self):
        self.settings = QSettings()
        self._apply_defaults()
        self._load()
        self._mk_pixmap()

    def _mk_pixmap(self):
        if os.path.isfile(self._main_image):
            self._pixmap = QPixmap(self._main_image)
        else:
            self._pixmap = QPixmap()

    def _apply_defaults(self):
        self._main_image = self.DEFAULTS["main_image"]
        self._main_scale = self.DEFAULTS["main_scale"]
        self._main_repeat = self.DEFAULTS["main_repeat"]
        self._main_position_x = self.DEFAULTS["main_position_x"]
        self._main_position_y = self.DEFAULTS["main_position_y"]
        self._text_color = self.DEFAULTS["text_color"]
        self._menubar_background = self.DEFAULTS["menubar_background"]
        self._treeview_background = self.DEFAULTS["treeview_background"]
        self._main_background = self.DEFAULTS["main_background"]
        self._button_background = self.DEFAULTS["button_background"]
        self._button_image = self.DEFAULTS["button_image"]
        self._button_position = self.DEFAULTS["button_position"]

    def _key(self, name):
        return f"{self.PREFIX}/{name}"

    def _load(self):
        self._main_image = str(self.settings.value(self._key("main_image"), self._main_image))
        self._main_scale = str(self.settings.value(self._key("main_scale"), self._main_scale))
        self._main_repeat = str(self.settings.value(self._key("main_repeat"), self._main_repeat))
        self._main_position_x = str(self.settings.value(self._key("main_position_x"), self._main_position_x))
        self._main_position_y = str(self.settings.value(self._key("main_position_y"), self._main_position_y))
        self._text_color = str(self.settings.value(self._key("text_color"), self._text_color))
        self._menubar_background = str(self.settings.value(self._key("menubar_background"), self._menubar_background))
        self._treeview_background = str(self.settings.value(self._key("treeview_background"), self._treeview_background))
        self._main_background = str(self.settings.value(self._key("main_background"), self._main_background))
        self._button_background = str(self.settings.value(self._key("button_background"), self._button_background))
        self._button_image = str(self.settings.value(self._key("button_image"), self._button_image))
        self._button_position = str(self.settings.value(self._key("button_position"), self._button_position))

    def _save(self, name, value):
        self.settings.setValue(self._key(name), value)

    def reload(self):
        self._load()
        self._mk_pixmap()

    def reset(self):
        self.main_image = self.DEFAULTS["main_image"]
        self.main_scale = self.DEFAULTS["main_scale"]
        self.main_repeat = self.DEFAULTS["main_repeat"]
        self.main_position_x = self.DEFAULTS["main_position_x"]
        self.main_position_y = self.DEFAULTS["main_position_y"]
        self.text_color = self.DEFAULTS["text_color"]
        self.menubar_background = self.DEFAULTS["menubar_background"]
        self.treeview_background = self.DEFAULTS["treeview_background"]
        self.main_background = self.DEFAULTS["main_background"]
        self.button_background = self.DEFAULTS["button_background"]
        self.button_image = self.DEFAULTS["button_image"]
        self.button_position = self.DEFAULTS["button_position"]
        self._mk_pixmap()
    # main_image
    @property
    def main_image(self):
        return self._main_image
    @main_image.setter
    def main_image(self, value):
        self._main_image = str(value)
        self._mk_pixmap()
        self._save("main_image", self._main_image)
    # main_scale
    @property
    def main_scale(self):
        return self._main_scale
    @main_scale.setter
    def main_scale(self, value):
        self._main_scale = str(value)
        self._save("main_scale", self._main_scale)
    # main_repeat
    @property
    def main_repeat(self):
        return self._main_repeat
    @main_repeat.setter
    def main_repeat(self, value):
        self._main_repeat = str(value)
        self._save("main_repeat", self._main_repeat)
    # main_position_x (horizontal)
    @property
    def main_position_x(self):
        return self._main_position_x
    @main_position_x.setter
    def main_position_x(self, value):
        self._main_position_x = str(value)
        self._save("main_position_x", self._main_position_x)
    # main_position_y (vertical)
    @property
    def main_position_y(self):
        return self._main_position_y
    @main_position_y.setter
    def main_position_y(self, value):
        self._main_position_y = str(value)
        self._save("main_position_y", self._main_position_y)
    # text_color (text color)
    @property
    def text_color(self):
        return self._text_color
    @text_color.setter
    def text_color(self, value):
        self._text_color = str(value)
        self._save("text_color", self._text_color)
    # menubar_background
    @property
    def menubar_background(self):
        return self._menubar_background
    @menubar_background.setter
    def menubar_background(self, value):
        self._menubar_background = str(value)
        self._save("menubar_background", self._menubar_background)
    # treeview_background
    @property
    def treeview_background(self):
        return self._treeview_background
    @treeview_background.setter
    def treeview_background(self, value):
        self._treeview_background = str(value)
        self._save("treeview_background", self._treeview_background)
    # main_background
    @property
    def main_background(self):
        return self._main_background
    @main_background.setter
    def main_background(self, value):
        self._main_background = str(value)
        self._save("main_background", self._main_background)
    # button_background
    @property
    def button_background(self):
        return self._button_background
    @button_background.setter
    def button_background(self, value):
        self._button_background = str(value)
        self._save("button_background", self._button_background)
    # button_image
    @property
    def button_image(self):
        return self._button_image
    @button_image.setter
    def button_image(self, value):
        self._button_image = str(value)
        self._save("button_image", self._button_image)
    # button_position
    @property
    def button_position(self):
        return self._button_position
    @button_position.setter
    def button_position(self, value):
        self._button_position = str(value)
        self._save("button_position", self._button_position)
    # pixmap ... not saved
    @property
    def pixmap(self):
        return self._pixmap
