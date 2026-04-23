"""Plugin main class"""

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
from qgis.PyQt.QtWidgets import QDialog, QMessageBox
from qgis.PyQt import uic
# log
from qgis.core import QgsMessageLog, Qgis

from qgis.PyQt.QtCore import QObject, QEvent, Qt, QRect
from qgis.PyQt.QtGui import QPainter, QColor, QPixmap
from qgis.PyQt.QtWidgets import QWidget

import math # ceil

from .qgd_props import QGISDresserProps

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        props = QGISDresserProps()
        # is null ?
        if props.pixmap.isNull():
            return
        # view calculation (logical pixel)
        # pixmap.width() and pixmap.height() are transformed into logical pixels.
        pm_ratio = props.pixmap.devicePixelRatio()
        vw, vh = self.width(), self.height()
        iw, ih = props.pixmap.width()/pm_ratio, props.pixmap.height()/pm_ratio
        rw, rh = vw/iw, vh/ih # rate ... scale candidate
        # scale
        if props.main_scale == "fit_larger":
            sw = sh = rw if rw > rh else rh
        elif props.main_scale == "fit_smaller":
            sw = sh = rw if rw < rh else rh
        elif props.main_scale == "stretch":
            sw, sh = rw, rh
        elif props.main_scale == "shrink_larger":
            sc = rw if rw > rh else rh
            sw = sh = 1 if sc > 1 else sc
        elif props.main_scale == "shrink_smaller":
            sc = rw if rw < rh else rh
            sw = sh = 1 if sc > 1 else sc
        else: # none
            # considers rate of device ratio (logical pixels / physical pixels) and pixmap ratio
            dv_ratio = self.devicePixelRatioF()
            if dv_ratio > 0.:
                sw, sh = pm_ratio/dv_ratio, pm_ratio/dv_ratio
            else:
                sw, sh = 1., 1.
        # drawing area (single)
        dw, dh = int(sw*iw), int(sh*ih)
        if not (dw >= 1 and dh >= 1):
            return
        # Left of single image.
        if "center" in props.main_position_x:
            # (x+dw/2) = vw/2
            x = int((vw-dw)/2)
        elif "right" in props.main_position_x:
            x =  vw-dw
        else: # "left"
            x = 0
        # Top of single image.
        if "middle" in props.main_position_y:
            y = int((vh-dh)/2)
        elif "bottom" in props.main_position_y:
            y =  vh-dh
        else: # "top"
            y = 0
        # repeat
        rect = event.rect() if event is not None else None
        if rect is not None:
            minx = rect.left()
            miny = rect.top()
            maxx = rect.right()
            maxy = rect.bottom()
        else:
            # maxx = width-1, maxy = height-1
            minx,miny,maxx,maxy = 0,0,vw-1,vh-1
        main_repeat = props.main_repeat
        if main_repeat in ("repeat", "repeat-x", "repeat-xy"):
            x0 = ((minx-x) // dw) * dw + x
            xs = range(x0, maxx+1, dw)
        else:
            xs = () if x + dw <= minx or x > maxx else (x,)
        if main_repeat in ("repeat", "repeat-y", "repeat-xy"):
            y0 = ((miny-y) // dh) * dh + y
            ys = range(y0, maxy+1, dh)
        else:
            ys = () if y + dh <= miny or y > maxy else (y,)
        # draws
        p = QPainter(self)
        try:
            for x in xs:
                for y in ys:
                    p.drawPixmap(QRect(x, y, dw, dh), props.pixmap)
        finally:
            p.end()
        # print(len(xs), len(ys))

class MainWindowResizeFilter(QObject):
    def __init__(self, bg_widget):
        super().__init__()
        self.bg_widget = bg_widget

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            self.bg_widget.setGeometry(obj.rect())
            self.bg_widget.lower()
            self.bg_widget.update()
        return False
