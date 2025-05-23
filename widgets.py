from .utils import playSfx
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from abc import ABC, abstractmethod
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QLineEdit, QProgressBar, QPushButton, QGraphicsDropShadowEffect, QSlider, 
    QTabWidget, QWidget, QFrame, QSizePolicy, QHBoxLayout, QLabel
)


"""
Text Input
"""
class FTextInput(QLineEdit):
    def __init__(self):
        super(FTextInput, self).__init__()
        self.setMinimumHeight(30)

"""
Progress Bar
"""
class FProgressBar(QProgressBar):
    def __init__(self, playSound: bool = False):
        super(FProgressBar, self).__init__()

        self.playSound = playSound
        self.setValue(0)
        self.setMaximumHeight(20)

        self.sfx = QSoundEffect()
        self.valueChanged.connect(self.onValueChanged)

    def onValueChanged(self, value: int):
        if self.playSound:
            playSfx(self.sfx, "progress_beep")


"""
Button
"""
class FButton(QPushButton):
    def __init__(self, label: str, role: str = "normal", parent=None):
        super().__init__(label)

        self.setProperty("role", role)
        self.setProperty("borderColor", "default")

        self.onClick = None
        self.sfx = QSoundEffect()

    def connect_func(self, func: callable, args: list = None, attach_sender: bool = False):
        def wrapper():
            playSfx(self.sfx, "click")
            if attach_sender and args is None:
                func(self)

            elif attach_sender and args is not None:
                func(self, *args)

            elif not attach_sender and args is not None:
                func(*args)

            elif not attach_sender and args is None:
                func()

        self.clicked.connect(wrapper)

    


"""
Slider
"""
class FSlider(QSlider):
    def __init__(self):
        super(FSlider, self).__init__()

        #self.setStyleSheet(styles.FSLIDER)
        self.setMinimumWidth(30)


"""
Tab Widget
"""
class FTabWidget(QTabWidget):
    def __init__(self):
        super(FTabWidget, self).__init__()

        #self.setStyleSheet(styles.FTAB)
        # self.setTabShape(QTabWidget.TabShape.Triangular)
        self.addTab(QWidget(), "CPU")
        self.addTab(QWidget(), "MEM")


class TitleBar(QFrame):
    def __init__(self, window):
        super(TitleBar, self).__init__()
        self.window = window
        self.layout = self.window.layout
        self.offset = None
        self.state = 2 # for windowed mode and 3 for maximum size

        # title bar
        # self.setStyleSheet(styles.TITLE_BAR)
        self.setObjectName("title-bar")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        # title bar layout
        self.title_bar_layout = QHBoxLayout()
        self.setLayout(self.title_bar_layout)

        # title text
        self.title_text = QLabel()
        self.title_text.setObjectName("win-title")
        # self.title_text.setStyleSheet(styles.TITLE_TEXT)
        self.title_bar_layout.addWidget(self.title_text)

        # hide window
        self.hide_win_btn = FButton("-", "normal")
        self.hide_win_btn.setProperty("borderColor", "default")
        self.hide_win_btn.setMaximumSize(30, 30)
        self.hide_win_btn.connect_func(self.hide_win)
        self.title_bar_layout.addWidget(self.hide_win_btn)

        # fullscreen btn
        self.win_state_btn = FButton("#", "normal")
        self.win_state_btn.setProperty("borderColor", "default")
        self.win_state_btn.setMaximumSize(30, 30)
        self.title_bar_layout.addWidget(self.win_state_btn)
        self.win_state_btn.connect_func(self.handleWinState)

        # close btn
        self.close_btn = FButton("X", "danger")
        self.close_btn.setProperty("borderColor", "default")
        self.close_btn.connect_func(self.close_win)
        self.close_btn.setMaximumSize(30, 30)
        self.title_bar_layout.addWidget(self.close_btn)


    def setTitle_(self, title: str):
        self.title_text.setText(title)

    def close_win(self):
        self.window.close()

    def handleWinState(self):
        if self.state == 2:
            self.window.hide()
            screen_geo = self.window.screen().availableGeometry()
            self.window.setMinimumSize(screen_geo.size())
            self.window.show()
            self.state = 3

        else:
            self.window.hide()
            self.window.setMinimumSize(800, 600)
            self.window.show()
            self.state = 2


    def hide_win(self):
        self.window.showMinimized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPosition().toPoint() - self.window.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.offset is not None:
            self.window.move(event.globalPosition().toPoint() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.offset = None
        event.accept()


class BaseDock(ABC):

    @abstractmethod
    def init_ui(self):
        pass

    @abstractmethod
    def add_app_to_dock(self, app_name: str):
        pass
    
    @abstractmethod
    def launch_app_from_dock(self, exec_str: str):
        pass

    @abstractmethod
    def add_icon_to_sys_tray(self, app_name: str, app_icon: QIcon):
        pass
