import sys, os
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QProgressBar, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QAction

# Tối ưu hóa card đồ họa cho Win 10
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu"

class MyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setWindowTitle("Python Chromium Việt Nam v1.1")
        self.showMaximized()

        # Thanh công cụ
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Các nút điều hướng
        back_btn = QAction("◀", self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Thanh địa chỉ
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Nhập địa chỉ hoặc tìm kiếm trên Google...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Thanh tiến trình
        self.progress = QProgressBar()
        self.progress.setMaximumHeight(2)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")

        # Bố cục giao diện
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.progress)
        layout.addWidget(self.browser)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Kết nối sự kiện
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadFinished.connect(self.update_title)
        self.browser.loadProgress.connect(self.progress.setValue)
        self.browser.loadFinished.connect(lambda: self.progress.setValue(0))

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        q = self.url_bar.text().strip()
        if " " in q or "." not in q:
            url = "https://www.google.com/search?q=" + q
        elif not q.startswith("http"):
            url = "https://" + q
        else:
            url = q
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - Python Chromium Việt Nam v1.1")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Python Chromium Việt Nam v1.1")
    app.setOrganizationName("Limoba Seinichi tin học")
    window = MyBrowser()
    window.show()
    sys.exit(app.exec())
