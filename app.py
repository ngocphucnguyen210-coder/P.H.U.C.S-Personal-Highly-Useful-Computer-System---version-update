import streamlit as st
import datetime
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64

# Import thư viện Groq chính hãng
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

# Cấu hình trang web Streamlit
st.set_page_config(
    page_title="P.H.U.C.S - Personal Highly Useful Computer System",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API KEY CỦA GIA PHÚC
GROQ_API_KEY_DEFAULT = "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"

# --- KHỞI TẠO SESSION STATE (QUẢN LÝ TRẠNG THÁI DỮ LIỆU THỰC TẾ) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Nguyễn Gia Phúc"
if 'user_id' not in st.session_state:
    st.session_state.user_id = "PHUCS-VN-2026-8888"

# Quản lý Trạng thái Đồng hồ bấm giờ
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 0
if 'study_logs' not in st.session_state:
    st.session_state.study_logs = []

# Quản lý Chat & Dữ liệu
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào Nguyễn Gia Phúc! Mình là P.H.U.C.S - Trợ lý AI cao cấp chạy bằng Groq Cloud siêu tốc. Hôm nay chúng ta sẽ cùng chinh phục môn học nào đây? ✨"}
    ]
if 'todos' not in st.session_state:
    st.session_state.todos = [
        {"task": "Ôn tập Toán hàm số & Đạo hàm", "done": True, "date": "17/10/2026"},
        {"task": "Soạn văn tác phẩm Vợ Nhặt - Kim Lân", "done": False, "date": "17/10/2026"}
    ]
if 'events' not in st.session_state:
    st.session_state.events = [{"name": "Thi giữa kỳ môn Vật lí", "category": "Thi cử", "date": str(datetime.date.today())}]
if 'notes_list' not in st.session_state:
    st.session_state.notes_list = []
if 'group_messages' not in st.session_state:
    st.session_state.group_messages = [{"sender": "Gia Phúc", "text": "Chào cả nhóm ôn thi nhé!"}]

# --- THAY ĐỔI HÌNH NỀN THỰC TẾ (FIX LỖI HÌNH NỀN) ---
bg_css = ""
if 'bg_choice' not in st.session_state:
    st.session_state.bg_choice = "Hồng mộng mơ (Tĩnh)"

# Xử lý CSS Background động
if st.session_state.bg_choice == "Hồng mộng mơ (Tĩnh)":
    bg_css = "background-color: #FFF0F5;"
elif st.session_state.bg_choice == "Dark Mode Hồng đêm (Tĩnh)":
    bg_css = "background-color: #2D1B24; color: #FFC0CB;"
elif st.session_state.bg_choice == "Dải ngân hà hồng (Động)":
    bg_css = "background: linear-gradient(-45deg, #ff9a9e, #fecfef, #a1c4fd, #c2e9fb); background-size: 400% 400%; animation: gradient 15s ease infinite;"
elif st.session_state.bg_choice == "Sóng biển hồng (Động)":
    bg_css = "background: linear-gradient(135deg, #fff0f5 0%, #ffd1dc 50%, #ffb6c1 100%);"

st.markdown(f"""
<style>
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    .stApp {{
        {bg_css}
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    section[data-testid="stSidebar"] {{
        background-color: #FFE4E1 !important;
        border-right: 1px solid #FFB6C1;
    }}
    .main-title {{
        color: #D87093;
        font-weight: 800;
        text-align: center;
        font-size: 2.5rem;
    }}
    .slogan {{
        color: #C71585;
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }}
    .login-container {{
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(219, 112, 147, 0.2);
        max-width: 500px;
        margin: 50px auto;
        text-align: center;
        border: 2px solid #FFC0CB;
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #FF69B4 0%, #DB7093 100%);
        color: white;
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: bold;
        border: none;
    }}
    .user-card {{
        background: rgba(255, 255, 255, 0.8);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #FFB6C1;
        margin-bottom: 15px;
    }}
    .timer-display {{
        font-size: 3.5rem;
        font-weight: bold;
        color: #D87093;
        text-align: center;
        background: white;
        padding: 20px;
        border-radius: 20px;
        border: 3px solid #FFB6C1;
        margin: 20px 0;
    }}
</style>
""", unsafe_allow_html=True)

# --- TRANG ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="login-container">
            <h1 style="color: #D87093; font-size: 3rem; margin-bottom: 0;">🌸 P.H.U.C.S 🌸</h1>
            <p style="color: #DB7093; font-weight: 600; font-size: 1.1rem;">Personal Highly Useful Computer System</p>
            <p class="slogan">"Đồng hành cùng P.H.U.C.S, vững bước thành công"</p>
            <hr style="border-color: #FFC0CB;">
            <h3 style="color: #6B4226; font-size: 1.2rem; margin-top: 20px;">Vui lòng chọn phương thức đăng nhập:</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("👤 Khách (Guest)"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Khách Danh Dự"
            st.rerun()
    with col2:
        if st.button("🌐 Gmail"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (Gmail)"
            st.rerun()
    with col3:
        if st.button("📘 Facebook"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (FB)"
            st.rerun()
    with col4:
        if st.button("🍏 iCloud"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (iCloud)"
            st.rerun()

else:
    # --- THANH SIDEBAR ---
    with st.sidebar:
        st.markdown(f"""
            <div class="user-card">
                <h3 style="color: #C71585; margin: 0;">🌸 {st.session_state.user_name}</h3>
                <p style="color: #666; font-size: 0.85rem; margin: 5px 0;">ID: <code>{st.session_state.user_id}</code></p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Đăng xuất"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.divider()
        
        # FIX CÀI ĐẶT HÌNH NỀN HOẠT ĐỘNG THẬT
        st.subheader("🎨 Giao diện & Hình nền")
        selected_bg = st.selectbox(
            "Chọn hình nền sẵn có", 
            ["Hồng mộng mơ (Tĩnh)", "Dải ngân hà hồng (Động)", "Sóng biển hồng (Động)", "Dark Mode Hồng đêm (Tĩnh)"],
            index=["Hồng mộng mơ (Tĩnh)", "Dải ngân hà hồng (Động)", "Sóng biển hồng (Động)", "Dark Mode Hồng đêm (Tĩnh)"].index(st.session_state.bg_choice)
        )
        if selected_bg != st.session_state.bg_choice:
            st.session_state.bg_choice = selected_bg
            st.rerun()
            
        uploaded_bg = st.file_uploader("Tải ảnh nền từ máy lên", type=["png", "jpg", "jpeg"])
        if uploaded_bg is not None:
            bytes_data = uploaded_bg.getvalue()
            b64_img = base64.b64encode(bytes_data).decode()
            st.markdown(f"""
                <style>
                .stApp {{
                    background-image: url("data:image/png;base64,{b64_img}");
                    background-size: cover;
                    background-attachment: fixed;
                }}
                </style>
            """, unsafe_allow_html=True)

        st.divider()
        
        # CÀI ĐẶT GROQ API
        with st.expander("⚙️ Cài đặt Groq API (Đã kích hoạt)"):
            groq_api_key = st.text_input("Groq API Key:", value=GROQ_API_KEY_DEFAULT, type="password")
            groq_model = st.selectbox("Model Groq AI:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
            st.success("🟢 Groq API Key đã sẵn sàng!")

    # --- MÀN HÌNH CHÍNH & CÁC TAB ---
    st.markdown('<h1 class="main-title">🌸 P.H.U.C.S - AI STUDY ASSISTANT 🌸</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Đồng hành cùng P.H.U.C.S, vững bước thành công"</p>', unsafe_allow_html=True)
    
    tab_chat, tab_clock, tab_calendar, tab_todo, tab_chatgroup, tab_notes, tab_charts, tab_games = st.tabs([
        "💬 Trợ lý AI (Groq)", 
        "⏱️ Đồng hồ bấm giờ", 
        "📅 Lịch & Sự kiện", 
        "📝 To-Do List", 
        "👥 Nhóm chat", 
        "📓 Note & Vẽ", 
        "📊 Biểu đồ", 
        "🎮 Trò chơi (30+)"
    ])
    
    # ---------------- TAB 1: TRỢ LÝ AI TRẢ LỜI THẬT (FIX LỖI AI KHÔNG TRẢ LỜI) ----------------
    with tab_chat:
        st.markdown("### 🤖 Trò chuyện cùng P.H.U.C.S AI")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar="🌸" if msg["role"]=="assistant" else "👤"):
                st.markdown(msg["content"])
                
        user_prompt = st.chat_input("Nhập câu hỏi học tập của bạn cho P.H.U.C.S...")
        
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant", avatar="🌸"):
                with st.spinner("P.H.U.C.S đang suy luận câu trả lời..."):
                    ai_reply = ""
                    if HAS_GROQ and groq_api_key:
                        try:
                            client = Groq(api_key=groq_api_key)
                            messages_payload = [
                                {"role": "system", "content": "Bạn là P.H.U.C.S, trợ lý AI hỗ trợ học tập xịn, sang, cao cấp, luôn trả lời chính xác, chi tiết và lịch sự cho bạn Nguyễn Gia Phúc."}
                            ]
                            for h in st.session_state.chat_history:
                                messages_payload.append({"role": h["role"], "content": h["content"]})
                                
                            response = client.chat.completions.create(
                                model=groq_model,
                                messages=messages_payload,
                                temperature=0.6,
                                max_tokens=2048
                            )
                            ai_reply = response.choices[0].message.content
                        except Exception as e:
                            ai_reply = f"⚠️ Lỗi kết nối Groq API: {e}"
                    else:
                        ai_reply = "Vui lòng kiểm tra thư viện Groq trên hệ thống!"
                        
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    # ---------------- TAB 2: ĐỒNG HỒ BẤM GIỜ CHẠY THẬT (FIX LỖI ĐỒNG HỒ) ----------------
    with tab_clock:
        st.markdown("### ⏱️ Đồng hồ bấm giờ học tập (Đếm giờ thời gian thực)")
        
        subj = st.selectbox("Chọn môn học:", ["Toán học", "Ngữ Văn", "Vật lí", "Tiếng Anh", "Hóa học", "Lịch Sử", "Địa Lí"])
        
        # Định dạng HH:MM:SS
        m, s = divmod(st.session_state.timer_seconds, 60)
        h, m = divmod(m, 60)
        time_str = f"{h:02d}:{m:02d}:{s:02d}"
        
        timer_placeholder = st.empty()
        timer_placeholder.markdown(f'<div class="timer-display">{time_str}</div>', unsafe_allow_html=True)
        
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            if st.button("▶️ Bắt đầu"):
                st.session_state.timer_running = True
        with col_b2:
            if st.button("⏸️ Tạm dừng"):
                st.session_state.timer_running = False
        with col_b3:
            if st.button("🔄 Đặt lại"):
                st.session_state.timer_running = False
                st.session_state.timer_seconds = 0
                st.rerun()
        with col_b4:
            if st.button("💾 Lưu lịch sử"):
                st.session_state.study_logs.append({"subject": subj, "time": time_str, "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")})
                st.success(f"Đã lưu thành công: {time_str} môn {subj}!")

        # Vòng lặp đếm giờ nhảy thực tế từng giây
        if st.session_state.timer_running:
            time.sleep(1)
            st.session_state.timer_seconds += 1
            st.rerun()

        if st.session_state.study_logs:
            st.markdown("#### 📜 Lịch sử thời gian đã lưu:")
            for log in st.session_state.study_logs:
                st.write(f"📖 Môn: **{log['subject']}** | ⏱️ Thời gian: `{log['time']}` | 🗓️ Ngày lưu: {log['date']}")

    # ---------------- TAB 3: LỊCH & SỰ KIỆN THỰC TẾ ----------------
    with tab_calendar:
        st.markdown("### 📅 Quản lý Lịch & Sự kiện")
        
        with st.form("add_event_form"):
            e_name = st.text_input("Tên sự kiện new:")
            e_cat = st.selectbox("Phân loại:", ["Thi cử", "Sinh nhật", "Kỷ niệm", "Quan trọng", "Khác"])
            e_date = st.date_input("Ngày diễn ra:", datetime.date.today())
            if st.form_submit_button("Thêm sự kiện") and e_name:
                st.session_state.events.append({"name": e_name, "category": e_cat, "date": str(e_date)})
                st.success("Đã lưu sự kiện!")
                st.rerun()
                
        st.markdown("#### 📌 Danh sách sự kiện đã tạo:")
        for idx, ev in enumerate(st.session_state.events):
            cols = st.columns([4, 1])
            cols[0].write(f"🗓️ **{ev['name']}** [{ev['category']}] - Ngày: `{ev['date']}`")
            if cols[1].button("Xóa", key=f"del_ev_{idx}"):
                st.session_state.events.pop(idx)
                st.rerun()

    # ---------------- TAB 4: TO-DO LIST HOẠT ĐỘNG THẬT ----------------
    with tab_todo:
        st.markdown("### 📝 Danh sách To-Do List")
        
        new_task = st.text_input("Thêm nhiệm vụ mới...")
        if st.button("➕ Thêm nhiệm vụ") and new_task:
            st.session_state.todos.append({"task": new_task, "done": False, "date": datetime.datetime.now().strftime("%d/%m/%Y")})
            st.rerun()
            
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### ⏳ Chưa xong")
            for idx, item in enumerate(st.session_state.todos):
                if not item["done"]:
                    sc = st.columns([3, 1])
                    sc[0].write(f"❌ {item['task']}")
                    if sc[1].button("Hoàn thành", key=f"td_done_{idx}"):
                        st.session_state.todos[idx]["done"] = True
                        st.rerun()
        with col_t2:
            st.markdown("#### ✅ Đã xong")
            for item in st.session_state.todos:
                if
