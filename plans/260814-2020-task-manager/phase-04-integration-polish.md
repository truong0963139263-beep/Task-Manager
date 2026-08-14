# Phase 04: Integration & UX Polish
Status: ✅ Complete
Dependencies: Phase 01, Phase 02, Phase 03

## Objective
Kết nối toàn bộ logic Event Listeners giữa Data Layer và UI Layer, tích hợp Keyboard Shortcuts, Export/Import dữ liệu JSON, Toast Notifications, Micro-animations và Theme Persistence.

## Implementation Steps
1. [x] Đăng ký phím tắt toàn cục (Keyboard Shortcuts): `Ctrl+K` (Focus tìm kiếm), `Ctrl+N` (Mở form thêm mới), `Esc` (Đóng modal).
2. [x] Thêm tính năng Sao lưu & Phục hồi dữ liệu (Backup & Restore): Tích hợp Export JSON file & Import JSON file trực tiếp từ giao diện.
3. [x] Tích hợp Toast Notification System (Thông báo mượt ở góc màn hình khi Thêm/Sửa/Xóa/Export thành công).
4. [x] Thêm Micro-animations (Slide-in toast, Fade-in task card, smooth theme transition).
5. [x] Tùy chỉnh Theme Switcher (Dark Mode / Light Mode toggle) tự động lưu preference vào LocalStorage.

## Files Created/Modified
- `index.html` - Thêm nút Export/Import JSON & Keyboard Hint Bar.
- `css/styles.css` - Custom Keyboard Badge styling, Card fade-in keyframes.
- `js/app.js` - Register Keyboard Shortcuts & File Import/Export event handlers.

## Test Criteria
- [x] Nhấn `Ctrl+K` và `Ctrl+N` thực hiện đúng thao tác tức thì.
- [x] Export file JSON tải về thành công và Import file JSON cập nhật lại ứng dụng ngay lập tức.
- [x] Mọi tương tác phản hồi tức thì dưới 100ms.

---
Next Phase: [`phase-05-testing-verification.md`](file:///c:/Henry%20AI/plans/260814-2020-task-manager/phase-05-testing-verification.md)
