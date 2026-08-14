# Phase 02: Data Layer & Storage Manager
Status: ✅ Complete
Dependencies: Phase 01

## Objective
Xây dựng mô hình dữ liệu (Data Model) cho Task và Module quản lý lưu trữ dữ liệu bền vững qua Browser LocalStorage API (`js/storage.js`).

## Data Model Definition
```json
{
  "id": "task_1723650000000_a1b2",
  "title": "Hoàn thành báo cáo công việc",
  "description": "Mô tả chi tiết nhiệm vụ",
  "priority": "high", // 'high' | 'medium' | 'low'
  "status": "pending", // 'pending' | 'completed'
  "dueDate": "2026-08-20",
  "createdAt": "2026-08-14T20:20:00Z"
}
```

## Implementation Steps
1. [x] Định nghĩa Task Model & khởi tạo mock data tự động nếu chưa có dữ liệu trong LocalStorage.
2. [x] Xây dựng các hàm CRUD trong `js/storage.js`: `getTasks()`, `addTask(taskData)`, `updateTask(id, updates)`, `deleteTask(id)`, `toggleTaskStatus(id)`, `clearCompletedTasks()`.
3. [x] Xây dựng các hàm helper Lọc & Sắp xếp nâng cao: `filterAndSortTasks(tasks, { statusFilter, searchQuery, priorityFilter, sortBy })`.
4. [x] Viết hàm tính toán thống kê tổng quan `getTaskStats(tasks)` (Tổng số task, Đã xong, Đang làm, Quá hạn, Hạn hôm nay).
5. [x] Thêm các helper Backup & Restore: `exportTasksJSON()` và `importTasksJSON(jsonStr)`.

## Files Created/Modified
- `js/storage.js` - Data persistence layer, CRUD, Validation & Stats calculations.
- `js/ui.js` - Integration với Data Layer helpers.
- `js/app.js` - Controller kết nối Data Layer.

## Test Criteria
- [x] Mọi thao tác thêm/sửa/xóa task đều được lưu vào LocalStorage và duy trì sau khi F5 trang.
- [x] Hàm Lọc & Sắp xếp trả về dữ liệu chính xác tuyệt đối.

---
Next Phase: [`phase-03-ui-components.md`](file:///c:/Henry%20AI/plans/260814-2020-task-manager/phase-03-ui-components.md)
