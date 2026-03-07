TIẾNG VIỆT:
# 🌿 Hệ Sinh Thái Vinagle (Vina Ecosystem)

Một hệ sinh thái công nghệ hoàn chỉnh được tạo dành riêng cho người dùng Việt Nam, tương tự với hệ sinh thái của Google, nhưng với định hướng Việt Nam.

Các Dịch Vụ

1. **VinaMail** 📧
Hộp thư điện tử tương tự Gmail, với giao diện Yahoo Mail đời đầu (Beta uses only).

**Tính năng:**
- ✅ Đăng ký / Đăng nhập
- ✅ Gửi/Nhận email
- ✅ Lưu nháp
- ✅ Quản lý danh bạ (Contacts)
- ✅ Tạo thư mục tùy chỉnh
- ✅ Tìm kiếm email
- ✅ Thùng rác

Công nghệ:
- Backend: Python (Flask)
- Database: SQLite
- Frontend: HTML/CSS/JavaScript

Port: 5001

### 2. **VinaTube** 
Video sharing platform tương tự YouTube, với giao diện cổ đại.

**Tính năng:**
- ✅ Đăng ký / Đăng nhập
- ✅ Tải video lên
- ✅ Xem video
- ✅ Lượt thích (Like)
- ✅ Chức năng bình luận
- ✅ Tạo playlist
- ✅ Tìm kiếm video (Video searcher)

**Công nghệ:**
- Backend: Python (Flask)
- Database: SQLite
- Frontend: HTML/CSS/JavaScript

**Port:** 5002

---

## 🚀 Cài Đặt

### Prerequisites
- Python 3.8+
- pip
- Git

### Bước 1: Clone hoặc tải về repo

```bash
cd He_sinh_thai_Vina
```

### Bước 2: Cài đặt Python packages

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy VinaMail Backend

```bash
cd VinaMail/backend
python app.py
```

VinaMail sẽ chạy tại `http://localhost:5001`

Mở frontend tại: `VinaMail/frontend/index.html`

### Bước 4: Chạy VinaTube Backend (trong terminal khác)

```bash
cd VinaTube/backend
python app.py
```

VinaTube sẽ chạy tại `http://localhost:5002`

Mở frontend tại: `VinaTube/frontend/index.html`

---

## 📁 Cấu Trúc Dự Án

```
He_sinh_thai_Vina/
├── VinaMail/
│   ├── backend/
│   │   ├── app.py              # Flask app chính
│   │   ├── models.py           # Database models
│   │   ├── database.py         # Database initialization
│   │   └── vinamail.db         # SQLite database (tự tạo)
│   └── frontend/
│       ├── index.html          # Trang chính
│       ├── style.css           # Styling
│       └── script.js           # Frontend logic
│
├── VinaTube/
│   ├── backend/
│   │   ├── app.py              # Flask app chính
│   │   ├── models.py           # Database models
│   │   ├── database.py         # Database initialization
│   │   ├── vinatube.db         # SQLite database (tự tạo)
│   │   └── uploads/            # Thư mục lưu video (tự tạo)
│   └── frontend/
│       ├── index.html          # Trang chính
│       ├── style.css           # Styling
│       └── script.js           # Frontend logic
│
└── README.md                    # Tài liệu này
```

---

## 🔌 API Endpoints

### VinaMail API (Port 5001)

#### Authentication
- `POST /api/auth/register` - Đăng ký
- `POST /api/auth/login` - Đăng nhập

#### Emails
- `GET /api/emails/<user_id>` - Lấy emails
- `POST /api/emails/<user_id>/send` - Gửi email
- `POST /api/emails/<user_id>/draft` - Lưu nháp
- `DELETE /api/emails/<email_id>/delete` - Xóa email
- `GET /api/emails/<email_id>/search` - Tìm kiếm

#### Contacts
- `GET /api/contacts/<user_id>` - Lấy danh bạ
- `POST /api/contacts/<user_id>/add` - Thêm liên hệ

#### Folders
- `GET /api/folders/<user_id>` - Lấy thư mục
- `POST /api/folders/<user_id>/create` - Tạo thư mục

---

### VinaTube API (Port 5002)

#### Authentication
- `POST /api/auth/register` - Đăng ký
- `POST /api/auth/login` - Đăng nhập

#### Videos
- `GET /api/videos` - Lấy tất cả video (pagination)
- `GET /api/videos/<user_id>` - Lấy video của user
- `GET /api/videos/<video_id>` - Chi tiết video
- `POST /api/videos/upload` - Tải lên video
- `POST /api/videos/<video_id>/like` - Thích video
- `DELETE /api/videos/<video_id>/delete` - Xóa video

#### Comments
- `GET /api/videos/<video_id>/comments` - Lấy bình luận
- `POST /api/videos/<video_id>/comment` - Thêm bình luận

#### Search
- `GET /api/search?q=<query>` - Tìm kiếm video

#### Playlists
- `GET /api/playlists/<user_id>` - Lấy playlist
- `POST /api/playlists/<user_id>/create` - Tạo playlist

---

## 🎨 Giao Diện

### VinaMail
- **Phong cách:** Yahoo Mail 2010s
- **Màu chủ đạo:** Xanh dương (#667eea), xám
- **Layout:** 2 cột (Sidebar + Main Content)

### VinaTube
- **Phong cách:** YouTube 2010s
- **Màu chủ đạo:** Đỏ (#ff0000), trắng
- **Layout:** 2 cột (Sidebar + Videos Grid)

---

## 🔄 Workflow Phát Triển

### Cách mở ứng dụng frontend:

**Option 1: Mở file trực tiếp**
```bash
# Windows
start VinaMail/frontend/index.html
start VinaTube/frontend/index.html

# macOS
open VinaMail/frontend/index.html
open VinaTube/frontend/index.html

# Linux
xdg-open VinaMail/frontend/index.html
xdg-open VinaTube/frontend/index.html
```

**Option 2: Dùng Live Server (VS Code Extension)**
- Cài extension "Live Server"
- Right-click `index.html` → "Open with Live Server"

**Option 3: Dùng Python HTTP Server**
```bash
# Trong thư mục frontend
python -m http.server 8000

# Truy cập http://localhost:8000/index.html
```

---

## 🐛 Troubleshooting

### CORS Error?
Backend đã cấu hình CORS, nếu vẫn gặp lỗi, thêm header trong Flask:
```python
from flask_cors import CORS
CORS(app)
```

### Database Error?
- Xóa file `.db` và chạy lại app (database sẽ tự tạo)
- Kiểm tra quyền thư mục

### Video không tải lên?
- Kiểm tra thư mục `uploads` tồn tại
- Kiểm tra dung lượng file < 500MB
- Kiểm tra format video (MP4, WebM, etc.)

---

## 📝 Ghi Chú

- Hiện tại đây là version Beta
- Dữ liệu lưu trữ cục bộ (SQLite)
- Cần thêm xác thực email, 2FA, mã hóa mật khẩu cao cấp hơn
- Video processing (encoding, streaming) chưa được tối ưu - giai đoạn Beta

---

## 🛣️ Roadmap - Tính Năng Sắp Tới

### VinaMail
- [ ] Hỗ trợ thư mục lẫn nhau giữa người dùng (Share files with Multi-Users)
- [ ] Email notifications
- [ ] Dark mode (Beta)
- [ ] Lịch dương/lịch âm, lên kế hoạcg
- [ ] Drive integration VinaClouds

### VinaTube
- [ ] Live streaming
- [ ] Subtitle hỗ trợ
- [ ] Transcode video tự động
- [ ] Quality selection
- [ ] Channel subscription

### Các dịch vụ sắp thêm
- [ ] **VinaMap** - Bản đồ và định vị
- [ ] **VinaClouds** - Lưu trữ  điện toán đám mây (giá trị dự kiến: 1 TB miễn phí toàn tập)
- [ ] **Vinagle Artifical Intellince** AI Tích hợp trên PyBrowser

---

📄 License

MIT License - Sử dụng tự do cho mục đích học tập và phát triển (xem thêm tại mục MIT Lincense) 

---

## 👨‍💻 Tác Giả

Vinagle PyBrowser Technology Corpotaion - Nguyễn Nhật Minh - Xây dựng hệ sinh thái công nghệ cho người Việt

---

**Chúc bạn có một trải nghiệm tuyệt vời với Vina Ecosystem!** 🚀
