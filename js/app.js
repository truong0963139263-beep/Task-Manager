/* ==========================================================================
   TaskFlow Pro Main Entry Controller (KPI Analytics & View Nav Controller)
   ========================================================================== */

import { 
  getTasks, 
  addTask, 
  updateTask, 
  deleteTask, 
  toggleTaskStatus, 
  clearCompletedTasks,
  filterAndSortTasks,
  exportTasksJSON,
  importTasksJSON,
  getSettings, 
  saveSettings 
} from './storage.js';

import { 
  renderTaskList, 
  updateStats, 
  renderKPIDashboard,
  showToast 
} from './ui.js';

// Application State
let currentFilter = 'all'; // 'all' | 'pending' | 'completed' | 'overdue'
let searchQuery = '';
let priorityFilter = 'all'; // 'all' | 'high' | 'medium' | 'low'
let sortBy = 'createdAt'; // 'createdAt' | 'priority' | 'dueDate'

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavTabs();
  initEventListeners();
  initKeyboardShortcuts();
  refreshApp();
});

/**
 * Initialize Light/Dark Theme
 */
function initTheme() {
  const settings = getSettings();
  document.documentElement.setAttribute('data-theme', settings.theme || 'dark');
  updateThemeIcon(settings.theme || 'dark');
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#theme-toggle-btn i');
  if (!icon) return;
  if (theme === 'light') {
    icon.className = 'fa-solid fa-sun';
  } else {
    icon.className = 'fa-solid fa-moon';
  }
}

/**
 * Navigation View Tabs Switcher (Tasks vs KPI Analytics)
 */
function initNavTabs() {
  const navTabs = document.querySelectorAll('.nav-tab');
  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      navTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const targetView = tab.dataset.view;
      document.querySelectorAll('.app-view').forEach(view => view.classList.remove('active-view'));

      if (targetView === 'kpi') {
        document.getElementById('view-kpi').classList.add('active-view');
        renderKPIDashboard(getTasks());
      } else {
        document.getElementById('view-tasks').classList.add('active-view');
      }
    });
  });
}

/**
 * Keyboard Shortcuts
 */
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const modal = document.getElementById('task-modal');
      if (modal.classList.contains('open')) {
        modal.classList.remove('open');
      }
      return;
    }

    const activeEl = document.activeElement;
    const isEditingText = activeEl && (activeEl.tagName === 'INPUT' || activeEl.tagName === 'TEXTAREA' || activeEl.tagName === 'SELECT');

    if (( (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k' ) || (!isEditingText && e.key === '/')) {
      e.preventDefault();
      const searchInput = document.getElementById('search-input');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
      return;
    }

    if (!isEditingText && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'n') {
      e.preventDefault();
      document.getElementById('add-task-btn').click();
      return;
    }
  });
}

/**
 * Register Event Listeners
 */
function initEventListeners() {
  // Theme Toggle Button
  document.getElementById('theme-toggle-btn').addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    updateThemeIcon(newTheme);
    saveSettings({ theme: newTheme });
  });

  // Export JSON Backup Button
  document.getElementById('export-btn').addEventListener('click', () => {
    const jsonStr = exportTasksJSON();
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `taskflow_kpi_backup_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Xuất file backup dữ liệu thành công!');
  });

  // Import JSON File Button
  const importFileInput = document.getElementById('import-file-input');
  document.getElementById('import-btn').addEventListener('click', () => {
    importFileInput.click();
  });

  importFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target.result;
      const success = importTasksJSON(content);
      if (success) {
        showToast('Khôi phục dữ liệu JSON thành công!');
        refreshApp();
      } else {
        showToast('File JSON không hợp lệ!', 'error');
      }
      importFileInput.value = '';
    };
    reader.readAsText(file);
  });

  // Clickable Stat Cards
  document.querySelectorAll('.stat-card.clickable').forEach(card => {
    card.addEventListener('click', () => {
      const filterType = card.dataset.statFilter;
      currentFilter = filterType;
      
      document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.dataset.filter === filterType) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });

      refreshApp();
    });
  });

  // Filter Tabs
  document.getElementById('filter-tabs').addEventListener('click', (e) => {
    if (e.target.classList.contains('filter-btn')) {
      document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
      e.target.classList.add('active');
      currentFilter = e.target.dataset.filter;
      refreshApp();
    }
  });

  // Priority Filter Select
  document.getElementById('priority-filter-select').addEventListener('change', (e) => {
    priorityFilter = e.target.value;
    refreshApp();
  });

  // Sort Select
  document.getElementById('sort-by-select').addEventListener('change', (e) => {
    sortBy = e.target.value;
    refreshApp();
  });

  // Clear Completed Tasks Button
  document.getElementById('clear-completed-btn').addEventListener('click', () => {
    const tasks = getTasks();
    const completedCount = tasks.filter(t => t.status === 'completed').length;
    
    if (completedCount === 0) {
      showToast('Không có công việc nào đã hoàn thành.', 'info');
      return;
    }

    if (confirm(`Bạn có chắc chắn muốn dọn dẹp ${completedCount} công việc đã hoàn thành không?`)) {
      const deleted = clearCompletedTasks();
      showToast(`Đã dọn dẹp ${deleted} công việc đã hoàn thành!`);
      refreshApp();
    }
  });

  // Search Input
  document.getElementById('search-input').addEventListener('input', (e) => {
    searchQuery = e.target.value;
    refreshApp();
  });

  // Modal Control
  const modal = document.getElementById('task-modal');
  const openModalBtn = document.getElementById('add-task-btn');
  const closeModalBtn = document.getElementById('close-modal-btn');
  const cancelModalBtn = document.getElementById('cancel-modal-btn');
  const taskForm = document.getElementById('task-form');

  const openModal = (task = null) => {
    taskForm.reset();
    if (task) {
      document.getElementById('modal-heading').textContent = 'Chỉnh sửa công việc';
      document.getElementById('task-id').value = task.id;
      document.getElementById('task-title-input').value = task.title;
      document.getElementById('task-desc-input').value = task.description || '';
      document.getElementById('task-priority-input').value = task.priority;
      document.getElementById('task-date-input').value = task.dueDate || '';
    } else {
      document.getElementById('modal-heading').textContent = 'Thêm công việc mới';
      document.getElementById('task-id').value = '';
    }
    modal.classList.add('open');
    document.getElementById('task-title-input').focus();
  };

  const closeModal = () => modal.classList.remove('open');

  openModalBtn.addEventListener('click', () => openModal());
  closeModalBtn.addEventListener('click', closeModal);
  cancelModalBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  // Form Submit
  taskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const id = document.getElementById('task-id').value;
    const title = document.getElementById('task-title-input').value;
    const description = document.getElementById('task-desc-input').value;
    const priority = document.getElementById('task-priority-input').value;
    const dueDate = document.getElementById('task-date-input').value;

    try {
      if (id) {
        updateTask(id, { title, description, priority, dueDate });
        showToast('Cập nhật công việc thành công!');
      } else {
        addTask({ title, description, priority, dueDate });
        showToast('Thêm mới công việc thành công!');
      }
      closeModal();
      refreshApp();
    } catch (err) {
      showToast(err.message || 'Lỗi khi lưu dữ liệu', 'error');
    }
  });

  // Task Grid Delegation
  const taskGrid = document.getElementById('task-grid');
  taskGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.task-card');
    if (!card) return;
    const taskId = card.dataset.id;

    if (e.target.closest('[data-action="toggle"]')) {
      const updated = toggleTaskStatus(taskId);
      if (updated) {
        showToast(updated.status === 'completed' ? 'Đã hoàn thành công việc!' : 'Đã chuyển về đang làm');
        refreshApp();
      }
      return;
    }

    if (e.target.closest('[data-action="edit"]')) {
      const tasks = getTasks();
      const task = tasks.find(t => t.id === taskId);
      if (task) openModal(task);
      return;
    }

    if (e.target.closest('[data-action="delete"]')) {
      if (confirm('Bạn có chắc chắn muốn xóa công việc này không?')) {
        deleteTask(taskId);
        showToast('Đã xóa công việc!');
        refreshApp();
      }
      return;
    }
  });
}

/**
 * Filter & Refresh App UI
 */
function refreshApp() {
  const allTasks = getTasks();

  const filteredTasks = filterAndSortTasks(allTasks, {
    statusFilter: currentFilter,
    searchQuery: searchQuery,
    priorityFilter: priorityFilter,
    sortBy: sortBy
  });

  const taskGrid = document.getElementById('task-grid');
  const emptyState = document.getElementById('empty-state');

  renderTaskList(filteredTasks, taskGrid, emptyState, {
    currentFilter,
    searchQuery,
    priorityFilter
  });
  
  updateStats(allTasks, currentFilter);
}
