import streamlit as st
import pandas as pd
import json
import io
import re
import urllib.request
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Real Estate Lead Scoring & Human-In-The-Loop",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .kpi-banner {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .tier-vip {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .tier-mid {
        background-color: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
    }
    .tier-junk {
        background-color: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sample Dataset Generator ---
SAMPLE_LEADS = [
    {
        "ID": "LD-101",
        "Họ và Tên": "Nguyễn Văn Hùng",
        "Số Điện Thoại": "0988123456",
        "Email": "hung.nguyen@corp.vn",
        "Ngân Sách Dự Kiến": "35 tỷ",
        "Mô Tả Nhu Cầu": "Tôi là chủ doanh nghiệp cần mua Biệt thự đơn lập ven sông tại Vinhomes Ocean Park hoặc Phú Mỹ Hưng, tài chính mạnh không thành vấn đề. Yêu cầu pháp lý chuẩn 100%, có sổ hồng riêng và muốn gặp trực tiếp chủ đầu tư để đàm phán.",
        "Khu Vực": "Quận 1 / Phú Mỹ Hưng"
    },
    {
        "ID": "LD-102",
        "Họ và Tên": "Trần Thị Mai",
        "Số Điện Thoại": "0912987654",
        "Email": "mai.tran@gmail.com",
        "Ngân Sách Dự Kiến": "5 tỷ",
        "Mô Tả Nhu Cầu": "Cần tìm mua căn hộ chung cư 2 phòng ngủ tầm 4-5 tỷ khu vực Quận 7, đang cân nhắc chính sách hỗ trợ vay ngân hàng 70%. Nhu cầu thực cần tư vấn thêm vị trí.",
        "Khu Vực": "Quận 7"
    },
    {
        "ID": "LD-103",
        "Họ và Tên": "Lê Hoàng Nam",
        "Số Điện Thoại": "0903111222",
        "Email": "nam.investor@gmail.com",
        "Ngân Sách Dự Kiến": "80 tỷ",
        "Mô Tả Nhu Cầu": "Nhà đầu tư chuyên nghiệp tìm mua Penthouse Quận 1 hoặc Shophouse mặt đường lớn để mở chuỗi. Đã sẵn sàng dòng tiền mua sỉ số lượng lớn.",
        "Khu Vực": "Quận 1"
    },
    {
        "ID": "LD-104",
        "Họ và Tên": "Phạm Văn Tèo",
        "Số Điện Thoại": "0977000111",
        "Email": "teo@yahoo.com",
        "Ngân Sách Dự Kiến": "1.5 tỷ",
        "Mô Tả Nhu Cầu": "Cần mua biệt thự sân vườn hồ bơi tại trung tâm Quận 1 giá 1-2 tỷ. Hỏi giá cho vui chứ chưa có ý định mua.",
        "Khu Vực": "Quận 1"
    },
    {
        "ID": "LD-105",
        "Họ và Tên": "Đỗ Minh Tuấn",
        "Số Điện Thoại": "0934555666",
        "Email": "tuan.insurance@service.com",
        "Ngân Sách Dự Kiến": "Không rõ",
        "Mô Tả Nhu Cầu": "Chào anh chị, bên em chuyên cung cấp gói bảo hiểm nhân thọ và dịch vụ vay vốn hỗ trợ tài chính lãi suất thấp.",
        "Khu Vực": "Toàn quốc"
    },
    {
        "ID": "LD-106",
        "Họ và Tên": "Vũ Anh Khoa",
        "Số Điện Thoại": "0918000999",
        "Email": "khoa.vu@tech.vn",
        "Ngân Sách Dự Kiến": "50 tỷ",
        "Mô Tả Nhu Cầu": "Tìm mua quỹ đất công nghiệp hoặc sàn văn phòng diện tích lớn trên 1000m2 tại TP.HCM. Tài chính mạnh, gặp đàm phán ngay.",
        "Khu Vực": "TP.HCM"
    },
    {
        "ID": "LD-107",
        "Họ và Tên": "Lương Quốc Bảo",
        "Số Điện Thoại": "Thuê bao",
        "Email": "bao@unknown.com",
        "Ngân Sách Dự Kiến": "Không có nhu cầu",
        "Mô Tả Nhu Cầu": "Báo nhầm số, không có nhu cầu mua bất động sản, dữ liệu cũ. Gọi nhiều lần không bắt máy.",
        "Khu Vực": "Không xác định"
    }
]

# --- AI Lead Scoring Rule Engine ---
def evaluate_lead_ai(row):
    desc = str(row.get("Mô Tả Nhu Cầu", ""))
    budget = str(row.get("Ngân Sách Dự Kiến", ""))
    phone = str(row.get("Số Điện Thoại", ""))
    text = (desc + " " + budget + " " + phone).lower()
    
    score = 50
    reasons = []
    vip_hits = []
    junk_hits = []

    # 1. TIÊU CHÍ CỘNG 50 ĐIỂM (VIP)
    # Ngân sách lớn
    has_big_budget = any(k in text for k in ["20 tỷ", "30 tỷ", "35 tỷ", "50 tỷ", "80 tỷ", "100 tỷ", "tài chính mạnh", "không thành vấn đề"])
    # Loại hình cao cấp
    has_high_end = any(k in text for k in ["biệt thự đơn lập", "penthouse", "shophouse mặt đường", "quỹ đất công nghiệp", "sàn văn phòng"])
    # Vị trí đắc địa
    has_prime_loc = any(k in text for k in ["quận 1", "ven sông", "ocean park", "phú mỹ hưng"])
    # Đối tượng khách
    has_vip_client = any(k in text for k in ["chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "số lượng lớn"])
    # Cấp thiết & Minh bạch
    has_urgent = any(k in text for k in ["pháp lý chuẩn", "sổ hồng riêng", "gặp trực tiếp chủ đầu tư", "đàm phán"])

    if has_big_budget: vip_hits.append("Ngân sách lớn (≥20 tỷ / Tài chính mạnh)")
    if has_high_end: vip_hits.append("Loại hình cao cấp (Biệt thự/Penthouse/Shophouse/Đất CN)")
    if has_prime_loc: vip_hits.append("Vị trí đắc địa (Quận 1/Ven sông/Ocean Park/Phú Mỹ Hưng)")
    if has_vip_client: vip_hits.append("Đối tượng VIP (Chủ DN/NĐT chuyên nghiệp/Mua sỉ)")
    if has_urgent: vip_hits.append("Nhu cầu cấp thiết & Minh bạch (Pháp lý/Sổ hồng/Gặp CĐT)")

    if vip_hits:
        score += 50
        reasons.append(f"🟢 +50 ĐIỂM (VIP): {'; '.join(vip_hits)}")

    # 2. TIÊU CHÍ TRỪ 50 ĐIỂM (RÁC / SPAM)
    has_unrealistic = any(k in text for k in ["giá 1 tỷ", "giá 2 tỷ", "giá 1-2 tỷ", "giá vài trăm", "quận 1 giá 1-2 tỷ", "nhà quận 1 giá 1-2 tỷ"]) and ("quận 1" in text or "trung tâm" in text)
    has_no_demand = any(k in text for k in ["nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành", "báo nhầm"])
    has_uncooperative = any(k in text for k in ["hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác"])
    has_spam = any(k in text for k in ["bảo hiểm", "vay vốn", "mời chào dịch vụ", "quảng cáo"])
    has_bad_contact = any(k in text for k in ["thuê bao", "không bắt máy", "không phản hồi zalo"])

    if has_unrealistic: junk_hits.append("Yêu cầu phi thực tế (Giá quá thấp so với thị trường)")
    if has_no_demand: junk_hits.append("Không có nhu cầu / Nhầm số / Dữ liệu cũ")
    if has_uncooperative: junk_hits.append("Không thiện chí / Hỏi giá cho vui")
    if has_spam: junk_hits.append("Spam / Quảng cáo dịch vụ khác (Bảo hiểm/Vay vốn)")
    if has_bad_contact: junk_hits.append("Thông tin liên lạc lỗi / Thuê bao / Không phản hồi")

    if junk_hits:
        score -= 50
        reasons.append(f"🔴 -50 ĐIỂM (RÁC/SPAM): {'; '.join(junk_hits)}")

    # 3. CÁC TRƯỜNG HỢP KHÁC
    if not vip_hits and not junk_hits:
        has_mid = any(k in text for k in ["chung cư", "nhà phố", "3 tỷ", "4 tỷ", "5 tỷ", "7 tỷ", "10 tỷ", "tầm trung"])
        has_bank = any(k in text for k in ["vay ngân hàng", "cân nhắc chính sách"])
        has_consult = any(k in text for k in ["tư vấn thêm", "hỏi vị trí", "pháp lý"])
        
        mid_hits = []
        if has_mid: mid_hits.append("Phân khúc tầm trung (3-10 tỷ)")
        if has_bank: mid_hits.append("Cần hỗ trợ vay ngân hàng")
        if has_consult: mid_hits.append("Nhu cầu thực, cần tư vấn thêm")

        if mid_hits:
            score += 10
            reasons.append(f"🟡 +10 ĐIỂM (Tiềm năng trung bình): {'; '.join(mid_hits)}")
        else:
            reasons.append("⚪ 0 ĐIỂM: Khách hàng nhu cầu tiêu chuẩn")

    final_score = max(0, min(100, score))
    
    if final_score >= 80:
        tier = "🔥 VIP / Siêu Tiềm Năng"
        rec_action = "Ưu tiên Salesman VIP chốt đàm phán"
    elif final_score >= 40:
        tier = "⚡ Nhu Cầu Thực / Trung Bình"
        rec_action = "Chăm sóc theo quy trình chuẩn"
    else:
        tier = "🗑️ Khách Rác / Spam"
        rec_action = "Loại bỏ / Không tốn tài nguyên"

    return {
        "Điểm AI": final_score,
        "Phân Loại AI": tier,
        "Đề Xuất AI": rec_action,
        "Giải Trình AI Chi Tiết": " | ".join(reasons)
    }

# --- Main App Header ---
st.title("🏠 AI Lead Scoring System — Ngành Bất Động Sản")
st.caption("Quy trình tự động hóa phân tích Lead từ Google Sheets, Chấm điểm AI & Kiểm duyệt Human-In-The-Loop")

# --- Sidebar: Data Import Source ---
st.sidebar.header("📥 1. Nguồn Dữ Liệu Khách Hàng")
source_option = st.sidebar.radio(
    "Chọn nguồn lấy dữ liệu:",
    ["📊 Google Sheets Link", "📁 Upload File Excel/CSV", "✨ Dữ Liệu Mẫu Chuẩn BĐS"]
)

raw_df = None

if source_option == "📊 Google Sheets Link":
    sheet_url = st.sidebar.text_input(
        "Nhập Link Google Sheets:",
        value="https://docs.google.com/spreadsheets/d/1gkm1GqupYAvEfqZ2U5iT5HF2F6crWOVDwakNbWNFSwo/edit?gid=1542775777#gid=1542775777"
    )
    if st.sidebar.button("🚀 Tải dữ liệu từ Google Sheets"):
        try:
            # Convert edit URL to export CSV URL
            match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
            gid_match = re.search(r"gid=([0-9]+)", sheet_url)
            if match:
                doc_id = match.group(1)
                gid = gid_match.group(1) if gid_match else "0"
                csv_url = f"https://docs.google.com/spreadsheets/d/{doc_id}/export?format=csv&gid={gid}"
                
                req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
                content = urllib.request.urlopen(req).read().decode('utf-8')
                raw_df = pd.read_csv(io.StringIO(content))
                st.sidebar.success("Tải dữ liệu từ Google Sheets thành công!")
            else:
                st.sidebar.error("Link Google Sheets không hợp lệ!")
        except Exception as e:
            st.sidebar.warning("Không thể truy cập trực tiếp Google Sheets công khai do quyền riêng tư. Đang chuyển sang chế độ tải dữ liệu mẫu chuẩn.")
            raw_df = pd.DataFrame(SAMPLE_LEADS)

elif source_option == "📁 Upload File Excel/CSV":
    uploaded_file = st.sidebar.file_uploader("Tải lên file Excel (.xlsx) hoặc CSV", type=["xlsx", "csv"])
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                raw_df = pd.read_csv(uploaded_file)
            else:
                raw_df = pd.read_excel(uploaded_file)
            st.sidebar.success("Tải file thành công!")
        except Exception as e:
            st.sidebar.error(f"Lỗi đọc file: {e}")

else:
    raw_df = pd.DataFrame(SAMPLE_LEADS)

# If no df yet, default to sample dataset
if raw_df is None:
    raw_df = pd.DataFrame(SAMPLE_LEADS)

# --- Session State Initialization for Human-In-The-Loop Data ---
if "processed_df" not in st.session_state or st.sidebar.button("🔄 Chạy AI Chấm Điểm Lại"):
    # Run AI Scoring
    ai_results = [evaluate_lead_ai(row) for _, row in raw_df.iterrows()]
    ai_df = pd.DataFrame(ai_results)
    
    # Merge Raw Data with AI Results
    merged_df = pd.concat([raw_df.reset_index(drop=True), ai_df.reset_index(drop=True)], axis=1)
    
    # Add Human-in-the-loop audit fields if not present
    merged_df["Trạng Thái Duyệt (Human)"] = merged_df["Đề Xuất AI"]
    merged_df["Ghi Chú Kiểm Duyệt"] = "Chưa chỉnh sửa"
    merged_df["Xác Nhận Chốt"] = True
    
    st.session_state.processed_df = merged_df

df = st.session_state.processed_df

# --- Executive KPI Summary Cards ---
st.markdown("""
    <div class="kpi-banner">
        <h3>📊 Thống Kê Tổng Quan Phân Loại Khách Hàng Tiềm Năng</h3>
    </div>
""", unsafe_allow_html=True)

total_leads = len(df)
vip_count = len(df[df["Phân Loại AI"].str.contains("VIP", na=False)])
mid_count = len(df[df["Phân Loại AI"].str.contains("Trung Bình", na=False)])
junk_count = len(df[df["Phân Loại AI"].str.contains("Rác", na=False)])

m1, m2, m3, m4 = st.columns(4)
m1.metric("Tổng Số Leads", total_leads)
m2.metric("🔥 Khách VIP (+50 đ)", vip_count, f"{round(vip_count/total_leads*100)}%")
m3.metric("⚡ Khách Trung Bình (+10 đ)", mid_count, f"{round(mid_count/total_leads*100)}%")
m4.metric("🗑️ Khách Rác / Spam (-50 đ)", junk_count, f"{round(junk_count/total_leads*100)}%", delta_color="inverse")

st.divider()

# --- Section 2: Human-In-The-Loop Review Workspace ---
st.header("👤 2. Giao Diện Kiểm Duyệt Human-In-The-Loop (Phê Duyệt Kết Quả)")
st.info("💡 Con người có thể xem giải trình AI, điều chỉnh trạng thái chốt khách hàng và thêm ghi chú trước khi xuất báo cáo Excel bàn giao.")

# Filter Tabs
st.subheader("Filter danh sách theo phân loại:")
selected_tab = st.radio("Bộ lọc danh sách:", ["Tất cả Leads", "🔥 Khách VIP / Siêu Tiềm Năng", "⚡ Nhu Cầu Thực / Trung Bình", "🗑️ Khách Rác / Spam"], horizontal=True)

display_df = df.copy()
if "VIP" in selected_tab:
    display_df = display_df[display_df["Phân Loại AI"].str.contains("VIP", na=False)]
elif "Trung Bình" in selected_tab:
    display_df = display_df[display_df["Phân Loại AI"].str.contains("Trung Bình", na=False)]
elif "Rác" in selected_tab:
    display_df = display_df[display_df["Phân Loại AI"].str.contains("Rác", na=False)]

# Interactive Data Editor for Human-in-the-loop
edited_df = st.data_editor(
    display_df,
    column_config={
        "Xác Nhận Chốt": st.column_config.CheckboxColumn(
            "Xác Nhận",
            help="Tích chọn để chốt kết quả bàn giao",
            default=True,
        ),
        "Trạng Thái Duyệt (Human)": st.column_config.SelectboxColumn(
            "Trạng Thái Duyệt (Human-in-the-loop)",
            help="Con người ghi đè trạng thái của AI nếu cần",
            options=[
                "Ưu tiên Salesman VIP chốt đàm phán",
                "Chăm sóc theo quy trình chuẩn",
                "Cần tìm hiểu thêm thông tin",
                "Loại bỏ / Không tốn tài nguyên"
            ],
            required=True,
        ),
        "Điểm AI": st.column_config.NumberColumn(
            "Điểm AI",
            format="%d đ",
        ),
    },
    disabled=["Họ và Tên", "Số Điện Thoại", "Mô Tả Nhu Cầu", "Điểm AI", "Phân Loại AI", "Giải Trình AI Chi Tiết"],
    hide_index=True,
    use_container_width=True,
    num_rows="fixed"
)

# Update state with edited values
st.session_state.processed_df.update(edited_df)

st.divider()

# --- Section 3: Export to Excel (.xlsx) ---
st.header("📤 3. Xuất Báo Cáo File Excel Bàn Giao (.xlsx)")

# Create formatted Excel file in memory
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Sheet 1: Dữ liệu đã phê duyệt
    export_df = st.session_state.processed_df.copy()
    export_df.to_excel(writer, sheet_name='Danh_Sach_Leads_Da_Duyet', index=False)
    
    # Sheet 2: Thống kê KPI
    summary_data = {
        "Chỉ Số KPI": ["Tổng số Leads", "Khách VIP (≥80đ)", "Khách Trung Bình (40-79đ)", "Khách Rác (<40đ)", "Tỷ lệ VIP", "Ngày xuất báo cáo"],
        "Giá Trị": [total_leads, vip_count, mid_count, junk_count, f"{round(vip_count/total_leads*100)}%", datetime.now().strftime("%Y-%m-%d %H:%M")]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Thong_Ke_KPI', index=False)

buffer.seek(0)

st.download_button(
    label="📊 Tải Về Báo Cáo Excel Đã Kiểm Duyệt (.xlsx)",
    data=buffer,
    file_name=f"Bao_Cao_Cham_Diem_Leads_BDS_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=True
)

st.success("✅ Quy trình hoàn tất! Bạn có thể xem chi tiết từng Lead hoặc tải về file Excel bàn giao ngay lập tức.")
