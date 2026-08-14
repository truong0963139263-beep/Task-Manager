import streamlit as st
import json
import os
from datetime import datetime, date

# --- Page Configuration ---
st.set_page_config(
    page_title="TaskFlow — Quản Lý Công Việc Cá Nhân",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern Styling ---
st.markdown("""
    <style>
    /* Dark & Glassmorphism Theme Accents */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .css-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 10px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Storage File Config ---
DATA_FILE = "tasks_data.json"

DEFAULT_TASKS = [
    {
        "id": "task_1723650001000",
        "title": "Chào mừng bạn đến với TaskFlow trên Streamlit! 🎉",
        "description": "Ứng dụng quản lý công việc cá nhân thông minh, nhẹ và trực quan.",
        "priority": "high",
        "status": "pending",
        "dueDate": datetime.now().strftime("%Y-%m-%d"),
        "createdAt": datetime.now().isoformat()
    },
    {
        "id": "task_1723650002000",
        "title": "Lên danh sách công việc trong tuần",
        "description": "Dùng khung 'Thêm công việc mới' ở cột bên trái để tạo nhiệm vụ mới.",
        "priority": "medium",
        "status": "pending",
        "dueDate": datetime.now().strftime("%Y-%m-%d"),
        "createdAt": datetime.now().isoformat()
    }
]

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_TASKS)
        return DEFAULT_TASKS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_TASKS

def save_data(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Initialize Session State
if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()

# --- Header ---
st.title("⚡ TaskFlow — Streamlit App")
st.caption("Ứng dụng quản lý công việc cá nhân chạy trên Streamlit Framework")

# --- Stats Dashboard ---
tasks = st.session_state.tasks
total_tasks = len(tasks)
completed_tasks = len([t for t in tasks if t["status"] == "completed"])
pending_tasks = total_tasks - completed_tasks
today_str = datetime.now().strftime("%Y-%m-%d")
overdue_tasks = len([t for t in tasks if t["status"] == "pending" and t.get("dueDate") and t.get("dueDate") < today_str])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng số việc", total_tasks)
col2.metric("Đang thực hiện", pending_tasks)
col3.metric("Đã hoàn thành", completed_tasks)
col4.metric("Quá hạn", overdue_tasks, delta_color="inverse")

st.divider()

# --- Sidebar: Form Thêm Mới & Actions ---
with st.sidebar:
    st.header("➕ Thêm Công Việc Mới")
    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Tên công việc *", placeholder="Nhập tên nhiệm vụ...")
        new_desc = st.text_area("Ghi chú / Mô tả", placeholder="Nhập ghi chú...")
        new_priority = st.selectbox("Mức độ ưu tiên", ["low", "medium", "high"], 
                                   format_func=lambda x: "🔴 Cao" if x == "high" else ("🟡 Trung bình" if x == "medium" else "🟢 Thấp"))
        new_due = st.date_input("Hạn chót (Deadline)", value=date.today())
        
        submitted = st.form_submit_button("💾 Lưu công việc", use_container_width=True)
        if submitted:
            if new_title.strip():
                new_task = {
                    "id": f"task_{int(datetime.now().timestamp()*1000)}",
                    "title": new_title.strip(),
                    "description": new_desc.strip(),
                    "priority": new_priority,
                    "status": "pending",
                    "dueDate": new_due.strftime("%Y-%m-%d"),
                    "createdAt": datetime.now().isoformat()
                }
                st.session_state.tasks.insert(0, new_task)
                save_data(st.session_state.tasks)
                st.success("Thêm mới thành công!")
                st.rerun()
            else:
                st.error("Vui lòng nhập tên công việc!")

    st.divider()
    st.header("⚙️ Tiện Ích & Sao Lưu")
    
    # Export JSON
    json_data = json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2)
    st.download_button(
        label="📥 Xuất dữ liệu JSON",
        data=json_data,
        file_name=f"taskflow_backup_{today_str}.json",
        mime="application/json",
        use_container_width=True
    )
    
    # Import JSON
    uploaded_file = st.file_uploader("📤 Phục hồi từ file JSON", type=["json"])
    if uploaded_file is not None:
        try:
            imported = json.load(uploaded_file)
            if isinstance(imported, list):
                st.session_state.tasks = imported
                save_data(imported)
                st.success("Phục hồi dữ liệu thành công!")
                st.rerun()
        except Exception:
            st.error("File JSON không hợp lệ!")

    # Clear completed
    if st.button("🧹 Dọn việc đã xong", use_container_width=True):
        st.session_state.tasks = [t for t in st.session_state.tasks if t["status"] != "completed"]
        save_data(st.session_state.tasks)
        st.success("Đã dọn dẹp các việc hoàn thành!")
        st.rerun()

# --- Main Toolbar: Search & Filters ---
filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

with filter_col1:
    search_query = st.text_input("🔍 Tìm kiếm công việc", placeholder="Nhập từ khóa...")

with filter_col2:
    status_filter = st.selectbox("Lọc trạng thái", ["Tất cả", "Đang làm", "Đã xong", "Quá hạn"])

with filter_col3:
    sort_by = st.selectbox("Sắp xếp", ["Mới nhất", "Ưu tiên cao", "Hạn chót"])

# --- Filter & Sort Logic ---
filtered_tasks = st.session_state.tasks.copy()

# Search Filter
if search_query.strip():
    q = search_query.lower().strip()
    filtered_tasks = [t for t in filtered_tasks if q in t["title"].lower() or q in t.get("description", "").lower()]

# Status Filter
if status_filter == "Đang làm":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == "pending"]
elif status_filter == "Đã xong":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == "completed"]
elif status_filter == "Quá hạn":
    filtered_tasks = [t for t in filtered_tasks if t["status"] == "pending" and t.get("dueDate") and t["dueDate"] < today_str]

# Sort Logic
priority_weights = {"high": 3, "medium": 2, "low": 1}
if sort_by == "Ưu tiên cao":
    filtered_tasks.sort(key=lambda x: priority_weights.get(x.get("priority", "low"), 1), reverse=True)
elif sort_by == "Hạn chót":
    filtered_tasks.sort(key=lambda x: x.get("dueDate", "9999-99-99"))
else:
    filtered_tasks.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

# --- Render Task List ---
st.subheader("📋 Danh Sách Công Việc")

if not filtered_tasks:
    st.info("📌 Không có công việc nào phù hợp với bộ lọc hiện tại.")
else:
    for idx, task in enumerate(filtered_tasks):
        with st.container():
            c1, c2, c3 = st.columns([0.5, 4, 1.5])
            
            # Checkbox Status Toggle
            is_done = task["status"] == "completed"
            checked = c1.checkbox("", value=is_done, key=f"check_{task['id']}")
            if checked != is_done:
                task["status"] = "completed" if checked else "pending"
                save_data(st.session_state.tasks)
                st.rerun()
                
            # Task Content
            with c2:
                title_style = f"~~{task['title']}~~" if is_done else f"**{task['title']}**"
                st.markdown(title_style)
                if task.get("description"):
                    st.caption(task["description"])
                    
            # Badges & Actions
            with c3:
                p = task.get("priority", "medium")
                p_label = "🔴 Cao" if p == "high" else ("🟡 Trung bình" if p == "medium" else "🟢 Thấp")
                due = task.get("dueDate", "")
                
                st.write(f"{p_label} | 📅 {due if due else 'Không có hạn'}")
                if st.button("🗑️ Xóa", key=f"del_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    save_data(st.session_state.tasks)
                    st.success("Đã xóa công việc!")
                    st.rerun()
            st.divider()
