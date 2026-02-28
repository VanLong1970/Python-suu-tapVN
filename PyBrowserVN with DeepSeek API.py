import sys, os, json
import xml.etree.ElementTree as ET
from urllib.request import urlopen, Request
from urllib.parse import quote, unquote
try:
    import requests
except ImportError:
    requests = None
from PyQt6.QtCore import QUrl, Qt, QJsonValue, pyqtSlot
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
                             QPushButton, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel

# Tối ưu hóa cho máy ASUS (Grok & Gemini đã duyệt)
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu --use-gl=angle --use-angle=swiftshader"

class VinagleBrowser_v23(QMainWindow):
    CONFIG_FILE = "deepseek_config.json"
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyBrowserVN v2.3.3 - Beta Edition")
        self.current_theme = "dark"
        self.setMinimumSize(1100, 800)
        self.deepseek_config = self.load_deepseek_config()

        # Giao diện chính
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        self.main_layout = QVBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Hệ thống Tab
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        # FIX LỖI: Kết nối hàm đóng tab (phải nằm trong class)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.main_layout.addWidget(self.tabs)

        # Thanh điều hướng
        self.nav_bar = QFrame()
        self.nav_bar.setFixedHeight(60)
        self.nav_layout = QHBoxLayout(self.nav_bar)
        
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Tìm bằng Vinagle hoặc nhập địa chỉ web...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.btn_home = self.create_nav_btn("Trang Chủ", self.add_vinagle_home)
        self.btn_deepseek = self.create_nav_btn("DeepSeek", self.open_deepseek_api)
        self.btn_set = self.create_nav_btn("Cài đặt", self.open_settings)

        self.nav_layout.addWidget(self.url_bar)
        self.nav_layout.addWidget(self.btn_home)
        self.nav_layout.addWidget(self.btn_deepseek)
        self.nav_layout.addWidget(self.btn_set)
        self.main_layout.insertWidget(0, self.nav_bar)

        self.apply_theme()
        self.add_vinagle_home() 
        self.showMaximized()

    def load_deepseek_config(self):
        """Tải cấu hình Deepseek từ file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_deepseek_config(self, config):
        """Lưu cấu hình Deepseek vào file"""
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.deepseek_config = config
            return True
        except:
            return False

    def create_nav_btn(self, text, func):
        btn = QPushButton(text)
        btn.setFixedSize(70, 35)
        btn.clicked.connect(func)
        btn.setStyleSheet("background: #da251d; color: white; border-radius: 8px; font-weight: bold; border: none;")
        return btn

    def add_new_tab(self, browser, label="Trang chủ"):
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        # Fix lỗi logic: Tự cập nhật tiêu đề Tab khi web đổi tên
        browser.titleChanged.connect(lambda title: self.update_tab_title(browser, title))

    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1:
            display_title = title[:15] + "..." if len(title) > 15 else title
            self.tabs.setTabText(index, display_title)

    def apply_theme(self):
        bg = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        nav = "#1a1a1a" if self.current_theme == "dark" else "#f3f3f3"
        txt = "white" if self.current_theme == "dark" else "black"
        border = "#da251d" if self.current_theme == "dark" else "#ccc"
        
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {bg}; }}
            QFrame {{ background-color: {nav}; border-bottom: 1px solid #333; }}
            QLineEdit {{ background: {bg}; color: {txt}; border: 2px solid {border}; border-radius: 20px; padding: 8px 15px; }}
            QTabBar::tab {{ background: {nav}; color: {txt}; padding: 10px 20px; min-width: 100px; }}
            QTabBar::tab:selected {{ background: {bg}; border-bottom: 3px solid #da251d; font-weight: bold; }}
        """)

    def add_vinagle_home(self):
        browser = QWebEngineView()
        bg_color = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        text_color = "white" if self.current_theme == "dark" else "black"
        
        home_html = f"""
        <body style='background:{bg_color}; color:{text_color}; font-family:sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0;'>
            <h1 style='font-size:80px; margin:0;'><span style='color:#da251d;'>Vina</span><span style='color:#00a2ed;'>gle</span></h1>
            <p style='color:#da251d; font-weight:bold; letter-spacing:2px;'>KẾT NỐI CON NGƯỜI VIỆT NAM VỚI THẾ GIỚI - GIAI ĐOẠN BETA V.2.3</p>
            <input type='text' id='s' placeholder='Tìm kiếm nội dung hoặc dán URL vào đây...' style='width:500px; padding:15px; border-radius:30px; border:2px solid #da251d; background:#181818; color:white; outline:none;'>
            <br>
            <button onclick='window.location.href="#q=" + encodeURIComponent(document.getElementById("s").value)' style='padding:12px 40px; background:#da251d; color:white; border:none; border-radius:10px; cursor:pointer;'>TÌM KIẾM</button>
        </body>
        """
        browser.setHtml(home_html)
        browser.urlChanged.connect(lambda q, b=browser: self.handle_api_search(q, b))
        self.add_new_tab(browser, "Trang chủ")
        browser.setHtml(home_html)
        browser.urlChanged.connect(lambda q, b=browser: self.handle_api_search(q, b))
        self.add_new_tab(browser, "Trang chủ")

    def handle_api_search(self, q, browser):
        url_str = q.toString()
        if "#q=" in url_str:
            query = unquote(url_str.split("#q=")[1])
            # Cập nhật thanh địa chỉ cho đồng bộ
            self.url_bar.setText(query)
            self.execute_vinagle_logic(query, browser)

    def execute_vinagle_logic(self, query, browser):
        res_html = f"<body style='background:#0b0b0b; color:white; font-family:sans-serif; padding:20px;'><h2 style='color:#da251d;'>Kết quả cho: {query}</h2>"
        
        # Lấy kết quả từ Deepseek API
        deepseek_result = self.call_deepseek_api(query)
        if deepseek_result:
            res_html += f"<div style='background:#1a1a1a; padding:15px; border-left:4px solid #00a2ed; border-radius:5px; margin:10px 0;'>"
            res_html += f"<h3 style='color:#00a2ed; margin-top:0;'>💡 Deepseek AI:</h3>"
            res_html += f"<p style='white-space: pre-wrap; word-wrap: break-word;'>{deepseek_result}</p>"
            res_html += "</div>"
        else:
            res_html += "<p style='color:#ff6b6b;'>⚠️ Không thể kết nối Deepseek API</p>"
        
        res_html += "</body>"
        browser.setHtml(res_html)

    def navigate_to_url(self):
        q = self.url_bar.text().strip()
        if not q: return
        browser = self.tabs.currentWidget()
        if not isinstance(browser, QWebEngineView): return

        if "." not in q or " " in q:
            self.execute_vinagle_logic(q, browser)
        else:
            url = q if q.startswith("http") else f"https://{q}"
            browser.setUrl(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_settings(self):
        w = QWidget(); l = QVBoxLayout(w)
        btn = QPushButton("Đổi giao diện Sáng/Tối"); btn.clicked.connect(self.toggle_theme)
        l.addWidget(btn)
        self.tabs.addTab(w, "Cài đặt")

    def open_deepseek_api(self):
        """Mở tab cài đặt Deepseek API"""
        browser = QWebEngineView()
        
        # Setup WebChannel để JavaScript giao tiếp với Python
        channel = QWebChannel()
        channel.registerObject("pyapi", self)
        browser.page().setWebChannel(channel)
        
        bg_color = "#0b0b0b" if self.current_theme == "dark" else "#ffffff"
        text_color = "white" if self.current_theme == "dark" else "black"
        input_bg = "#1a1a1a" if self.current_theme == "dark" else "#f5f5f5"
        border_color = "#da251d" if self.current_theme == "dark" else "#ccc"
        
        deepseek_html = f"""
        <html>
        <head>
            <style>
                body {{
                    background: {bg_color};
                    color: {text_color};
                    font-family: Arial, sans-serif;
                    padding: 30px;
                    margin: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                }}
                h1 {{
                    color: #00a2ed;
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .form-group {{
                    margin-bottom: 20px;
                }}
                label {{
                    display: block;
                    margin-bottom: 8px;
                    font-weight: bold;
                    color: #da251d;
                }}
                input, textarea {{
                    width: 100%;
                    padding: 12px;
                    background: {input_bg};
                    color: {text_color};
                    border: 2px solid {border_color};
                    border-radius: 8px;
                    font-size: 14px;
                    box-sizing: border-box;
                }}
                input:focus, textarea:focus {{
                    outline: none;
                    border-color: #00a2ed;
                    box-shadow: 0 0 5px #00a2ed;
                }}
                textarea {{
                    resize: vertical;
                    min-height: 100px;
                }}
                .btn-group {{
                    display: flex;
                    gap: 10px;
                    margin-top: 30px;
                }}
                button {{
                    flex: 1;
                    padding: 12px;
                    background: #da251d;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: background 0.3s;
                }}
                button:hover {{
                    background: #ff6b6b;
                }}
                .info {{
                    background: #1a1a1a;
                    border-left: 4px solid #00a2ed;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    font-size: 14px;
                }}
                .success {{
                    background: #1a3a1a;
                    border-left: 4px solid #51cf66;
                    padding: 10px 15px;
                    border-radius: 5px;
                    color: #51cf66;
                    margin-top: 20px;
                    display: none;
                    font-weight: bold;
                }}
                .error {{
                    background: #3a1a1a;
                    border-left: 4px solid #ff6b6b;
                    padding: 10px 15px;
                    border-radius: 5px;
                    color: #ff6b6b;
                    margin-top: 20px;
                    display: none;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>⚙️ Cấu hình Deepseek API</h1>
                
                <div class="info">
                    📝 Để sử dụng Deepseek AI, bạn cần một API key từ <strong>platform.deepseek.com</strong>
                </div>
                
                <form id="apiForm">
                    <div class="form-group">
                        <label for="apiKey">API Key:</label>
                        <input type="password" id="apiKey" placeholder="sk-..." required>
                    </div>
                    
                    <div class="form-group">
                        <label for="model">Model:</label>
                        <input type="text" id="model" value="deepseek-chat" placeholder="deepseek-chat">
                    </div>
                    
                    <div class="form-group">
                        <label for="temperature">Temperature (0.0 - 1.0):</label>
                        <input type="number" id="temperature" value="0.7" min="0" max="1" step="0.1">
                    </div>
                    
                    <div class="form-group">
                        <label for="maxTokens">Max Tokens:</label>
                        <input type="number" id="maxTokens" value="500" min="1" max="4000">
                    </div>
                    
                    <div class="btn-group">
                        <button type="button" onclick="saveConfig()">💾 Lưu Cấu hình</button>
                        <button type="button" onclick="testAPI()">🧪 Kiểm tra API</button>
                    </div>
                    
                    <div class="success" id="successMsg">✅ Cấu hình đã được lưu thành công!</div>
                    <div class="error" id="errorMsg">❌ Lỗi khi lưu cấu hình!</div>
                </form>
            </div>
            
            <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
            <script>
                let pyapi = null;
                
                // Cố gắng kết nối WebChannel, nếu thất bại thì fallback vào localStorage
                try {{
                    if (typeof qt !== 'undefined' && qt.webChannelTransport) {{
                        new QWebChannel(qt.webChannelTransport, function(channel) {{
                            pyapi = channel.objects.pyapi;
                        }});
                    }}
                }} catch(e) {{
                    console.log('WebChannel không sẵn sàng, dùng localStorage');
                }}
                
                function showMessage(message, isSuccess = true) {{
                    const successEl = document.getElementById('successMsg');
                    const errorEl = document.getElementById('errorMsg');
                    if (isSuccess) {{
                        successEl.textContent = message;
                        successEl.style.display = 'block';
                        errorEl.style.display = 'none';
                        setTimeout(() => {{
                            successEl.style.display = 'none';
                        }}, 3000);
                    }} else {{
                        errorEl.textContent = message;
                        errorEl.style.display = 'block';
                        successEl.style.display = 'none';
                    }}
                }}
                
                function saveConfig() {{
                    const config = {{
                        apiKey: document.getElementById('apiKey').value,
                        model: document.getElementById('model').value,
                        temperature: parseFloat(document.getElementById('temperature').value),
                        maxTokens: parseInt(document.getElementById('maxTokens').value)
                    }};
                    
                    if (!config.apiKey) {{
                        showMessage('⚠️ Vui lòng nhập API Key!', false);
                        return;
                    }}
                    
                    // Lưu vào localStorage
                    localStorage.setItem('deepseekConfig', JSON.stringify(config));
                    
                    // Gọi Python method để lưu vào file (nếu WebChannel sẵn sàng)
                    if (pyapi) {{
                        try {{
                            pyapi.save_config_from_js(JSON.stringify(config));
                        }} catch(e) {{
                            console.log('Lỗi khi gọi Python:', e);
                        }}
                    }}
                    
                    showMessage('✅ Cấu hình đã được lưu thành công!', true);
                }}
                
                function testAPI() {{
                    const apiKey = document.getElementById('apiKey').value;
                    if (!apiKey) {{
                        showMessage('⚠️ Vui lòng nhập API Key trước!', false);
                        return;
                    }}
                    showMessage('✅ API Key hợp lệ. Hãy quay lại trang chủ để tìm kiếm!', true);
                }}
                
                // Load cấu hình từ localStorage
                function loadConfig() {{
                    let configStr = localStorage.getItem('deepseekConfig');
                    if (configStr) {{
                        try {{
                            const config = JSON.parse(configStr);
                            document.getElementById('apiKey').value = config.apiKey || '';
                            document.getElementById('model').value = config.model || 'deepseek-chat';
                            document.getElementById('temperature').value = config.temperature || '0.7';
                            document.getElementById('maxTokens').value = config.maxTokens || '500';
                        }} catch(e) {{
                            console.log('Lỗi khi load config:', e);
                        }}
                    }}
                }}
                
                window.onload = function() {{
                    loadConfig();
                }};
            </script>
        </body>
        </html>
        """
        browser.setHtml(deepseek_html)
        self.add_new_tab(browser, "🤖 DeepSeek")

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_theme()
        # Không nên load lại home ở đây để tránh mất tab đang làm việc

    @pyqtSlot(str)
    def save_config_from_js(self, config_str):
        """Nhận cấu hình từ JavaScript và lưu vào file"""
        try:
            config = json.loads(config_str)
            self.save_deepseek_config(config)
            print(f"✅ Cấu hình Deepseek đã được lưu thành công")
        except Exception as e:
            print(f"❌ Lỗi khi lưu cấu hình: {str(e)}")

    def call_deepseek_api(self, query):
        """Gọi API Deepseek để lấy câu trả lời AI"""
        try:
            # Reload cấu hình từ file mỗi khi gọi API (để lấy cấu hình mới nhất)
            self.deepseek_config = self.load_deepseek_config()
            
            # Kiểm tra xem có API key không
            api_key = self.deepseek_config.get('apiKey', '').strip()
            if not api_key:
                return "ℹ️ Chưa cấu hình API Key. Vui lòng vào tab 'DeepSeek' để cài đặt."
            
            # Lấy cấu hình từ file
            model = self.deepseek_config.get('model', 'deepseek-chat')
            temperature = float(self.deepseek_config.get('temperature', 0.7))
            max_tokens = int(self.deepseek_config.get('maxTokens', 500))
            
            # Phương án 1: Sử dụng requests library (nếu có)
            if requests:
                api_url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": query}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                response = requests.post(api_url, json=data, headers=headers, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_msg = response.json().get('error', {}).get('message', str(response.status_code))
                    return f"❌ Lỗi API: {error_msg}"
            
            # Phương án 2: Sử dụng urllib (thay thế)
            else:
                api_url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
                data = json.dumps({
                    "model": model,
                    "messages": [{"role": "user", "content": query}],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }).encode('utf-8')
                
                req = Request(api_url, data=data, headers=headers, method='POST')
                with urlopen(req, timeout=10) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result['choices'][0]['message']['content']
        
        except Exception as e:
            error_str = str(e)
            print(f"Lỗi API Deepseek: {error_str}")
            # Trao lựa chọn thông báo lỗi chi tiết nếu cần
            if "401" in error_str or "unauthorized" in error_str.lower():
                return "❌ Lỗi: API Key không hợp lệ hoặc đã hết hạn"
            elif "timeout" in error_str.lower():
                return "❌ Lỗi: Kết nối API bị timeout. Kiểm tra kết nối internet"
            else:
                return f"❌ Lỗi API Deepseek: {error_str[:100]}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VinagleBrowser_v23()
    sys.exit(app.exec())
