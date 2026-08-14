/* ==========================================================================
   TaskFlow Storage Manager Module (Phase 02 - Data Layer & Persistence)
   Handles LocalStorage CRUD, Data Sanitization, Sorting, Filtering & Export/Import
   ========================================================================== */

const STORAGE_KEY_ITEMS = 'taskflow_items_v1';
const STORAGE_KEY_SETTINGS = 'taskflow_settings_v1';

/**
 * Priority Weights for sorting algorithms
 */
const PRIORITY_WEIGHTS = {
  high: 3,
  medium: 2,
  low: 1
};

/**
 * Default initial mock data for first-time usage
 */
const DEFAULT_TASKS = [
  {
    id: 'task_1723650001000',
    title: 'Chào mừng bạn đến với TaskFlow! 🎉',
    description: 'Thử đánh dấu hoàn thành công việc này bằng cách click vào ô checkbox bên trái.',
    priority: 'high',
    status: 'pending',
    dueDate: new Date().toISOString().split('T')[0],
    createdAt: new Date(Date.now() - 3600000).toISOString()
  },
  {
    id: 'task_1723650002000',
    title: 'Lên danh sách công việc trong tuần',
    description: 'Bấm nút "+ Thêm công việc" ở góc phải để tạo thêm các nhiệm vụ mới.',
    priority: 'medium',
    status: 'pending',
    dueDate: new Date(Date.now() + 86400000 * 2).toISOString().split('T')[0],
    createdAt: new Date().toISOString()
  },
  {
    id: 'task_1723650003000',
    title: 'Khởi tạo ứng dụng thành công',
    description: 'Hệ thống đã tự động lưu dữ liệu vào trình duyệt của bạn qua LocalStorage.',
    priority: 'low',
    status: 'completed',
    dueDate: new Date().toISOString().split('T')[0],
    createdAt: new Date(Date.now() - 7200000).toISOString()
  }
];

/**
 * Check if LocalStorage is available in current browser environment
 * @returns {boolean}
 */
function isStorageAvailable() {
  try {
    const testKey = '__storage_test__';
    window.localStorage.setItem(testKey, testKey);
    window.localStorage.removeItem(testKey);
    return true;
  } catch (e) {
    return false;
  }
}

// In-memory fallback if LocalStorage is disabled/blocked
let memoryStorage = null;

/**
 * Fetch all tasks from LocalStorage or Memory Fallback
 * @returns {Array} List of task objects
 */
export function getTasks() {
  if (!isStorageAvailable()) {
    return memoryStorage || DEFAULT_TASKS;
  }

  try {
    const rawData = localStorage.getItem(STORAGE_KEY_ITEMS);
    if (!rawData) {
      saveTasks(DEFAULT_TASKS);
      return DEFAULT_TASKS;
    }
    const parsed = JSON.parse(rawData);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error('Lỗi khi đọc dữ liệu từ LocalStorage:', error);
    return [];
  }
}

/**
 * Save array of tasks to LocalStorage or Memory Fallback
 * @param {Array} tasks 
 */
export function saveTasks(tasks) {
  if (!isStorageAvailable()) {
    memoryStorage = tasks;
    return;
  }

  try {
    localStorage.setItem(STORAGE_KEY_ITEMS, JSON.stringify(tasks));
  } catch (error) {
    console.error('Lỗi khi lưu dữ liệu vào LocalStorage:', error);
  }
}

/**
 * Add a new task with validation
 * @param {Object} taskData 
 * @returns {Object} Newly created task
 */
export function addTask(taskData) {
  if (!taskData || !taskData.title || !taskData.title.trim()) {
    throw new Error('Tên công việc không được để trống.');
  }

  const tasks = getTasks();
  const newTask = {
    id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
    title: taskData.title.trim(),
    description: (taskData.description || '').trim(),
    priority: ['high', 'medium', 'low'].includes(taskData.priority) ? taskData.priority : 'medium',
    status: 'pending',
    dueDate: taskData.dueDate || '',
    createdAt: new Date().toISOString()
  };

  tasks.unshift(newTask);
  saveTasks(tasks);
  return newTask;
}

/**
 * Update an existing task by ID
 * @param {string} id 
 * @param {Object} updates 
 * @returns {Object|null} Updated task or null
 */
export function updateTask(id, updates) {
  const tasks = getTasks();
  const index = tasks.findIndex(t => t.id === id);
  if (index === -1) return null;

  const currentTask = tasks[index];
  const updatedTask = {
    ...currentTask,
    ...updates,
    title: updates.title !== undefined ? updates.title.trim() : currentTask.title,
    description: updates.description !== undefined ? updates.description.trim() : currentTask.description,
    priority: updates.priority && ['high', 'medium', 'low'].includes(updates.priority) ? updates.priority : currentTask.priority
  };

  tasks[index] = updatedTask;
  saveTasks(tasks);
  return updatedTask;
}

/**
 * Delete a task by ID
 * @param {string} id 
 * @returns {boolean} True if deleted successfully
 */
export function deleteTask(id) {
  const tasks = getTasks();
  const filtered = tasks.filter(t => t.id !== id);
  saveTasks(filtered);
  return filtered.length !== tasks.length;
}

/**
 * Toggle task completion status
 * @param {string} id 
 * @returns {Object|null} Updated task
 */
export function toggleTaskStatus(id) {
  const tasks = getTasks();
  const task = tasks.find(t => t.id === id);
  if (!task) return null;

  const newStatus = task.status === 'completed' ? 'pending' : 'completed';
  return updateTask(id, { status: newStatus });
}

/**
 * Delete all completed tasks (Batch Clean)
 * @returns {number} Count of deleted tasks
 */
export function clearCompletedTasks() {
  const tasks = getTasks();
  const remaining = tasks.filter(t => t.status !== 'completed');
  const deletedCount = tasks.length - remaining.length;
  saveTasks(remaining);
  return deletedCount;
}

/**
 * Advanced Filtering & Sorting helper
 * @param {Array} tasks 
 * @param {Object} options { statusFilter, searchQuery, priorityFilter, sortBy }
 * @returns {Array} Filtered and sorted tasks
 */
export function filterAndSortTasks(tasks, options = {}) {
  const { 
    statusFilter = 'all', 
    searchQuery = '', 
    priorityFilter = 'all', 
    sortBy = 'createdAt' 
  } = options;

  const query = searchQuery.toLowerCase().trim();
  const todayStr = new Date().toISOString().split('T')[0];

  return tasks.filter(task => {
    // Status Filter
    if (statusFilter === 'pending' && task.status !== 'pending') return false;
    if (statusFilter === 'completed' && task.status !== 'completed') return false;
    if (statusFilter === 'overdue') {
      if (task.status === 'completed' || !task.dueDate || task.dueDate >= todayStr) return false;
    }

    // Priority Filter
    if (priorityFilter !== 'all' && task.priority !== priorityFilter) return false;

    // Search Query Matching
    if (query) {
      const matchTitle = task.title.toLowerCase().includes(query);
      const matchDesc = (task.description || '').toLowerCase().includes(query);
      if (!matchTitle && !matchDesc) return false;
    }

    return true;
  }).sort((a, b) => {
    if (sortBy === 'priority') {
      return (PRIORITY_WEIGHTS[b.priority] || 0) - (PRIORITY_WEIGHTS[a.priority] || 0);
    }
    if (sortBy === 'dueDate') {
      if (!a.dueDate) return 1;
      if (!b.dueDate) return -1;
      return a.dueDate.localeCompare(b.dueDate);
    }
    // Default: Sort by Created At (Newest First)
    return new Date(b.createdAt) - new Date(a.createdAt);
  });
}

/**
 * Calculate Overview Statistics
 * @param {Array} tasks 
 * @returns {Object} Stats object { total, pending, completed, overdue, dueToday }
 */
export function getTaskStats(tasks = getTasks()) {
  const todayStr = new Date().toISOString().split('T')[0];
  const total = tasks.length;
  const completed = tasks.filter(t => t.status === 'completed').length;
  const pending = total - completed;
  const overdue = tasks.filter(t => t.status === 'pending' && t.dueDate && t.dueDate < todayStr).length;
  const dueToday = tasks.filter(t => t.status === 'pending' && t.dueDate === todayStr).length;

  return { total, pending, completed, overdue, dueToday };
}

/**
 * Export tasks as JSON backup string
 * @returns {string} JSON String
 */
export function exportTasksJSON() {
  const tasks = getTasks();
  return JSON.stringify(tasks, null, 2);
}

/**
 * Import tasks from JSON backup string
 * @param {string} jsonStr 
 * @returns {boolean} Success status
 */
export function importTasksJSON(jsonStr) {
  try {
    const parsed = JSON.parse(jsonStr);
    if (Array.isArray(parsed)) {
      saveTasks(parsed);
      return true;
    }
    return false;
  } catch (e) {
    console.error('Import JSON thất bại:', e);
    return false;
  }
}

/**
 * Get App Settings (Theme, etc.)
 */
export function getSettings() {
  if (!isStorageAvailable()) return { theme: 'dark', sortBy: 'createdAt' };
  try {
    const data = localStorage.getItem(STORAGE_KEY_SETTINGS);
    return data ? JSON.parse(data) : { theme: 'dark', sortBy: 'createdAt' };
  } catch (e) {
    return { theme: 'dark', sortBy: 'createdAt' };
  }
}

/**
 * Save App Settings
 */
export function saveSettings(settings) {
  if (!isStorageAvailable()) return;
  try {
    const current = getSettings();
    localStorage.setItem(STORAGE_KEY_SETTINGS, JSON.stringify({ ...current, ...settings }));
  } catch (e) {
    console.error('Lỗi khi lưu settings:', e);
  }
}
