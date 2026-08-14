# 📐 TECHNICAL DESIGN DOCUMENT: task-manager

**Ngày tạo:** 2026-08-14  
**Trạng thái:** 🟢 Approved  
**Dựa trên:** [`docs/specs/task_manager_spec.md`](file:///c:/Henry%20AI/docs/specs/task_manager_spec.md) & [`plans/260814-2020-task-manager/plan.md`](file:///c:/Henry%20AI/plans/260814-2020-task-manager/plan.md)

---

## 1. MÔ HÌNH DỮ LIỆU & LƯU TRỮ (DATABASE SCHEMA)

Ứng dụng lưu trữ dữ liệu tại Browser `localStorage` với 2 keys chính:

### 1.1. Task Items Key (`task_manager_items_v1`)
Mảng các đối tượng `TaskItem`:
```json
[
  {
    "id": "task_1723650000000",
    "title": "Thiết kế giao diện UI",
    "description": "Hoàn thiện CSS & Glassmorphism cho modal",
    "priority": "high",
    "status": "pending",
    "dueDate": "2026-08-20",
    "createdAt": "2026-08-14T20:20:00.000Z"
  }
]
```

### 1.2. App Settings Key (`task_manager_settings_v1`)
```json
{
  "theme": "dark",
  "sortBy": "dueDate"
}
```

---

## 2. KIẾN TRÚC GIAO DIỆN & LINH KIỆN UI (COMPONENTS)

```
┌──────────────────────────────────────────────────────────────┐
│  APP HEADER: Logo + Title + Theme Switcher (Dark/Light)     │
│  STATS DASHBOARD: [Total: 5] [Active: 3] [Done: 2] [Overdue] │
├──────────────────────────────────────────────────────────────┤
│  TOOLBAR:                                                    │
│  [🔍 Tìm kiếm công việc...] [Filter: Tất cả/Đang làm/Đã xong] │
│  [Priority: Tất cả/Cao/TB/Thấp]   [+ Thêm công việc]         │
├──────────────────────────────────────────────────────────────┤
│  TASK LIST CONTAINER:                                        │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ ☑️  Hoàn thiện thiết kế UI          [🔴 Cao] [📅 20/08] │  │
│  │     Mô tả chi tiết công việc...     [✏️ Sửa] [🗑️ Xóa]  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. LUỒNG HOẠT ĐỘNG (USER JOURNEYS)

### Hành trình 1: Thêm mới công việc
1. Người dùng bấm nút `+ Thêm công việc`.
2. Modal Form mở ra với hiệu ứng mờ nền (Glassmorphism).
3. Nhập tiêu đề, chọn mức ưu tiên (Cao/Trung bình/Thấp) và chọn ngày deadline.
4. Bấm `Lưu công việc`:
   - Hàm `saveTask()` lưu thông tin vào `LocalStorage`.
   - Hàm `renderTasks()` cập nhật lại danh sách ngay lập tức.
   - Hiển thị Toast notification: "Thêm công việc thành công!".

### Hành trình 2: Đánh dấu hoàn thành
1. Bấm vào ô checkbox của task.
2. Trạng thái task đổi từ `pending` sang `completed`.
3. Tiêu đề task hiển thị hiệu ứng gạch ngang (strike-through) mượt mà.
4. Cập nhật ngay các con số thống kê ở Header.

### Hành trình 3: Lọc & Tìm kiếm công việc
1. Gõ từ khóa vào ô tìm kiếm.
2. Danh sách lọc theo thời gian thực (real-time filtering) kết hợp với tab trạng thái đang chọn.

---

## 4. BỘ ĐIỀU KIỆN KIỂM THỬ (TEST CASES & ACCEPTANCE CRITERIA)

### TC-01: Happy Path - Thêm mới Task
- **Given:** Người dùng mở ứng dụng và bấm `+ Thêm công việc`.
- **When:** Nhập tên "Nộp báo cáo tuần", chọn Priority "High", chọn DueDate "2026-08-20", bấm `Lưu`.
- **Then:** Task mới xuất hiện đầu danh sách với badge Đỏ (Cao), LocalStorage cập nhật thành công, Toast thông báo xuất hiện.

### TC-02: Form Validation - Để trống tiêu đề
- **Given:** Form modal đang mở.
- **When:** Để trống ô tiêu đề và bấm `Lưu`.
- **Then:** Hiển thị thông báo "Vui lòng nhập tên công việc", form giữ nguyên trạng thái, không lưu dữ liệu rỗng.

### TC-03: Toggle Hoàn thành Task
- **Given:** Task đang ở trạng thái `pending`.
- **When:** Click checkbox của task.
- **Then:** Trạng thái chuyển sang `completed`, tiêu đề gạch ngang, bộ đếm "Đã xong" +1.

### TC-04: Lọc theo Mức độ ưu tiên
- **Given:** Có 3 task (1 Cao, 1 Trung bình, 1 Thấp).
- **When:** Chọn bộ lọc Priority là "Cao".
- **Then:** Chỉ có 1 task mức độ Cao hiển thị trên giao diện.

### TC-05: Lưu trữ bền vững (F5 Refresh Test)
- **Given:** Đã có 2 task trong ứng dụng.
- **When:** Người dùng nhấn F5 (Tải lại trang).
- **Then:** Toàn bộ 2 task vẫn hiển thị chính xác trạng thái ban đầu.

---

*Tạo bởi AWF 4.0 - Design Phase*
