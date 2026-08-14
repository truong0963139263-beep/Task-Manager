import streamlit as st
import json
import os
from datetime import datetime, date

# --- Page Configuration ---
st.set_page_config(
    page_title="TaskFlow Pro — Quản Lý Công Việc & Báo Cáo KPI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Ultra Modern Theme & Glassmorphism ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #090d16 0%, #131b2e 100%);
        color: #f8fafc;
    }
    .kpi-card {
        background: rgba(19, 27, 46, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .kpi-score-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.2) 100%);
        border: 1px solid rgba(99, 102, 241, 0.4);
        border-radius: 18px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Storage File Config ---
DATA_FILE = "tasks_data.json"

DEFAULT_TASKS = [
    {
        "id": "task_1723650001000",
        "title": "Chào mừng bạn đến với TaskFlow Pro trên Streamlit! 🎉",
        "description": "Ứng dụng quản lý công việc và báo cáo chỉ số KPI năng suất cá nhân.",
        "priority": "high",
        "status": "pending",
        "dueDate": datetime.now().strftime("%Y-%m-%d"),
        "createdAt": datetime.now().isoformat()
    },
    {
        "id": "task_1723650002000",
        "title": "Hoàn thành kế hoạch công việc tuần mới",
        "description": "Thêm các nhiệm vụ quan trọng vào danh sách để theo dõi chỉ số KPI.",
        "priority": "medium",
        "status": "completed",
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

if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()

# --- Header ---
st.title("📊 TaskFlow Pro — Quản Lý Task & Báo Cáo KPI")
st.caption("Hệ thống quản lý công việc & phân tích hiệu suất năng suất cá nhân")

# --- Tabs Navigation ---
tab_tasks, tab_kpi = st.tabs(["📋 Danh Sách Công Việc", "📊 Báo Cáo KPI & Analytics"])

# ==========================================
# TAB 1: DANH SÁCH CÔNG VIỆC
# ==========================================
with tab_tasks:
    tasks = st.session_state.tasks
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "completed"])
    pending_tasks = total_tasks - completed_tasks
    today_str = datetime.now().strftime("%Y-%m-%d")
    overdue_tasks = len([t for t in tasks if t["status"] == "pending" and t.get("dueDate") and t.get("dueDate") < today_str])

    # Header Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tổng Số Việc", total_tasks)
    m2.metric("Đang Thực Hiện", pending_tasks)
    m3.metric("Đã Hoàn Thành", completed_tasks)
    m4.metric("Quá Hạn KPI", overdue_tasks, delta_color="inverse")

    st.divider()

    # Toolbar: Filter & Search
    f1, f2, f3 = st.columns([2, 1, 1])
    with f1:
        search_query = st.text_input("🔍 Tìm kiếm công việc", placeholder="Nhập từ khóa...")
    with f2:
        status_filter = st.selectbox("Lọc trạng thái", ["Tất cả", "Đang làm", "Đã xong", "Quá hạn"])
    with f3:
        sort_by = st.selectbox("Sắp xếp", ["Mới nhất", "Ưu tiên cao", "Hạn chót"])

    # Filter Logic
    filtered_tasks = st.session_state.tasks.copy()
    if search_query.strip():
        q = search_query.lower().strip()
        filtered_tasks = [t for t in filtered_tasks if q in t["title"].lower() or q in t.get("description", "").lower()]

    if status_filter == "Đang làm":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "pending"]
    elif status_filter == "Đã xong":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "completed"]
    elif status_filter == "Quá hạn":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == "pending" and t.get("dueDate") and t["dueDate"] < today_str]

    priority_weights = {"high": 3, "medium": 2, "low": 1}
    if sort_by == "Ưu tiên cao":
        filtered_tasks.sort(key=lambda x: priority_weights.get(x.get("priority", "low"), 1), reverse=True)
    elif sort_by == "Hạn chót":
        filtered_tasks.sort(key=lambda x: x.get("dueDate", "9999-99-99"))
    else:
        filtered_tasks.sort(key=lambda x: x.get("createdAt", ""), reverse=True)

    # Task Cards Rendering
    if not filtered_tasks:
        st.info("📌 Không tìm thấy công việc nào phù hợp.")
    else:
        for task in filtered_tasks:
            with st.container():
                c1, c2, c3 = st.columns([0.5, 4, 1.5])
                is_done = task["status"] == "completed"
                checked = c1.checkbox("", value=is_done, key=f"cb_{task['id']}")
                if checked != is_done:
                    task["status"] = "completed" if checked else "pending"
                    save_data(st.session_state.tasks)
                    st.rerun()

                with c2:
                    t_title = f"~~{task['title']}~~" if is_done else f"**{task['title']}**"
                    st.markdown(t_title)
                    if task.get("description"):
                        st.caption(task["description"])

                with c3:
                    p = task.get("priority", "medium")
                    p_badge = "🔴 Cao" if p == "high" else ("🟡 Trung bình" if p == "medium" else "🟢 Thấp")
                    due = task.get("dueDate", "")
                    st.write(f"{p_badge} | 📅 {due if due else 'Không có hạn'}")
                    if st.button("🗑️ Xóa", key=f"del_{task['id']}"):
                        st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                        save_data(st.session_state.tasks)
                        st.rerun()
                st.divider()

# ==========================================
# TAB 2: BÁO CÁO KPI & ANALYTICS DASHBOARD
# ==========================================
with tab_kpi:
    tasks_kpi = st.session_state.tasks
    tot = len(tasks_kpi) or 1
    comp = len([t for t in tasks_kpi if t["status"] == "completed"])
    over = len([t for t in tasks_kpi if t["status"] == "pending" and t.get("dueDate") and t["dueDate"] < today_str])
    
    comp_rate = round((comp / tot) * 100)
    ontime_rate = round(((comp - over) / comp) * 100) if comp > 0 else 100
    ontime_rate = max(0, ontime_rate)
    
    kpi_score = round((comp_rate * 0.7) + (ontime_rate * 0.3)) if len(tasks_kpi) > 0 else 0
    kpi_eval = "🌟 XUẤT SẮC" if kpi_score >= 80 else ("🔥 TỐT" if kpi_score >= 50 else "⚡ CẦN CỐ GẮNG")

    # Banner Header KPI
    st.markdown(f"""
        <div class="kpi-score-banner">
            <h2 style="margin: 0; font-size: 1.8rem;">🎯 Chỉ Số Năng Suất KPI Cá Nhân: <span style="color: #6366f1;">{kpi_score}%</span> ({kpi_eval})</h2>
            <p style="margin-top: 0.5rem; color: #94a3b8;">Đánh giá dựa trên tỷ lệ hoàn thành công việc ({comp_rate}%) và tỷ lệ hoàn thành đúng hạn ({ontime_rate}%).</p>
        </div>
    """, unsafe_allow_html=True)

    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("Chỉ Số Hoàn Thành", f"{comp_rate}%", f"{comp}/{tot} việc đã xong")
    kc2.metric("Tỷ Lệ Đúng Hạn", f"{ontime_rate}%", f"{over} việc trễ hạn", delta_color="inverse")
    
    high_tasks = len([t for t in tasks_kpi if t.get("priority") == "high"])
    med_tasks = len([t for t in tasks_kpi if t.get("priority") == "medium"])
    low_tasks = len([t for t in tasks_kpi if t.get("priority") == "low"])
    
    kc3.metric("Việc Khẩn Cấp (Cao)", high_tasks)
    kc4.metric("Việc Quá Hạn Cần Xử Lý", over, delta_color="inverse")

    st.divider()

    # Visual Charts with Streamlit Progress & Bar Charts
    ch1, ch2 = st.columns(2)
    with ch1:
        st.subheader("🔥 Phân Phối Mức Độ Ưu Tiên (Priority)")
        chart_data_p = {
            "🔴 Ưu tiên Cao": high_tasks,
            "🟡 Ưu tiên Trung bình": med_tasks,
            "🟢 Ưu tiên Thấp": low_tasks
        }
        st.bar_chart(chart_data_p)

    with ch2:
        st.subheader("📈 Trạng Thái Công Việc (Status Breakdown)")
        chart_data_s = {
            "⚡ Đang làm": tot - comp,
            "✅ Hoàn thành": comp,
            "🚨 Quá hạn": over
        }
        st.bar_chart(chart_data_s)

# --- Sidebar Controls ---
with st.sidebar:
    st.header("➕ Thêm Công Việc Mới")
    with st.form("sidebar_add_form", clear_on_submit=True):
        n_title = st.text_input("Tên công việc *")
        n_desc = st.text_area("Ghi chú mô tả")
        n_prio = st.selectbox("Độ ưu tiên KPI", ["low", "medium", "high"], 
                             format_func=lambda x: "🔴 Cao" if x == "high" else ("🟡 Trung bình" if x == "medium" else "🟢 Thấp"))
        n_date = st.date_input("Hạn chót (Deadline)", value=date.today())
        
        if st.form_submit_button("💾 Lưu công việc", use_container_width=True):
            if n_title.strip():
                new_t = {
                    "id": f"task_{int(datetime.now().timestamp()*1000)}",
                    "title": n_title.strip(),
                    "description": n_desc.strip(),
                    "priority": n_prio,
                    "status": "pending",
                    "dueDate": n_date.strftime("%Y-%m-%d"),
                    "createdAt": datetime.now().isoformat()
                }
                st.session_state.tasks.insert(0, new_t)
                save_data(st.session_state.tasks)
                st.success("Đã thêm công việc mới!")
                st.rerun()

    st.divider()
    st.header("⚙️ Sao Lưu Dữ Liệu JSON")
    st.download_button(
        label="📥 Export File Backup JSON",
        data=json.dumps(st.session_state.tasks, ensure_ascii=False, indent=2),
        file_name=f"taskflow_kpi_backup_{today_str}.json",
        mime="application/json",
        use_container_width=True
    )
