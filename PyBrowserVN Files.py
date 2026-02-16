import sys, os, json
import xml.etree.ElementTree as ET # Thêm thư viện xử lý RSS
from urllib.request import urlopen, Request
from urllib.parse import quote, unquote
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                             QPushButton, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Tối ưu hóa nhân trình duyệt
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu"

class VinagleBrowser_v23(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Chromium Browser Việt Nam v2.3")
        self.current_theme = "dark"
        self.setMinimumSize(1100, 800)

        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tabs)

        self.nav_bar = QFrame()
        self.nav_bar.setFixedHeight(60)
        self.nav_layout = QHBoxLayout(self.nav_bar)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Tìm kiếm bằng Vinagle hoặc tìm kiếm URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.btn_home = self.create_nav_btn("🏠 Chủ", self.add_vinagle_home)
        self.btn_set = self.create_nav_btn("⚙️ Cài", self.open_settings)

        self.nav_layout.addWidget(self.url_bar)
        self.nav_layout.addWidget(self.btn_home)
        self.nav_layout.addWidget(self.btn_set)
        self.main_layout.insertWidget(0, self.nav_bar)

        self.apply_theme()
        self.add_vinagle_home() 
        self.showMaximized()

    def create_nav_btn(self, text, func):
        btn = QPushButton(text)
        btn.setFixedSize(70, 35)
        btn.clicked.connect(func)
        btn.setStyleSheet("background: #da251d; color: white; border-radius: 8px; font-weight: bold; border: none;")
        return btn

    def apply_theme(self):
        bg = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        nav = "#1a1a1a" if self.current_theme == "dark" else "#f3f3f3"
        txt = "white" if self.current_theme == "dark" else "black"
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {bg}; }}
            QFrame {{ background-color: {nav}; border-bottom: 1px solid #333; }}
            QLineEdit {{ background: {bg}; color: {txt}; border: 2px solid #da251d; border-radius: 20px; padding: 8px 15px; }}
            QTabBar::tab {{ background: {nav}; color: {txt}; padding: 10px 20px; }}
            QTabBar::tab:selected {{ background: {bg}; border-bottom: 3px solid #da251d; font-weight: bold; }}
        """)

    def add_vinagle_home(self):
        browser = QWebEngineView()
        bg_color = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        text_color = "white" if self.current_theme == "dark" else "black"
        
        home_html = f"""
        <body style='background:{bg_color}; color:{text_color}; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; overflow:hidden;'>
            <h1 style='font-size:110px; margin:0;'><span style='color:#da251d;'>Vina</span><span style='color:#00a2ed;'>gle</span></h1>
            <p style='letter-spacing:6px; color:#da251d; font-weight:bold; margin-bottom:40px;'>KẾT NỐI CON NGƯỜI VIỆT NAM SANG THẾ GIỚI - GIAI ĐOẠN BETA v2.3</p>
            <input type='text' id='s' placeholder='Nhập từ khóa tìm kiếm...' style='width:650px; padding:22px; border-radius:45px; border:2px solid #da251d; background:#181818; color:white; font-size:20px; outline:none;'>
            <button onclick='window.location.href="#q=" + encodeURIComponent(document.getElementById("s").value)' style='margin-top:30px; padding:18px 60px; background:#da251d; color:white; border:none; border-radius:15px; cursor:pointer; font-weight:bold; font-size:20px;'>TÌM VỚI VINAGLE</button>
        </body>
        """
        browser.setHtml(home_html)
        browser.urlChanged.connect(lambda q, b=browser: self.handle_api_search(q, b))
        browser.loadFinished.connect(lambda ok, b=browser: self.handle_errors(ok, b))
        self.tabs.addTab(browser, "Trang chủ")
        self.tabs.setCurrentWidget(browser)

    def handle_api_search(self, q, browser):
        url_str = q.toString()
        if "#q=" in url_str:
            query = unquote(url_str.split("#q=")[1])
            self.execute_vinagle_logic(query, browser)

    def execute_vinagle_logic(self, query, browser):
        """Lõi tìm kiếm Hybrid v2.3: Wiki + Tri thức tổng hợp + VnExpress RSS"""
        results_list = []
        try:
            rss_url = "https://vnexpress.net/rss/tin-moi-nhat.rss"
            req_rss = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_rss, timeout=5) as resp_rss:
                tree = ET.fromstring(resp_rss.read())
                for item in tree.findall(".//item")[:10]: # Duyệt 10 tin mới nhất
                    title = item.find("title").text
                    link = item.find("link").text
                    if query.lower() in title.lower():
                        results_list.append({"t": title, "s": "Nguồn: Báo VnExpress (Chính thống)", "l": link, "v": True})
        except: pass
        try:
            wiki_url = f"https://vi.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(query)}&format=json"
            req_w = Request(wiki_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_w, timeout=5) as resp_w:
                data_w = json.loads(resp_w.read().decode())
                for item in data_w['query']['search'][:5]:
                    results_list.append({"t": item['title'], "s": item['snippet'], "l": f"https://vi.wikipedia.org/wiki/{quote(item['title'])}", "v": False})
        except: pass
        
        try:
            rss_url = "https://thanhnien.vn/rss/home.rss"
            req_rss = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_rss, timeout=5) as resp_rss:
                tree = ET.fromstring(resp_rss.read())
                for item in tree.findall(".//item")[:10]: # Duyệt 10 tin mới nhất
                    title = item.find("title").text
                    link = item.find("link").text
                    if query.lower() in title.lower():
                        results_list.append({"t": title, "s": "Nguồn: Báo Thanh Niên (Chính thống)", "l": link, "v": True})
        except: pass
        try:
            rss_url = "https://nhandan.vn/rss/tin-moi-nhat-1.rss"
            req_rss = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_rss, timeout=5) as resp_rss:
                tree = ET.fromstring(resp_rss.read())
                for item in tree.findall(".//item")[:10]: # Duyệt 10 tin mới nhất
                    title = item.find("title").text
                    link = item.find("link").text
                    if query.lower() in title.lower():
                        results_list.append({"t": title, "s": "Nguồn: Báo Nhân Dân (Chính thống)", "l": link, "v": True})
        except: pass
        try:
            rss_url = "https://dantri.com.vn/rss/home.rss"
            req_rss = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_rss, timeout=5) as resp_rss:
                tree = ET.fromstring(resp_rss.read())
                for item in tree.findall(".//item")[:10]: # Duyệt 10 tin mới nhất
                    title = item.find("title").text
                    link = item.find("link").text
                    if query.lower() in title.lower():
                        results_list.append({"t": title, "s": "Nguồn: Báo Dân Trí (Chính thống)", "l": link, "v": True})
        except: pass
        try:
            rss_url = "https://www.qdnd.vn/rss/tin-moi-nhat"
            req_rss = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req_rss, timeout=5) as resp_rss:
                tree = ET.fromstring(resp_rss.read())
                for item in tree.findall(".//item")[:10]: # Duyệt 10 tin mới nhất
                    title = item.find("title").text
                    link = item.find("link").text
                    if query.lower() in title.lower():
                        results_list.append({"t": title, "s": "Nguồn: Báo Quân đội Nhân dân (Chính thống)", "l": link, "v": True})
        except: pass
        # Vẽ giao diện kết quả
        res_html = f"<body style='background:#0b0b0b; color:white; font-family:sans-serif; padding:40px;'><h2 style='color:#da251d;'>🔍 Vinagle Search Results v2.3</h2><hr style='border:1px solid #333; margin-bottom:30px;'>"
        if not results_list:
            res_html += "<p>Hệ thống không tìm thấy tin tức hoặc dữ liệu thô cho từ khóa này.</p>"
        else:
            for res in results_list:
                badge = "<span style='background:#da251d; color:white; padding:2px 8px; border-radius:4px; font-size:12px; margin-right:10px;'>XÁC THỰC</span>" if res.get("v") else ""
                res_html += f"""
                <div style='margin-bottom:35px; border-left:4px solid {"#da251d" if res.get("v") else "#444"}; padding-left:20px;'>
                    {badge}<a href='{res['l']}' style='color:#00a2ed; font-size:22px; text-decoration:none; font-weight:bold;'>{res['t']}</a>
                    <p style='color:#ccc; font-size:16px; margin-top:10px;'>{res['s']}...</p>
                </div>
                """
        res_html += "</body>"
        browser.setHtml(res_html)

    def handle_errors(self, ok, browser):
        if not ok and not browser.url().toString().startswith("data"):
            err_html = "<body style='background:#0b0b0b; color:#da251d; text-align:center; padding-top:100px; font-family:sans-serif;'><h1 style='font-size:150px;'>📵</h1><h1>VINAGLE v2.3: LỖI KẾT NỐI</h1><button onclick='location.reload()' style='background:#da251d; color:white; border:none; padding:15px 40px; border-radius:10px; cursor:pointer; font-weight:bold;'>THỬ LẠI</button></body>"
            browser.setHtml(err_html)

    def navigate_to_url(self):
        q = self.url_bar.text().strip()
        if not q: return
        if "." not in q or " " in q:
            self.execute_vinagle_logic(q, self.tabs.currentWidget())
        else:
            url = q if q.startswith("http") else f"https://{q}"
            self.tabs.currentWidget().setUrl(QUrl(url))

    def open_settings(self):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(50, 50, 50, 50)
        h = QLabel("⚙️ Vinagle Config v2.3"); h.setStyleSheet("font-size: 30px; font-weight: bold; color: #da251d;"); l.addWidget(h)
        btn = QPushButton("🌓 Đổi Giao Diện Sáng/Tối"); btn.setFixedSize(300, 50); btn.clicked.connect(self.toggle_theme); l.addWidget(btn)
        l.addStretch(); self.tabs.addTab(w, "Cài đặt"); self.tabs.setCurrentWidget(w)

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"; self.apply_theme(); self.add_vinagle_home()

    def close_tab(self, index):
        if self.tabs.count() > 1: self.tabs.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv); window = VinagleBrowser_v23(); sys.exit(app.exec())
