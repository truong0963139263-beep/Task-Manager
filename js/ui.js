/* ==========================================================================
   TaskFlow Pro UI Rendering & KPI Analytics Module
   ========================================================================== */

import { getTaskStats } from './storage.js';

let priorityChartInstance = null;
let statusChartInstance = null;

/**
 * Format Priority Badge
 */
function getPriorityBadge(priority) {
  switch (priority) {
    case 'high':
      return `<span class="badge badge-high"><i class="fa-solid fa-fire"></i> Cao</span>`;
    case 'medium':
      return `<span class="badge badge-medium"><i class="fa-solid fa-triangle-exclamation"></i> TB</span>`;
    case 'low':
      return `<span class="badge badge-low"><i class="fa-solid fa-leaf"></i> Thấp</span>`;
    default:
      return `<span class="badge badge-low">Bình thường</span>`;
  }
}

/**
 * Format Due Date Text
 */
function formatDueDate(dueDateStr) {
  if (!dueDateStr) return '';
  const todayStr = new Date().toISOString().split('T')[0];
  const isOverdue = dueDateStr < todayStr;
  const isToday = dueDateStr === todayStr;

  let styleClass = isOverdue 
    ? 'color: var(--priority-high); font-weight: 700;' 
    : (isToday ? 'color: var(--priority-medium); font-weight: 700;' : 'color: var(--text-secondary);');
  
  let label = dueDateStr;
  if (isToday) label = 'Hôm nay';
  if (isOverdue) label = `Quá hạn (${dueDateStr})`;

  return `<span style="${styleClass}"><i class="fa-regular fa-calendar"></i> ${label}</span>`;
}

/**
 * Render list of Task Cards
 */
export function renderTaskList(tasks, container, emptyState, context = {}) {
  container.querySelectorAll('.task-card').forEach(card => card.remove());

  if (tasks.length === 0) {
    emptyState.style.display = 'block';
    
    const titleEl = document.getElementById('empty-title');
    const subEl = document.getElementById('empty-sub');

    if (context.searchQuery) {
      titleEl.textContent = 'Không tìm thấy kết quả';
      subEl.textContent = `Không có công việc nào khớp với từ khóa "${context.searchQuery}"`;
    } else if (context.currentFilter === 'completed') {
      titleEl.textContent = 'Chưa có việc nào hoàn thành';
      subEl.textContent = 'Hãy hoàn thành các công việc trong danh sách!';
    } else if (context.currentFilter === 'overdue') {
      titleEl.textContent = 'Không có công việc nào quá hạn';
      subEl.textContent = 'Tuyệt vời! Bạn đang kiểm soát hạn chót rất tốt.';
    } else {
      titleEl.textContent = 'Chưa có công việc nào';
      subEl.textContent = 'Hãy bấm nút "Thêm công việc" để tạo nhiệm vụ mới!';
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
          <button class="action-btn edit" data-action="edit" title="Chỉnh sửa">
            <i class="fa-solid fa-pen"></i>
          </button>
          <button class="action-btn delete" data-action="delete" title="Xóa">
            <i class="fa-solid fa-trash-can"></i>
          </button>
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}

/**
 * Update Stats Header Cards
 */
export function updateStats(tasks, activeFilter = 'all') {
  const stats = getTaskStats(tasks);

  document.getElementById('stat-total').textContent = stats.total;
  document.getElementById('stat-pending').textContent = stats.pending;
  document.getElementById('stat-completed').textContent = stats.completed;
  document.getElementById('stat-overdue').textContent = stats.overdue;

  document.querySelectorAll('.stat-card').forEach(card => {
    if (card.dataset.statFilter === activeFilter) {
      card.classList.add('active-stat');
    } else {
      card.classList.remove('active-stat');
    }
  });

  // Automatically refresh KPI Analytics Dashboard
  renderKPIDashboard(tasks);
}

/**
 * Render KPI Analytics Dashboard & Chart.js Visualizations
 */
export function renderKPIDashboard(tasks) {
  const stats = getTaskStats(tasks);
  const total = stats.total || 1;
  const completed = stats.completed;
  const overdue = stats.overdue;
  const highCount = tasks.filter(t => t.priority === 'high').length;
  const mediumCount = tasks.filter(t => t.priority === 'medium').length;
  const lowCount = tasks.filter(t => t.priority === 'low').length;

  // Completion Rate
  const completionRate = Math.round((completed / total) * 100);
  const onTimeRate = completed > 0 ? Math.round(((completed - overdue) / completed) * 100) : 100;
  const finalOnTimeRate = Math.max(0, onTimeRate);

  // Overall KPI Productivity Score (0-100)
  const kpiScore = total === 0 ? 0 : Math.round((completionRate * 0.7) + (finalOnTimeRate * 0.3));

  // Update Score Elements
  const scoreValEl = document.getElementById('kpi-score-val');
  const scoreBadgeEl = document.getElementById('kpi-score-badge');
  if (scoreValEl) scoreValEl.textContent = `${kpiScore}%`;
  
  if (scoreBadgeEl) {
    if (kpiScore >= 80) {
      scoreBadgeEl.textContent = '🌟 Xuất Sắc';
    } else if (kpiScore >= 50) {
      scoreBadgeEl.textContent = '🔥 Tốt';
    } else {
      scoreBadgeEl.textContent = '⚡ Cần Cố Gắng';
    }
  }

  // Update KPI Metric Cards & Progress Bars
  const compRateEl = document.getElementById('kpi-completion-rate');
  const compBarEl = document.getElementById('kpi-completion-bar');
  const compSubEl = document.getElementById('kpi-completion-sub');
  if (compRateEl) compRateEl.textContent = `${completionRate}%`;
  if (compBarEl) compBarEl.style.width = `${completionRate}%`;
  if (compSubEl) compSubEl.textContent = `${completed}/${stats.total} công việc đã xong`;

  const ontimeRateEl = document.getElementById('kpi-ontime-rate');
  const ontimeBarEl = document.getElementById('kpi-ontime-bar');
  const ontimeSubEl = document.getElementById('kpi-ontime-sub');
  if (ontimeRateEl) ontimeRateEl.textContent = `${finalOnTimeRate}%`;
  if (ontimeBarEl) ontimeBarEl.style.width = `${finalOnTimeRate}%`;
  if (ontimeSubEl) ontimeSubEl.textContent = overdue === 0 ? 'Không có công việc trễ hạn' : `${overdue} công việc trễ hạn`;

  const highCountEl = document.getElementById('kpi-high-count');
  const highBarEl = document.getElementById('kpi-high-bar');
  if (highCountEl) highCountEl.textContent = highCount;
  if (highBarEl) highBarEl.style.width = `${Math.min(100, (highCount / total) * 100)}%`;

  const overdueCountEl = document.getElementById('kpi-overdue-count');
  const overdueBarEl = document.getElementById('kpi-overdue-bar');
  if (overdueCountEl) overdueCountEl.textContent = overdue;
  if (overdueBarEl) overdueBarEl.style.width = `${Math.min(100, (overdue / total) * 100)}%`;

  // Render Chart.js Visualizations if Chart library is loaded
  if (typeof Chart !== 'undefined') {
    renderPriorityChart(highCount, mediumCount, lowCount);
    renderStatusChart(stats.pending, stats.completed, stats.overdue);
  }
}

/**
 * Priority Distribution Donut Chart
 */
function renderPriorityChart(high, medium, low) {
  const ctx = document.getElementById('priorityChart');
  if (!ctx) return;

  if (priorityChartInstance) {
    priorityChartInstance.destroy();
  }

  priorityChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['🔴 Cao (Khẩn cấp)', '🟡 Trung bình', '🟢 Thấp'],
      datasets: [{
        data: [high, medium, low],
        backgroundColor: ['#f43f5e', '#f59e0b', '#10b981'],
        borderWidth: 0,
        hoverOffset: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12 } }
        }
      }
    }
  });
}

/**
 * Status Breakdown Bar Chart
 */
function renderStatusChart(pending, completed, overdue) {
  const ctx = document.getElementById('statusChart');
  if (!ctx) return;

  if (statusChartInstance) {
    statusChartInstance.destroy();
  }

  statusChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['⚡ Đang làm', '✅ Hoàn thành', '🚨 Quá hạn'],
      datasets: [{
        label: 'Số lượng công việc',
        data: [pending, completed, overdue],
        backgroundColor: ['#3b82f6', '#10b981', '#f43f5e'],
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
        y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255,255,255,0.05)' } }
      }
    }
  });
}

/**
 * Show Toast Notification
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
