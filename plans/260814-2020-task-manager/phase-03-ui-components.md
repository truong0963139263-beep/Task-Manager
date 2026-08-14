# Phase 03: UI Components & Layout
Status: ✅ Complete
Dependencies: Phase 01, Phase 02

## Objective
Thiết kế và render các UI Components tương tác: Header Stats (Clickable), Task Form Modal (Thêm/Sửa), Search & Filter Toolbar, Priority Filter Selector, Sort Selector, Clear Completed Tasks, Task Card Item, Empty State.

## Implementation Steps
1. [x] Nâng cấp Component Header Stats: Clickable Stat Cards hỗ trợ lọc nhanh khi click vào ô thống kê.
2. [x] Xây dựng Toolbar nâng cao: Thanh tìm kiếm (Real-time Search Input), Status Filter Tabs, Dropdown Lọc theo Độ ưu tiên & Dropdown Sắp xếp.
3. [x] Thêm nút Dọn việc xong (Clear Completed Button): Cho phép xóa hàng loạt các công việc đã hoàn thành.
4. [x] Xây dựng Task Card Item Component: Checkbox hoàn thành, Tiêu đề, Badge Priority (đỏ/vàng/xanh), Badge Deadline (cảnh báo quá hạn/hôm nay), Nút Action (Sửa/Xóa).
5. [x] Xây dựng Modal Form (Thêm / Chỉnh sửa công việc): Modal nổi với Backdrop mờ (Glassmorphism), Form Validation.
6. [x] Xây dựng Empty State UI động thông minh khi chưa có task hoặc tìm kiếm không thấy kết quả.

## Files Created/Modified
- `index.html` - Thêm HTML templates / containers & Select dropdowns.
- `css/styles.css` - Component styling, Clickable Stat Cards, Glassmorphism modals, Badges.
- `js/ui.js` - Dynamic Empty state renderer, Stats highlighter & Toast notifications.
- `js/app.js` - Logic controller điều khiển các UI components.

## Test Criteria
- [x] Giao diện hiển thị sắc nét, thẻ Task render đúng thông tin & màu sắc ưu tiên.
- [x] Click thẻ Stat Card tự động lọc danh sách tương ứng.
- [x] Modal mở/đóng mượt mà.

---
Next Phase: [`phase-04-integration-polish.md`](file:///c:/Henry%20AI/plans/260814-2020-task-manager/phase-04-integration-polish.md)
