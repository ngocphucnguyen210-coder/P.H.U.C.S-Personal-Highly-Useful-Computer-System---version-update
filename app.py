import streamlit as st
import datetime
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# --- CSS TÙY CHỈNH GIAO DIỆN HỒNG PASTEL CAO CẤP ---
st.markdown("""
<style>
    .stApp {
        background-color: #FFF0F5;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFE4E1;
        border-right: 1px solid #FFB6C1;
    }
    .main-title {
        color: #D87093;
        font-weight: 800;
        text-align: center;
        font-size: 2.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .slogan {
        color: #C71585;
        text-align: center;
        font-style: italic;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .login-container {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(219, 112, 147, 0.2);
        max-width: 500px;
        margin: 50px auto;
        text-align: center;
        border: 2px solid #FFC0CB;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF69B4 0%, #DB7093 100%);
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FF1493 0%, #C71585 100%);
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.6);
        transform: translateY(-2px);
    }
    .user-card {
        background: rgba(255, 255, 255, 0.7);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #FFB6C1;
        margin-bottom: 15px;
    }
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FF69B4;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Nguyễn Gia Phúc"
if 'user_id' not in st.session_state:
    st.session_state.user_id = "PHUCS-VN-2026-8888"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào Nguyễn Gia Phúc! Mình là P.H.U.C.S - Trợ lý AI cao cấp đã kết nối thành công với Groq Cloud siêu tốc. Hôm nay chúng ta sẽ cùng chinh phục những đỉnh cao kiến thức nào đây? ✨"}
    ]
if 'notes_list' not in st.session_state:
    st.session_state.notes_list = []
if 'todos' not in st.session_state:
    st.session_state.todos = [{"task": "Ôn tập Toán hàm số & Đạo hàm", "done": True, "date": "17/10/2026"}, {"task": "Soạn văn tác phẩm Kim Lân", "done": False, "date": "17/10/2026"}]
if 'events' not in st.session_state:
    st.session_state.events = []
if 'chats_db' not in st.session_state:
    st.session_state.chats_db = [{"id": 1, "title": "Hỏi đáp kiến thức Toán & Lý", "messages": []}]

# --- TRANG ĐĂNG NHẬP ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="login-container">
            <h1 style="color: #D87093; font-size: 3rem; margin-bottom: 0;">🌸 P.H.U.C.S 🌸</h1>
            <p style="color: #DB7093; font-weight: 600; font-size: 1.1rem;">Personal Highly Useful Computer System</p>
            <p class="slogan">"Đồng hành cùng P.H.U.C.S, vững bước thành công"</p>
            <hr style="border-color: #FFC0CB;">
            <h3 style="color: #6B4226; font-size: 1.2rem; margin-top: 20px;">Vui lòng chọn phương thức đăng nhập để tiếp tục:</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("👤 Khách (Guest)"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Khách Danh Dự"
            st.rerun()
    with col2:
        if st.button("🌐 Đăng nhập Gmail"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (Gmail)"
            st.rerun()
    with col3:
        if st.button("📘 Đăng nhập Facebook"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (FB)"
            st.rerun()
    with col4:
        if st.button("🍏 Đăng nhập iCloud"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (iCloud)"
            st.rerun()

else:
    # --- THANH SIDEBAR ---
    with st.sidebar:
        st.markdown(f"""
            <div class="user-card">
                <h3 style="color: #C71585; margin: 0;">🌸 {st.session_state.user_name}</h3>
                <p style="color: #666; font-size: 0.9rem; margin: 5px 0;">ID: <code>{st.session_state.user_id}</code></p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Đăng xuất tài khoản"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.divider()
        
        # 🎧 Nhạc Lofi
        st.subheader("🎧 Study Lofi Radio")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        
        st.divider()
        
        # Cài đặt Ngôn ngữ & Giao diện
        st.subheader("🌐 Ngôn ngữ / Language")
        selected_lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English", "한국어", "Français", "Deutsch", "日本語", "Español", "Русский", "中文"])
        
        st.subheader("🎨 Giao diện & Hình nền")
        bg_choice = st.selectbox("Chọn hình nền", ["Hồng mộng mơ (Tĩnh)", "Dải ngân hà hồng (Động)", "Sóng biển hồng (Động)", "Dark Mode Hồng đêm (Tĩnh)"])
        uploaded_bg = st.file_uploader("Tải ảnh nền từ máy lên", type=["png", "jpg", "jpeg"])
        
        st.divider()
        
        if st.button("➕ Tạo cuộc trò chuyện mới"):
            new_chat = {"id": len(st.session_state.chats_db) + 1, "title": f"Đoạn chat mới {len(st.session_state.chats_db)+1}", "messages": []}
            st.session_state.chats_db.append(new_chat)
            st.success("Đã tạo phòng chat mới!")
            
        search_kw = st.text_input("🔍 Tìm kiếm lịch sử...")
        
        st.subheader("📜 Lịch sử trò chuyện")
        for chat in st.session_state.chats_db:
            cols = st.columns([4, 1])
            with cols[0]:
                if st.button(chat["title"], key=f"chat_hist_{chat['id']}"):
                    st.toast(f"Đang mở: {chat['title']}")
            with cols[1]:
                if st.button("🗑️", key=f"del_chat_{chat['id']}"):
                    st.session_state.chats_db.remove(chat)
                    st.rerun()
                    
        st.divider()
        
        st.subheader("🎙️ Giọng nói P.H.U.C.S")
        voice_gender = st.radio("Giới tính giọng nói:", ["Nam", "Nữ"])
        if voice_gender == "Nam":
            v_type = st.selectbox("Chất giọng Nam:", ["Nam cao", "Nam thấp", "Nam trầm", "Nam Trung"])
            v_region = st.selectbox("Vùng miền Nam:", ["Miền Bắc", "Miền Trung", "Miền Nam"])
        else:
            v_type = st.selectbox("Chất giọng Nữ:", ["Nữ cao", "Nữ thấp", "Nữ trầm", "Nữ Trung"])
            v_region = st.selectbox("Vùng miền Nữ:", ["Miền Bắc", "Miền Trung", "Miền Nam"])

        st.divider()
        
        # --- CÀI ĐẶT GROQ API ĐÃ ĐƯỢC ĐIỀN SẴN KEY CỦA GIA PHÚC ---
        with st.expander("⚙️ Cài đặt Groq API (Đã kích hoạt)"):
            st.markdown("### ⚡ Cấu hình Groq Cloud API")
            # Điền sẵn API Key của bạn
            groq_api_key = st.text_input(
                "Mã Groq API Key:", 
                value="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", 
                type="password"
            )
            
            # Chọn Model Groq mới nhất
            groq_model = st.selectbox(
                "Model Groq AI Đang Dùng", 
                [
                    "llama-3.3-70b-versatile",  # Model mới nhất, mạnh nhất
                    "llama-3.1-8b-instant",     # Tốc độ cực nhanh
                    "mixtral-8x7b-32768"        # Model đa nhiệm
                ]
            )
            
            st.success("🟢 API Key của Gia Phúc đã sẵn sàng sử dụng!")
                
            st.markdown("### 💎 Nâng cấp P.H.U.C.S AI Plus")
            st.info("Giá: **35.000 VNĐ / năm**\n\n- Mở rộng lưu trữ từ **400GB^2 lên 500GB^2**.")
            if st.button("Nâng cấp ngay"):
                st.balloons()
                st.success("Cảm ơn bạn đã nâng cấp!")

    # --- MÀN HÌNH CHÍNH ---
    st.markdown('<h1 class="main-title">🌸 P.H.U.C.S - AI STUDY ASSISTANT 🌸</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Đồng hành cùng P.H.U.C.S, vững bước thành công"</p>', unsafe_allow_html=True)
    
    tab_chat, tab_clock, tab_calendar, tab_todo, tab_analytics, tab_formulas, tab_chatgroup, tab_notes, tab_charts, tab_games, tab_models = st.tabs([
        "💬 Trợ lý AI (Groq)", 
        "⏱️ Đồng hồ", 
        "📅 Lịch", 
        "📝 To-Do", 
        "📈 Thống kê", 
        "🧮 Công thức", 
        "👥 Nhóm chat", 
        "📓 Note & Vẽ", 
        "📊 Biểu đồ", 
        "🎮 Trò chơi", 
        "🧪 Mô hình"
    ])
    
    # ---------------- TAB 1: TRỢ LÝ AI (SỬ DỤNG GROQ API) ----------------
    with tab_chat:
        st.markdown("### 🤖 Trò chuyện thông minh cùng P.H.U.C.S AI (Groq Speed)")
        st.markdown("Trả lời chính xác, chi tiết mọi câu hỏi học tập (Toán, Văn, Lý, Hóa, Sinh, Sử, Địa, IELTS,...) với tốc độ siêu nhanh.")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar="🌸" if msg["role"]=="assistant" else "👤"):
                st.markdown(msg["content"])
                
        with st.container():
            col_plus, col_input = st.columns([1, 10])
            with col_plus:
                with st.popover("➕"):
                    st.write("**Công cụ đa phương tiện:**")
                    st.file_uploader("Gửi ảnh phân tích", type=["png", "jpg"])
                    st.file_uploader("Gửi video học tập", type=["mp4"])
                    if st.button("🎙️ Ghi âm giọng nói"): st.info("Đang lắng nghe...")
                    if st.button("🎨 Tạo ảnh AI"): st.success("Đã kích hoạt tạo ảnh!")
                    if st.button("🎵 Sáng tác nhạc"): st.success("Đã tạo nhạc lofi!")
            
            with col_input:
                user_prompt = st.chat_input("Nhập câu hỏi cho P.H.U.C.S AI...")
                
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant", avatar="🌸"):
                with st.spinner("P.H.U.C.S (Groq Engine) đang xử lý câu hỏi..."):
                    ai_reply = ""
                    # Tự động gọi Groq API bằng Key đã cài sẵn
                    if groq_api_key and HAS_GROQ:
                        try:
                            client = Groq(api_key=groq_api_key)
                            
                            system_instruction = (
                                "Bạn là P.H.U.C.S (Personal Highly Useful Computer System), một trợ lý AI hỗ trợ học tập xịn, "
                                "sang, cao cấp, thân thiện, gần gũi và lịch sự. Hãy trả lời cực kỳ chính xác, chi tiết, "
                                "đầy đủ cho người dùng Nguyễn Gia Phúc về các chủ đề học tập, luyện thi và đời sống."
                            )
                            
                            messages_payload = [{"role": "system", "content": system_instruction}]
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
                            ai_reply = f"⚠️ Lỗi kết nối Groq API: {e}. Vui lòng kiểm tra lại cấu hình."
                    
                    if not ai_reply:
                        ai_reply = "Xin lỗi Gia Phúc, P.H.U.C.S gặp chút gián đoạn kết nối. Bạn hãy kiểm tra lại gói thư viện groq trên Streamlit nhé!"
                    
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    # ---------------- TAB 2: ĐỒNG HỒ ----------------
    with tab_clock:
        st.markdown("### ⏱️ Đồng hồ bấm giờ học tập")
        c1, c2 = st.columns(2)
        with c1:
            subject = st.selectbox("Chọn môn học", ["Ngữ Văn", "Toán học", "Vật lí", "Sinh Học", "Tiếng Anh", "Lịch Sử", "Địa Lí", "Tự đặt tên"])
        with c2:
            st.info("💡 Bấm 'Bắt đầu' để hệ thống đếm giờ.")
            
        st.markdown("<h2 style='text-align: center; color: #DB7093;'>00:00:00</h2>", unsafe_allow_html=True)
        b1, b2, b3, b4 = st.columns(4)
        if b1.button("▶️ Bắt đầu"): st.toast("Đã đếm giờ!")
        if b2.button("⏸️ Tạm dừng"): st.toast("Đã tạm dừng!")
        if b3.button("🔄 Đặt lại"): st.toast("Đã reset!")
        if b4.button("💾 Lưu thời gian"): st.success("Đã lưu thời gian học tập!")

    # ---------------- TAB 3: LỊCH & SỰ KIỆN ----------------
    with tab_calendar:
        st.markdown("### 📅 Lịch & Sự kiện")
        selected_date = st.date_input("Chọn ngày", datetime.date.today())
        with st.form("ev_form"):
            ev_name = st.text_input("Tên sự kiện")
            ev_cat = st.selectbox("Phân loại", ["Sinh nhật", "Kỷ niệm", "Thi cử", "Quan trọng", "Khác"])
            ev_date = st.date_input("Ngày diễn ra")
            if st.form_submit_button("Lưu sự kiện") and ev_name:
                st.session_state.events.append({"name": ev_name, "category": ev_cat, "date": str(ev_date)})
                st.success("Đã thêm sự kiện!")
        
        filtered_events = [e for e in st.session_state.events if e['date'] == str(selected_date)]
        if not filtered_events:
            st.info("Không có sự kiện trong ngày này.")
        else:
            for ev in filtered_events:
                st.markdown(f"- **{ev['name']}** [{ev['category']}]")

    # ---------------- TAB 4: TO-DO LIST ----------------
    with tab_todo:
        st.markdown("### 📝 Quản lý To-Do List")
        new_t = st.text_input("Thêm nhiệm vụ mới...")
        if st.button("Thêm nhiệm vụ") and new_t:
            st.session_state.todos.append({"task": new_t, "done": False, "date": datetime.datetime.now().strftime("%d/%m/%Y")})
            st.success("Đã thêm!")
            
        t1, t2 = st.columns(2)
        with t1:
            st.markdown("#### ⏳ Chưa hoàn thành")
            for idx, item in enumerate(st.session_state.todos):
                if not item["done"]:
                    sc = st.columns([3, 1])
                    sc[0].write(f"❌ {item['task']}")
                    if sc[1].button("Xong", key=f"td_{idx}"):
                        st.session_state.todos[idx]["done"] = True
                        st.rerun()
        with t2:
            st.markdown("#### ✅ Đã hoàn thành")
            for item in st.session_state.todos:
                if item["done"]:
                    st.write(f"✔️ ~~{item['task']}~~")

    # ---------------- TAB 5: THỐNG KÊ & TIẾN ĐỘ ----------------
    with tab_analytics:
        st.markdown("### 📈 Thống kê & Tiến độ học tập")
        col_st1, col_st2, col_st3 = st.columns(3)
        with col_st1:
            st.markdown('<div class="stat-card"><h3>24.5 Giờ</h3><p>Tổng thời gian học tuần này</p></div>', unsafe_allow_html=True)
        with col_st2:
            st.markdown('<div class="stat-card"><h3>88%</h3><p>Tỷ lệ hoàn thành To-Do List</p></div>', unsafe_allow_html=True)
        with col_st3:
            st.markdown('<div class="stat-card"><h3>15 Ngày</h3><p>Chuỗi chuyên cần liên tục</p></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 Biểu đồ phân bổ thời gian học")
        fig, ax = plt.subplots()
        subjects = ['Toán', 'Văn', 'Anh', 'Lý', 'Hóa', 'Sử', 'Địa']
        hours = [6.5, 4.0, 5.0, 3.5, 3.0, 1.5, 1.0]
        ax.bar(subjects, hours, color='#FF69B4')
        ax.set_facecolor('#FFF0F5')
        st.pyplot(fig)

    # ---------------- TAB 6: KHO CÔNG THỨC ----------------
    with tab_formulas:
        st.markdown("### 🧮 Tra cứu Công thức Khoa học")
        subject_f = st.selectbox("Chọn môn học", ["Toán học", "Vật lí", "Hóa học"])
        if subject_f == "Toán học":
            st.info("**Công thức Giải tích & Hình học:**\n- Đạo hàm: $(x^n)' = n.x^{n-1}$\n- Nguyên hàm: $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C$\n- Thể tích khối chóp: $V = \\frac{1}{3} B.h$")
        elif subject_f == "Vật lí":
            st.info("**Công thức Vật lí THPT:**\n- Dao động điều hòa: $x = A \\cos(\\omega t + \\varphi)$\n- Định luật II Newton: $\\vec{F} = m.\\vec{a}$\n- Thấu kính hội tụ: $\\frac{1}{f} = \\frac{1}{d} + \\frac{1}{d'}$")
        else:
            st.info("**Hóa học:**\n- Số mol: $n = \\frac{m}{M} = \\frac{V}{22.4}$\n- Phương trình Clapeyron: $p.V = n.R.T$")

    # ---------------- TAB 7: NHÓM CHAT ----------------
    with tab_chatgroup:
        st.markdown("### 👥 Nhóm chat trực tuyến")
        gid = st.text_input("Nhập ID phòng chat:")
        if st.button("Vào phòng"): st.success(f"Đã kết nối phòng {gid}!")
        
        gc1, gc2 = st.columns([1, 3])
        with gc1:
            st.button("🌸 Bạn thân: Gia Phúc")
            st.button("🌸 Nhóm Ôn Thi")
        with gc2:
            st.container(height=250)
            st.chat_input("Nhập tin nhắn...")
            if st.button("📞 Gọi Audio"): st.info("Đang gọi thoại...")

    # ---------------- TAB 8: NOTE & BẢNG VẼ ----------------
    with tab_notes:
        st.markdown("### 📓 Note & Bảng vẽ Studio Pro")
        m_note = st.radio("Chế độ:", ["Soạn thảo văn bản", "Bảng vẽ Studio Pro"], horizontal=True)
        if m_note == "Soạn thảo văn bản":
            ntitle = st.text_input("Tiêu đề ghi chú")
            ncontent = st.text_area("Nội dung...", height=150)
            if st.button("Lưu ghi chú") and ntitle:
                st.session_state.notes_list.append({"title": ntitle, "content": ncontent, "type": "text"})
                st.success("Đã lưu!")
        else:
            st.info("Bảng vẽ Paint Studio Pro sẵn sàng phác thảo!")
            if st.button("Lưu bảng vẽ"):
                st.session_state.notes_list.append({"title": "Bảng vẽ", "content": "[Paint]", "type": "paint"})
                st.success("Đã lưu bảng vẽ!")
                
        st.markdown("#### 📂 Kho lưu trữ")
        for i, it in enumerate(st.session_state.notes_list):
            if st.button(f"Xóa: {it['title']}", key=f"del_n_{i}"):
                st.session_state.notes_list.pop(i)
                st.rerun()

    # ---------------- TAB 9: BIỂU ĐỒ ----------------
    with tab_charts:
        st.markdown("### 📊 Trình tạo biểu đồ")
        ctype = st.selectbox("Loại biểu đồ", ["Biểu đồ tròn", "Biểu đồ cột"])
        fig, ax = plt.subplots()
        if ctype == "Biểu đồ tròn":
            ax.pie([40, 30, 20, 10], labels=['Toán', 'Văn', 'Anh', 'Khác'], colors=['#FF69B4', '#FFB6C1', '#DB7093', '#FFC0CB'], autopct='%1.1f%%')
        else:
            ax.bar(['T2', 'T3', 'T4', 'T5', 'T6'], [5, 7, 6, 8, 4], color='#DB7093')
        st.pyplot(fig)

    # ---------------- TAB 10: TRÒ CHƠI (30 TRÒ) ----------------
    with tab_games:
        st.markdown("### 🎮 Kho trò chơi giải trí (30 trò)")
        g_sel = st.selectbox("Chọn trò chơi", [f"Trò chơi trí tuệ số {i}" for i in range(1, 31)])
        if st.button("Chơi ngay"):
            st.balloons()
            st.success(f"Đang khởi động {g_sel}!")

    # ---------------- TAB 11: MÔ HÌNH KHOA HỌC ----------------
    with tab_models:
        st.markdown("### 🧪 Mô hình Khoa học 3D")
        st.selectbox("Chọn mô hình", ["Hệ Mặt Trời", "Dao động lò xo", "Không gian OXYZ", "Phân tử hóa học"])
        st.info("Mô hình tương tác trực quan thời gian thực đang hiển thị.")
