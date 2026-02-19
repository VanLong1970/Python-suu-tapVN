import sys, os, json
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
if sys.platform == 'win32':
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('com.vinagle.browser')

class Seinichi_v22(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Chromium Browser Việt Nam v2.2")
        self.current_theme = "dark" 
        
        # Tab dọc
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.West)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Thanh điều hướng
        self.nav = QToolBar()
        self.addToolBar(self.nav)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Vinagle Search - Nhập nội dung cần tìm...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav.addWidget(self.url_bar)

        # Nút tiện ích
        self.add_nav_btn("🕒 Nhật ký", self.open_history_internal)
        self.add_nav_btn("📦 Kho", self.show_archive_page)
        self.add_nav_btn("⚙️ Cài đặt", self.open_settings_internal)
        self.add_nav_btn("📖 Reader", self.open_reader_mode)

        self.apply_theme()
        self.open_homepage()
        self.showMaximized()

    def apply_theme(self):
        if self.current_theme == "dark":
            self.setStyleSheet("QMainWindow { background-color: #0b0b0b; } QToolBar { background: #1a1a1a; border: none; } QLineEdit { background: #222; color: white; border: 1px solid #333; padding: 6px; border-radius: 8px; }")
        else:
            self.setStyleSheet("QMainWindow { background-color: #f0f2f5; } QToolBar { background: #ffffff; border-bottom: 1px solid #ddd; } QLineEdit { background: #fff; color: #000; border: 1px solid #ccc; padding: 6px; border-radius: 8px; }")

    def add_nav_btn(self, text, func):
        btn = QPushButton(text)
        btn.setStyleSheet("color: #da251d; font-weight: bold; background: transparent; border: none; padding: 5px; margin-left: 5px;")
        btn.clicked.connect(func)
        self.nav.addWidget(btn)

    def open_homepage(self):
        bg = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        txt = "white" if self.current_theme == "dark" else "black"
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ background: {bg}; color: {txt}; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
                .logo {{ font-size: 80px; font-weight: bold; margin-bottom: 25px; }}
                .vina {{ color: #da251d; }} .gle {{ color: #00a2ed; }}
                input {{ width: 550px; padding: 20px; border-radius: 40px; border: 1px solid #444; background: #1a1a1a; color: white; font-size: 18px; outline: none; }}
                .btns {{ margin-top: 35px; }}
                button {{ padding: 12px 25px; border-radius: 12px; border: none; background: #da251d; color: white; cursor: pointer; margin: 5px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="logo"><span class="vina">Vina</span><span class="gle">gle</span></div>
            <input type="text" id="s" placeholder="Tìm kiếm với Vinagle..." onkeydown="if(event.key==='Enter') go()">
            <div class="btns">
                <button onclick="go()">Tìm kiếm Vinagle</button>
                <button onclick="goImg()">Tìm hình ảnh 🖼️</button>
            </div>
            <script>
                function go() {{ let v = document.getElementById('s').value; if(v) window.location.href = "https://duckduckgo.com/?q=" + v; }}
                function goImg() {{ let v = document.getElementById('s').value; if(v) window.location.href = "https://www.google.com/search?tbm=isch&q=" + v; }}
            </script>
        </body>
        </html>
        """
        self.add_new_tab_with_html(html, "Vinagle Search")

    def handle_errors(self, ok, browser):
        if not ok:
            err_html = f"""
            <body style='background:#0b0b0b; color:#da251d; text-align:center; padding-top:100px; font-family:sans-serif;'>
                <h1 style='font-size:120px; margin:0;'>🚫</h1>
                <h1 style='text-transform: uppercase;'>Vinagle: Lỗi kết nối mạng</h1>
                <p style='color:white; font-size: 20px;'>Không thể truy cập máy chủ lúc này.</p>
                <button onclick='location.reload()' style='background:#da251d; color:white; border:none; padding:15px 30px; border-radius:10px; cursor:pointer; font-weight:bold; margin-top:20px;'>THỬ LẠI</button>
            </body>
            """
            browser.setHtml(err_html)

    def open_settings_internal(self):
        bg = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        txt = "white" if self.current_theme == "dark" else "black"
        html = f"""
        <body style='background:{bg}; color:{txt}; font-family:sans-serif; padding:50px;'>
            <h1 style='color:#da251d;'>⚙️ CÀI ĐẶT TRÌNH DUYỆT</h1>
            <hr>
            <h3>Giao diện hệ thống</h3>
            <button onclick='window.location.href="action://toggle-theme"' style='padding:10px; cursor:pointer; background:#da251d; color:white; border:none;'>
                Đổi chế độ {"Sáng" if self.current_theme == "dark" else "Tối"}
            </button>
            <p>Phiên bản: v2.2 - Python Chromium Browser Việt Nam</p>
        </body>
        """
        self.add_new_tab_with_html(html, "Cài đặt")
        self.tabs.currentWidget().urlChanged.connect(self.handle_theme_toggle)

    def handle_theme_toggle(self, url):
        if url.toString() == "action://toggle-theme":
            self.current_theme = "light" if self.current_theme == "dark" else "dark"
            self.apply_theme()
            self.open_settings_internal()

    def navigate_to_url(self):
        q = self.url_bar.text().strip()
        url = "https://duckduckgo.com/?q=" + q if "." not in q or " " in q else (q if q.startswith("http") else "https://" + q)
        self.tabs.currentWidget().setUrl(QUrl(url))

    def open_history_internal(self):
        html = "<body style='background:#0b0b0b;color:white;padding:40px;font-family:sans-serif;'><h1>🕒 Nhật ký duyệt web</h1><hr>"
        if os.path.exists("history.json"):
            with open("history.json", "r", encoding="utf-8") as f:
                for item in reversed(json.load(f)):
                    html += f"<p>• <a style='color:#00a2ed; text-decoration:none;' href='{item['u']}'>{item['t']}</a></p>"
        self.add_new_tab_with_html(html, "Nhật ký")

    def show_archive_page(self):
        html = "<body style='background:#0b0b0b;color:white;text-align:center;padding-top:50px;font-family:sans-serif;'><h1>📦 Kho lưu trữ</h1><hr><p>v1.1 Legacy | v2.2 Vinagle Search</p></body>"
        self.add_new_tab_with_html(html, "Kho lưu trữ")
    def open_reader_mode(self):
        # Lấy nội dung trang hiện tại dưới dạng văn bản thuần
        current_tab = self.tabs.currentWidget()
        if isinstance(current_tab, QWebEngineView):
            page = current_tab.page()
            page.toPlainText(lambda text: self.add_new_tab_with_html(
                f"<body style='padding:40px;font-family:sans-serif;background:#fdfdfd;color:#333;'>"
                f"<h1>Chế độ đọc</h1><hr><p>{text}</p></body>", 
                "Reader Mode"
            ))

    def add_new_tab_with_html(self, html, label):
        browser = QWebEngineView()
        browser.setHtml(html)
        browser.loadFinished.connect(lambda ok, b=browser: self.handle_errors(ok, b))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
    def add_new_tab(self, qurl, label):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        # Xử lý lỗi khi load trang
        browser.loadFinished.connect(lambda ok, b=browser: self.handle_errors(ok, b))
        # Lưu lịch sử khi URL thay đổi
        browser.urlChanged.connect(lambda q, b=browser: self.save_log(b))
        # Lấy favicon và gắn vào tab
        browser.iconChanged.connect(lambda icon, idx=self.tabs.count(): self.tabs.setTabIcon(idx, icon))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
        # Nếu còn nhiều tab thì mới cho đóng
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # Nếu chỉ còn 1 tab, thay vì đóng thì mở lại trang chủ
            self.open_homepage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Seinichi_v22()
    window.show()
    print("App started")
    sys.exit(app.exec())
