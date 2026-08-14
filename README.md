# 🚀 TaskFlow — Modern Task Management Web App

Ứng dụng Web App quản lý công việc cá nhân hiện đại, siêu nhẹ, giao diện Glassmorphic đỉnh cao với trải nghiệm người dùng cực mượt.

![TaskFlow Header Status](https://img.shields.io/badge/Status-100%25%20Completed-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-HTML5%20%7C%20CSS3%20%7C%20JS%20ES6-blue?style=for-the-badge)

---

## 🌟 Tính Năng Nổi Bật

- 📝 **Quản lý công việc toàn diện (CRUD):** Thêm mới, chỉnh sửa, xóa và đánh dấu hoàn thành công việc dễ dàng.
- 🎨 **Giao diện Glassmorphism đỉnh cao:** Thiết kế hiện đại với hiệu ứng làm mờ nền, màu sắc tailoring và hiệu ứng hover mượt mà.
- 🌓 **Hỗ trợ Dark Mode / Light Mode:** Chuyển đổi theme tức thì và tự động ghi nhớ sở thích của bạn.
- 📊 **Clickable Stats Dashboard:** Click trực tiếp vào các thẻ đếm *Tổng số*, *Đang làm*, *Đã xong*, *Quá hạn* để lọc danh sách tức thì.
- 🔍 **Tìm kiếm & Lọc thông minh:** Lọc theo trạng thái, từ khóa tìm kiếm real-time và độ ưu tiên (🔴 Cao / 🟡 Trung bình / 🟢 Thấp).
- 🔀 **Sắp xếp linh hoạt:** Theo Ngày khởi tạo (mới nhất), Mức độ ưu tiên hoặc Hạn chót (Deadline).
- 🧹 **Dọn dẹp hàng loạt (Batch Clear):** Nút *"Dọn việc xong"* giúp dọn sạch danh sách các công việc đã hoàn thành chỉ với 1-click.
- ⌨️ **Phím tắt nhanh (Keyboard Shortcuts):**
  - <kbd>Ctrl</kbd> + <kbd>K</kbd> hoặc <kbd>/</kbd> : Nhảy đến ô Tìm kiếm
  - <kbd>Ctrl</kbd> + <kbd>N</kbd> : Mở form Thêm công việc mới
  - <kbd>Esc</kbd> : Đóng cửa sổ đang mở
- 💾 **Sao lưu & Phục hồi Dữ liệu (Backup & Restore):** Xuất toàn bộ dữ liệu ra file `.json` và nạp lại bất cứ khi nào.
- 🔒 **Dữ liệu lưu trữ cá nhân (Privacy First):** Mọi dữ liệu lưu hoàn toàn trên LocalStorage trình duyệt của bạn, không lo lộ thông tin.

---

## 🚀 Hướng Dẫn Chạy Ứng Dụng

Ứng dụng đang chạy live trên máy local của bạn tại:
👉 **[http://localhost:8080](http://localhost:8080)**

Hoặc mở trực tiếp file [`index.html`](file:///c:/Henry%20AI/index.html) bằng bất kỳ trình duyệt web nào (Chrome, Edge, Firefox, Safari) mà không cần cài đặt thêm bất kỳ thư viện ngoài nào!

---

## 📂 Cấu Trúc Mã Nguồn Project

```
c:\Henry AI/
├── index.html                  # Khung HTML5 Semantic của ứng dụng TaskFlow
├── css/
│   └── styles.css              # Design System, Colors, Glassmorphism & Animations
├── js/
│   ├── app.js                  # Main Application Controller & Keyboard Shortcuts
│   ├── storage.js              # Data Persistence Layer & LocalStorage CRUD
│   └── ui.js                   # DOM Component Renderers & Toast Notifications
├── docs/
│   ├── BRIEF.md                # Tài liệu Brief ý tưởng ban đầu
│   ├── DESIGN.md               # Bản thiết kế kỹ thuật chi tiết
│   └── specs/
│       └── task_manager_spec.md # Specification chi tiết
├── plans/
│   └── 260814-2020-task-manager/# 5 Phases lập trình chi tiết
└── README.md                   # Hướng dẫn & Giới thiệu ứng dụng
```

---

*Phát triển bởi Antigravity AI với AWF (Antigravity Workflow Framework)*
