/* ==========================================================================
   TaskFlow UI Rendering & DOM Manipulation Module (Phase 03 UI Components)
   ========================================================================== */

import { getTaskStats } from './storage.js';

/**
 * Format Priority Text & Badge CSS Class
 */
function getPriorityBadge(priority) {
  switch (priority) {
    case 'high':
      return `<span class="badge badge-high"><i class="fa-solid fa-fire"></i> Cao</span>`;
    case 'medium':
      return `<span class="badge badge-medium"><i class="fa-solid fa-triangle-exclamation"></i> Trung bình</span>`;
    case 'low':
      return `<span class="badge badge-low"><i class="fa-solid fa-leaf"></i> Thấp</span>`;
    default:
      return `<span class="badge badge-low">Bình thường</span>`;
  }
}

/**
 * Format Due Date Text with Overdue/Today Indicators
 */
function formatDueDate(dueDateStr) {
  if (!dueDateStr) return '';
  const todayStr = new Date().toISOString().split('T')[0];
  const isOverdue = dueDateStr < todayStr;
  const isToday = dueDateStr === todayStr;

  let styleClass = isOverdue 
    ? 'color: var(--priority-high); font-weight: 600;' 
    : (isToday ? 'color: var(--priority-medium); font-weight: 600;' : 'color: var(--text-secondary);');
  
  let label = dueDateStr;
  if (isToday) label = 'Hôm nay';
  if (isOverdue) label = `Quá hạn (${dueDateStr})`;

  return `<span style="${styleClass}"><i class="fa-regular fa-calendar"></i> ${label}</span>`;
}

/**
 * Render list of Task Cards with Empty State customization
 * @param {Array} tasks 
 * @param {HTMLElement} container 
 * @param {HTMLElement} emptyState 
 * @param {Object} context { currentFilter, searchQuery, priorityFilter }
 */
export function renderTaskList(tasks, container, emptyState, context = {}) {
  container.querySelectorAll('.task-card').forEach(card => card.remove());

  if (tasks.length === 0) {
    emptyState.style.display = 'block';
    
    // Dynamic Empty State Messages
    const titleEl = document.getElementById('empty-title');
    const subEl = document.getElementById('empty-sub');

    if (context.searchQuery) {
      titleEl.textContent = 'Không tìm thấy kết quả';
      subEl.textContent = `Không có công việc nào khớp với từ khóa "${context.searchQuery}"`;
    } else if (context.currentFilter === 'completed') {
      titleEl.textContent = 'Chưa có việc nào hoàn thành';
      subEl.textContent = 'Hãy hoàn thành các công việc trong danh sách để xem ở đây!';
    } else if (context.currentFilter === 'overdue') {
      titleEl.textContent = 'Không có công việc nào quá hạn';
      subEl.textContent = 'Tuyệt vời! Bạn đang theo rất sát tiến độ công việc.';
    } else if (context.priorityFilter && context.priorityFilter !== 'all') {
      titleEl.textContent = 'Không có công việc nào ở độ ưu tiên này';
      subEl.textContent = 'Thử chuyển sang chọn mức ưu tiên khác hoặc tất cả.';
    } else {
      titleEl.textContent = 'Chưa có công việc nào';
      subEl.textContent = 'Hãy bấm nút "Thêm công việc" để tạo nhiệm vụ mới ngay!';
    }

    return;
  }

  emptyState.style.display = 'none';

  tasks.forEach(task => {
    const card = document.createElement('div');
    card.className = `task-card ${task.status === 'completed' ? 'completed' : ''}`;
    card.dataset.id = task.id;

    card.innerHTML = `
      <div class="task-card-header">
        <div class="custom-checkbox" data-action="toggle" title="Đánh dấu hoàn thành">
          ${task.status === 'completed' ? '<i class="fa-solid fa-check"></i>' : ''}
        </div>
        <div style="flex: 1;">
          <h3 class="task-title">${escapeHTML(task.title)}</h3>
          ${task.description ? `<p class="task-desc">${escapeHTML(task.description)}</p>` : ''}
        </div>
      </div>

      <div class="task-card-footer">
        <div class="task-badges">
          ${getPriorityBadge(task.priority)}
          ${formatDueDate(task.dueDate)}
        </div>
        <div class="task-actions">
          <button class="action-btn edit" data-action="edit" title="Chỉnh sửa công việc">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="action-btn delete" data-action="delete" title="Xóa công việc">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}

/**
 * Update Header Stats Cards & Active Ring Effect
 * @param {Array} tasks 
 * @param {string} activeFilter 
 */
export function updateStats(tasks, activeFilter = 'all') {
  const stats = getTaskStats(tasks);

  document.getElementById('stat-total').textContent = stats.total;
  document.getElementById('stat-pending').textContent = stats.pending;
  document.getElementById('stat-completed').textContent = stats.completed;
  document.getElementById('stat-overdue').textContent = stats.overdue;

  // Highlight active stat card
  document.querySelectorAll('.stat-card').forEach(card => {
    if (card.dataset.statFilter === activeFilter) {
      card.classList.add('active-stat');
    } else {
      card.classList.remove('active-stat');
    }
  });
}

/**
 * Show Toast Notification
 * @param {string} message 
 * @param {string} type 'success' | 'info' | 'error'
 */
export function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  let icon = '<i class="fa-solid fa-circle-check" style="color: var(--status-completed);"></i>';
  if (type === 'error') icon = '<i class="fa-solid fa-circle-xmark" style="color: var(--priority-high);"></i>';

  toast.innerHTML = `${icon} <span>${escapeHTML(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, 
    tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag)
  );
}
