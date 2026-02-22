import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView

def apply_superlite_xp():
    """
    SuperLite dành cho Windows XP (Luna style)
    """
    chromium_flags = [
        "--enable-low-end-device-mode",
        "--renderer-process-limit=2",
        "--disable-background-networking",
        "--disable-gpu",  # XP thường driver yếu
    ]
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(chromium_flags)

    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow { background-color: #ECECEC; }
        QWebEngineView { background-color: #3A6EA5; border: 2px solid #ECECEC; }
    """)
    return app

def apply_superlite_vista():
    """
    SuperLite dành cho Windows Vista trở lên (Aero style nhẹ)
    """
    chromium_flags = [
        "--enable-low-end-device-mode",
        "--renderer-process-limit=3",
        "--max-connections-per-server=6",
        "--disable-background-networking",
        "--js-flags=--max-old-space-size=384",
        "--enable-gpu-rasterization",
        "--ignore-gpu-blocklist",
    ]
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(chromium_flags)

    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow { background-color: #2C2C2C; }
        QWebEngineView { background-color: #00A2ED; border-radius: 6px; }
    """)
    return app

if __name__ == "__main__":
    mode = "vista"  # đổi thành "xp" nếu muốn chạy bản XP
    if mode == "xp":
        app = apply_superlite_xp()
        window_title = "PyBrowserVN SuperLite - XP"
    else:
        app = apply_superlite_vista()
        window_title = "PyBrowserVN SuperLite - Vista"

    window = QMainWindow()
    window.setWindowTitle(window_title)
    window.setGeometry(100, 100, 1000, 700)

    view = QWebEngineView()
    view.load(QUrl("https://google.vn"))  # Trang test
    window.setCentralWidget(view)

    window.show()
    sys.exit(app.exec())
