# Phase 01: Setup & Design System
Status: ✅ Complete
Dependencies: None

## Objective
Tạo cấu trúc dự án chuẩn, thiết lập Design System bằng CSS Variables (màu sắc, typography, shadows, border-radius) và tạo khung HTML5 cơ bản.

## Implementation Steps
1. [x] Tạo cấu trúc thư mục dự án (`index.html`, `css/styles.css`, `js/app.js`, `js/storage.js`, `js/ui.js`).
2. [x] Xây dựng Design System trong `css/styles.css` (Color Palette: Primary Accent, Background Dark/Light, Card Surface, Priority Badges).
3. [x] Nhúng Google Fonts (Inter) & FontAwesome Icons.
4. [x] Tạo khung HTML5 semantic (`<header>`, `<main>`, `<sidebar>/<filters>`, `<section class="task-container">`).
5. [x] Đảm bảo ứng dụng hiển thị mượt mà trên trình duyệt.

## Files Created/Modified
- `index.html` - Khung HTML5 semantic ứng dụng TaskFlow.
- `css/styles.css` - Design System tokens, Layouts, Reset, Glassmorphism & Micro-animations.
- `js/storage.js` - Data persistence với LocalStorage API.
- `js/ui.js` - DOM Rendering helpers & Toast notifications.
- `js/app.js` - Controller chính của ứng dụng.

## Test Criteria
- [x] Mở `index.html` trên trình duyệt hiển thị đúng layout khung app.
- [x] Font chữ Inter và màu sắc hiển thị theo Design System.

---
Next Phase: [`phase-02-data-layer.md`](file:///c:/Henry%20AI/plans/260814-2020-task-manager/phase-02-data-layer.md)
