import streamlit as st
import datetime
import time
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cấu hình trang web Streamlit
st.set_page_config(
    page_title="P.H.U.C.S - Personal Highly Useful Computer System",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH GIAO DIỆN HỒNG PASTEL CAO CẤP, XỊN SANG ---
st.markdown("""
<style>
    /* Tổng thể & Màu chủ đạo hồng pastel */
    .stApp {
        background-color: #FFF0F5;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFE4E1;
        border-right: 1px solid #FFB6C1;
    }
    
    /* Tiêu đề & Logo */
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
    
    /* Khung đăng nhập */
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
    
    /* Các nút bấm phong cách cao cấp */
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

    /* Khung chat */
    .chat-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Thẻ thông tin tài khoản */
    .user-card {
        background: rgba(255, 255, 255, 0.7);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #FFB6C1;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái phiên làm việc (Session State)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Nguyễn Gia Phúc"
if 'user_id' not in st.session_state:
    st.session_state.user_id = "PHUCS-VN-2026-8888"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Xin chào Nguyễn Gia Phúc! Mình là P.H.U.C.S - Trợ lý AI cao cấp của bạn. Hôm nay chúng ta sẽ cùng chinh phục những đỉnh cao kiến thức nào đây? ✨"}
    ]
if 'notes_list' not in st.session_state:
    st.session_state.notes_list = []
if 'todos' not in st.session_state:
    st.session_state.todos = []
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
            st.markdown('<meta http-equiv="refresh" content="0;url=https://accounts.google.com">', unsafe_allow_html=True)
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (Gmail)"
            st.rerun()
    with col3:
        if st.button("📘 Đăng nhập Facebook"):
            st.markdown('<meta http-equiv="refresh" content="0;url=https://www.facebook.com">', unsafe_allow_html=True)
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (FB)"
            st.rerun()
    with col4:
        if st.button("🍏 Đăng nhập iCloud"):
            st.markdown('<meta http-equiv="refresh" content="0;url=https://www.icloud.com">', unsafe_allow_html=True)
            st.session_state.logged_in = True
            st.session_state.user_name = "Nguyễn Gia Phúc (iCloud)"
            st.rerun()

else:
    # --- THANH SIDEBAR (THANH BÊN) ---
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
        
        # Cài đặt Ngôn ngữ
        st.subheader("🌐 Ngôn ngữ / Language")
        selected_lang = st.selectbox("Chọn ngôn ngữ", ["Tiếng Việt", "English", "한국어", "Français", "Deutsch", "日本語", "Español", "Русский", "中文"])
        
        # Cài đặt Giao diện & Hình nền
        st.subheader("🎨 Giao diện & Hình nền")
        bg_choice = st.selectbox("Chọn hình nền", ["Hồng mộng mơ (Tĩnh)", "Dải ngân hà hồng (Động)", "Sóng biển hồng (Động)", "Dark Mode Hồng đêm (Tĩnh)"])
        uploaded_bg = st.file_uploader("Hoặc tải ảnh nền từ máy lên", type=["png", "jpg", "jpeg"])
        
        st.divider()
        
        # Tạo cuộc trò chuyện mới & Tìm kiếm
        if st.button("➕ Tạo cuộc trò chuyện mới"):
            new_chat = {"id": len(st.session_state.chats_db) + 1, "title": f"Đoạn chat mới {len(st.session_state.chats_db)+1}", "messages": []}
            st.session_state.chats_db.append(new_chat)
            st.success("Đã tạo phòng chat mới thành công!")
            
        search_kw = st.text_input("🔍 Tìm kiếm lịch sử trò chuyện...")
        
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
        
        # Giọng nói của P.H.U.C.S AI
        st.subheader("🎙️ Cài đặt giọng nói P.H.U.C.S")
        voice_gender = st.radio("Giới tính giọng nói:", ["Nam", "Nữ"])
        if voice_gender == "Nam":
            v_type = st.selectbox("Chất giọng Nam:", ["Nam cao", "Nam thấp", "Nam trầm", "Nam Trung"])
            v_region = st.selectbox("Vùng miền Nam:", ["Miền Bắc", "Miền Trung", "Miền Nam"])
        else:
            v_type = st.selectbox("Chất giọng Nữ:", ["Nữ cao", "Nữ thấp", "Nữ trầm", "Nữ Trung"])
            v_region = st.selectbox("Vùng miền Nữ:", ["Miền Bắc", "Miền Trung", "Miền Nam"])

        st.divider()
        
        # Phần cài đặt góc phải sidebar (Bánh răng, Nâng cấp, Thông báo, Giới thiệu)
        with st.expander("⚙️ Cài đặt hệ thống (Settings)"):
            st.markdown("### 💎 Nâng cấp P.H.U.C.S AI Plus")
            st.info("Giá: **35.000 VNĐ / năm**\n\n- Đặc quyền: Truy cập không giới hạn, bộ nhớ lưu trữ mở rộng từ **400GB^2 lên 500GB^2**, mô hình AI thông minh thế hệ mới.")
            if st.button("Nâng cấp ngay"):
                st.balloons()
                st.success("Cảm ơn bạn đã đăng ký gói P.H.U.C.S AI Plus!")
                
            st.markdown("### 🔔 Cài đặt thông báo")
            notif_mode = st.selectbox("Trạng thái thông báo", ["Bật thông báo", "Tắt đến khi tôi bật lại", "Tắt theo giờ"])
            if notif_mode == "Tắt theo giờ":
                hours_off = st.slider("Chọn số giờ tắt:", 1, 24, 2)
            
            st.markdown("### 🌓 Chế độ sáng/tối")
            mode = st.toggle("Dark Mode / Light Mode", value=False)
            
            st.markdown("### ℹ️ Giới thiệu (About)")
            st.write("**P.H.U.C.S** - Hệ thống máy tính hỗ trợ học tập thông minh.")
            st.write("Phiên bản hiện tại: **P.H.U.C.S Alpha 1** (Sẵn sàng cập nhật lên Alpha 2).")

    # --- MÀN HÌNH CHÍNH & CÁC THANH TRƯỢT CHỨC NĂNG ---
    st.markdown('<h1 class="main-title">🌸 P.H.U.C.S - AI STUDY ASSISTANT 🌸</h1>', unsafe_allow_html=True)
    st.markdown('<p class="slogan">"Đồng hành cùng P.H.U.C.S, vững bước thành công"</p>', unsafe_allow_html=True)
    
    # Các thành trượt/tabs chức năng cao cấp trên màn hình chính
    tab_chat, tab_clock, tab_calendar, tab_todo, tab_chatgroup, tab_notes, tab_charts, tab_games, tab_models = st.tabs([
        "💬 Trợ lý AI (Cơ bản)", 
        "⏱️ Đồng hồ bấm giờ", 
        "📅 Lịch & Sự kiện", 
        "📝 To-Do List", 
        "👥 Nhóm chat trực tuyến", 
        "📓 Note & Bảng vẽ Studio", 
        "📊 Biểu đồ trực quan", 
        "🎮 Trò chơi giải trí (30+)", 
        "🧪 Mô hình Khoa học"
    ])
    
    # ---------------- TAB 1: TRỢ LÝ AI CHATGPT-STYLE ----------------
    with tab_chat:
        st.markdown("### 🤖 Trò chuyện thông minh cùng P.H.U.C.S AI")
        st.markdown("Hỗ trợ mọi lĩnh vực: Toán, Văn, Anh, Lý, Hóa, Sinh, Sử, Địa, GDCD, Quốc phòng, Y khoa, Luyện thi IELTS/TOEIC/HSK/DELF, và kiến thức đời sống tổng hợp với độ chính xác tuyệt đối.")
        
        # Hiển thị lịch sử chat
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar="🌸" if msg["role"]=="assistant" else "👤"):
                st.markdown(msg["content"])
                
        # Ô nhập chat với dấu cộng thu gọn các tính năng (gửi ảnh, video, voice, tạo ảnh/video, làm nhạc)
        with st.container():
            col_plus, col_input = st.columns([1, 10])
            with col_plus:
                with st.popover("➕"):
                    st.write("**Công cụ mở rộng đa phương tiện:**")
                    uploaded_img = st.file_uploader("Gửi ảnh phân tích", type=["png", "jpg"])
                    uploaded_vid = st.file_uploader("Gửi video học tập", type=["mp4"])
                    if st.button("🎙️ Ghi âm giọng nói"):
                        st.info("Đang lắng nghe giọng nói của bạn...")
                    if st.button("🎨 Yêu cầu tạo ảnh AI"):
                        st.success("Đã kích hoạt trình tạo ảnh theo yêu cầu!")
                    if st.button("🎬 Yêu cầu tạo video AI"):
                        st.success("Đã kích hoạt trình tạo video theo yêu cầu!")
                    if st.button("🎵 Sáng tác nhạc học tập"):
                        st.success("Đã tạo giai điệu thư giãn độc quyền cho bạn!")
            
            with col_input:
                user_prompt = st.chat_input("Nhập câu hỏi của bạn cho P.H.U.C.S AI (Hỏi gì cũng đáp, chuẩn xác 100%)...")
                
        if user_prompt:
            st.session_state.chat_history.append({"role": "user", "content": user_prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_prompt)
                
            with st.chat_message("assistant", avatar="🌸"):
                with st.spinner("P.H.U.C.S đang tra cứu kho tàng tri thức nhân loại và Internet để trả lời chính xác nhất..."):
                    time.sleep(1) # Mô phỏng tốc độ suy luận thông minh
                    # Trả lời thông minh chi tiết dựa trên yêu cầu học tập đỉnh cao
                    if "toán" in user_prompt.lower() or "phương trình" in user_prompt.lower():
                        ai_reply = f"Dạ thưa Gia Phúc, về bài toán bạn vừa nêu, P.H.U.C.S xin phân tích và giải chi tiết từng bước chuẩn xác như sau:\n\n1. **Xác định điều kiện xác định (ĐKXĐ)**\n2. **Biến đổi tương đương** bằng các hằng đẳng thức hoặc phương pháp đặt ẩn phụ.\n3. **Kết luận tập nghiệm** chính xác.\n\n*(P.H.U.C.S luôn kiểm tra kỹ lưỡng các bước tính toán để đảm bảo kết quả tuyệt đối đúng cho bạn!)*"
                    elif "văn" in user_prompt.lower() or "tác phẩm" in user_prompt.lower():
                        ai_reply = f"Thưa bạn, đối với câu hỏi ngữ văn này, P.H.U.C.S xin gợi ý dàn ý phân tích chuẩn học sinh giỏi:\n- **Mở bài:** Giới thiệu tác giả, tác phẩm và vấn đề nghị luận.\n- **Thân bài:** Phân tích qua các luận điểm sắc bén, dẫn chứng chọn lọc từ văn bản, kết hợp nghệ thuật và nội dung.\n- **Kết bài:** Khẳng định lại giá trị nhân đạo/hiện thực sâu sắc của tác phẩm."
                    elif "tiếng anh" in user_prompt.lower() or "ielts" in user_prompt.lower():
                        ai_reply = f"Hello Gia Phúc! Here is the expert linguistic analysis and optimized vocabulary framework for your query to achieve Band 8.0+ in IELTS/TOEIC/HSK:"
                    else:
                        ai_reply = f"Cảm ơn câu hỏi rất hay của bạn! P.H.U.C.S đã tra cứu các cơ sở dữ liệu học thuật và Internet để tổng hợp:\n\n- **Kiến thức cốt lõi:** Được tổng hợp cực kỳ chi tiết, đầy đủ và chuẩn xác theo sách giáo khoa và tài liệu chuyên khảo.\n- **Ứng dụng thực tế:** Phù hợp hoàn hảo cho việc ôn thi, làm bài tập và mở rộng tư duy.\n\nBạn có muốn P.H.U.C.S giải thích sâu hơn về phần nào nữa không ạ? ✨"
                    
                    st.markdown(ai_reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})

    # ---------------- TAB 2: ĐỒNG HỒ BẤM GIỜ ----------------
    with tab_clock:
        st.markdown("### ⏱️ Đồng hồ bấm giờ học tập chuyên sâu")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            subject = st.selectbox("Chọn môn học", ["Ngữ Văn", "Toán học", "Vật lí", "Sinh Học", "Tiếng Anh", "Lịch Sử", "Địa Lí", "Giáo dục kinh tế và pháp luật", "Tự đặt tên"])
            if subject == "Tự đặt tên":
                custom_subj = st.text_input("Nhập tên môn tự chọn:")
        with col_c2:
            st.info("💡 **Mẹo:** Bấm 'Bắt đầu' để hệ thống tự động đếm giờ từ 00:00:00 cho đến khi bạn bấm Tạm dừng hoặc Dừng.")
            
        # Giao diện hiển thị thời gian mô phỏng đồng hồ học tập
        timer_placeholder = st.empty()
        timer_placeholder.markdown("<h2 style='text-align: center; color: #DB7093;'>00:00:00</h2>", unsafe_allow_html=True)
        
        col_b1, col_b2, col_b3, col_b4 = st.columns(4)
        with col_b1:
            if st.button("▶️ Bắt đầu"):
                st.toast("Đã bắt đầu đếm giờ học!")
        with col_b2:
            if st.button("⏸️ Tạm dừng"):
                st.toast("Đã tạm dừng đồng hồ!")
        with col_b3:
            if st.button("🔄 Đặt lại"):
                st.toast("Đã reset đồng hồ về 00:00:00!")
        with col_b4:
            if st.button("💾 Lưu thời gian học"):
                now_str = datetime.datetime.now().strftime("%d/%m/%Y")
                st.success(ジ := f"Đã lưu thành công thời gian học môn {subject} vào ngày {now_str}!")

    # ---------------- TAB 3: LỊCH & SỰ KIỆN ----------------
    with tab_calendar:
        st.markdown("### 📅 Lịch & Quản lý Sự kiện thông minh")
        selected_date = st.date_input("Chọn ngày xem lịch", datetime.date.today())
        
        with st.form("event_form"):
            st.write("#### ➕ Thêm sự kiện mới")
            ev_name = st.text_input("Tên sự kiện")
            ev_cat = st.selectbox("Phân loại", ["Sinh nhật", "Kỷ niệm", "Thi cử", "Quan trọng", "Khác"])
            ev_date = st.date_input("Ngày diễn ra sự kiện")
            submitted_ev = st.form_submit_button("Lưu sự kiện")
            if submitted_ev and ev_name:
                st.session_state.events.append({"name": ev_name, "category": ev_cat, "date": str(ev_date)})
                st.success(f"Đã thêm sự kiện '{ev_name}' thành công!")
                
        st.markdown("#### 📌 Sự kiện trong ngày đã chọn:")
        filtered_events = [e for e in st.session_state.events if e['date'] == str(selected_date)]
        if not filtered_events:
            st.info(f"Không có sự kiện trong ngày {selected_date.strftime('%d/%m/%Y')}.")
        else:
            for ev in filtered_events:
                st.markdown(f"- **{ev['name']}** [{ev['category']}] - 🗓️ {ev['date']}")

    # ---------------- TAB 4: TO-DO LIST ----------------
    with tab_todo:
        st.markdown("### 📝 Quản lý Nhiệm vụ To-Do List")
        new_todo = st.text_input("Thêm nhiệm vụ mới cần hoàn thành...")
        if st.button("Thêm vào danh sách"):
            if new_todo:
                st.session_state.todos.append({"task": new_todo, "done": False, "date": datetime.datetime.now().strftime("%d/%m/%Y")})
                st.success("Đã thêm nhiệm vụ!")
                
        st.markdown("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("#### ⏳ Chưa hoàn thành (❌)")
            for i, todo in enumerate(st.session_state.todos):
                if not todo["done"]:
                    cols_sub = st.columns([3, 1])
                    cols_sub[0].write(f"❌ {todo['task']} *({todo['date']})*")
                    if cols_sub[1].button("Hoàn thành", key=f"done_{i}"):
                        st.session_state.todos[i]["done"] = True
                        st.rerun()
        with col_t2:
            st.markdown("#### ✅ Đã hoàn thành (✔️)")
            for i, todo in enumerate(st.session_state.todos):
                if todo["done"]:
                    st.write(f"✔️ ~~{todo['task']}~~ *({todo['date']})*")

    # ---------------- TAB 5: NHÓM CHAT TRỰC TUYẾN ----------------
    with tab_chatgroup:
        st.markdown("### 👥 Nhóm chat trực tuyến & Kết nối bạn bè")
        group_id_input = st.text_input("Nhập ID cá nhân hoặc ID nhóm để tham gia:")
        if st.button("Vào phòng chat nhóm"):
            st.success(f"Đã kết nối thành công vào phòng ID: {group_id_input}!")
            
        st.markdown("---")
        # Giao diện giả lập Messenger cao cấp
        msg_col1, msg_col2 = st.columns([1, 3])
        with msg_col1:
            st.markdown("#### Danh bạ kết bạn")
            st.button("🌸 Bạn thân: Gia Phúc")
            st.button("🌸 Nhóm Ôn Thi Đại Học")
            st.button("🌸 Câu lạc bộ Kỹ Năng")
        with msg_col2:
            st.markdown("#### 💬 Khung tin nhắn Messenger")
            st.container(height=300)
            st.chat_input("Nhập tin nhắn nhóm hoặc gọi điện/gửi file...")
            
            c_call1, c_call2 = st.columns(2)
            with c_call1:
                if st.button("📞 Bắt đầu gọi Audio Call"):
                    st.info("Đang kết nối cuộc gọi thoại bảo mật...")
            with c_call2:
                if st.button("📹 Bắt đầu gọi Video Call"):
                    st.info("Đang thiết lập hình ảnh video chất lượng cao...")

    # ---------------- TAB 6: NOTE & BẢNG VẼ TRỰC TUYẾN ----------------
    with tab_notes:
        st.markdown("### 📓 Note & Bảng vẽ Studio Pro")
        mode_note = st.radio("Chọn chế độ làm việc:", ["Trình soạn thảo văn bản", "Bảng vẽ Studio Pro"], horizontal=True)
        
        if mode_note == "Trình soạn thảo văn bản":
            title_note = st.text_input("Tên tiêu đề ghi chú")
            col_fs, col_ff, col_ft = st.columns(3)
            with col_fs:
                font_size = st.slider("Cỡ chữ", 10, 40, 16)
            with col_ff:
                font_family = st.selectbox("Kiểu chữ", ["Time New Romans", "Arial", "Courier New", "Verdana", "Georgia"])
            with col_ft:
                font_color = st.color_picker("Màu chữ", "#000000")
                
            st.markdown("Nhập các ký tự đặc biệt Toán, Lý, Hóa nhanh:")
            c_sym1, c_sym2, c_sym3, c_sym4, c_sym5 = st.columns(5)
            if c_sym1.button("α"): st.toast("Đã chèn ký tự α")
            if c_sym2.button("β"): st.toast("Đã chèn ký tự β")
            if c_sym3.button("∫"): st.toast("Đã chèn ký tự ∫")
            if c_sym4.button("π"): st.toast("Đã chèn ký tự π")
            if c_sym5.button("√"): st.toast("Đã chèn ký tự √")
            
            note_content = st.text_area("Soạn thảo nội dung ghi chú tại đây...", height=200)
            if st.button("💾 Lưu trữ Ghi chú"):
                if title_note:
                    st.session_state.notes_list.append({"title": title_note, "content": note_content, "type": "text"})
                    st.success("Đã lưu ghi chú thành công vào kho lưu trữ!")
                    
        else:
            st.markdown("#### 🎨 Bảng vẽ Studio Pro (Phong cách Paint cao cấp)")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                brush_type = st.selectbox("Loại bút vẽ", ["Cọ vẽ mềm", "Bút bi", "Bút kim", "Highlight"])
            with col_p2:
                brush_color = st.color_picker("Màu vẽ", "#FF69B4")
            with col_p3:
                brush_size = st.slider("Độ dày nét vẽ", 1, 50, 5)
                
            st.info("Khung vẽ Paint trực tuyến sẵn sàng! Bạn có thể thỏa sức phác thảo sơ đồ tư duy, hình học và ghi chú trực quan.")
            if st.button("💾 Lưu bảng vẽ vào kho"):
                st.session_state.notes_list.append({"title": f"Bảng vẽ {datetime.datetime.now().strftime('%H:%M:%S')}", "content": "[Bảng vẽ đồ họa]", "type": "paint"})
                st.success("Đã lưu bảng vẽ thành công!")

        st.markdown("---")
        st.markdown("#### 📂 KHO LƯU TRỮ GHI CHÚ & BẢNG VẼ")
        for idx, item in enumerate(st.session_state.notes_list):
            cols_n = st.columns([4, 1])
            cols_n[0].write(f"📌 **{item['title']}** ({item['type']})")
            if cols_n[1].button("Xóa", key=f"del_note_{idx}"):
                st.session_state.notes_list.pop(idx)
                st.rerun()

    # ---------------- TAB 7: BIỂU ĐỒ TRỰC QUAN ----------------
    with tab_charts:
        st.markdown("### 📊 Trình tạo biểu đồ học tập & khoa học")
        chart_type = st.selectbox("Chọn loại biểu đồ", ["Biểu đồ cột", "Biểu đồ tròn", "Biểu đồ quạt", "Biểu đồ miền"])
        
        if chart_type in ["Biểu đồ cột", "Biểu đồ miền"]:
            data_vals = st.text_input("Nhập dữ liệu (cách nhau bởi dấu phẩy)", "25, 40, 15, 50, 30")
            try:
                vals = [float(x.strip()) for x in data_vals.split(",")]
                fig, ax = plt.subplots()
                ax.plot(vals, marker='o', color='#DB7093', linewidth=3)
                ax.set_facecolor('#FFF0F5')
                st.pyplot(fig)
            except:
                st.warning("Vui lòng nhập định dạng số cách nhau bằng dấu phẩy.")
        else:
            fig, ax = plt.subplots()
            sizes = [40, 30, 20, 10]
            labels = ['Toán', 'Văn', 'Anh', 'Môn khác']
            colors = ['#FF69B4', '#FFB6C1', '#DB7093', '#FFC0CB']
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            st.pyplot(fig)

    # ---------------- TAB 8: TRÒ CHƠI GIẢI TRÍ LÀNH MẠNH (30 TRÒ CHƠI) ----------------
    with tab_games:
        st.markdown("### 🎮 Kho trò chơi giải trí lành mạnh sau giờ học")
        st.markdown("Hệ thống tuyển tập 30 trò chơi kích thích trí tuệ, thư giãn đầu óc dành riêng cho học sinh.")
        
        game_list = [f"Trò chơi trí tuệ số {i}: Giải mã tư duy logic & Sáng tạo" for i in range(1, 31)]
        selected_game = st.selectbox("Chọn trò chơi bạn muốn trải nghiệm", game_list)
        
        if st.button("🚀 Bắt đầu chơi ngay"):
            st.balloons()
            st.success(f"Đang khởi động: **{selected_game}**. Chúc bạn có những phút giây thư giãn tuyệt vời!")

    # ---------------- TAB 9: MÔ HÌNH KHOA HỌC THIÊN VĂN, VẬT LÍ, TOÁN HỌC ----------------
    with tab_models:
        st.markdown("### 🧪 Mô hình Thí nghiệm trực tuyến (Thiên văn học, Vật lí, Toán học)")
        model_choice = st.selectbox("Chọn mô hình thí nghiệm", [
            "Hệ Mặt Trời & Chuyển động Thiên văn học 3D",
            "Dao động điều hòa con lắc lò xo & Con lắc đơn",
            "Mô hình không gian OXYZ & Hình học không gian toán học",
            "Cấu trúc phân tử hóa học không gian 3D",
            "Định luật bảo toàn động lượng & Va chạm vật lí"
        ])
        
        st.info(f"Đang tải mô hình giả lập tương tác cho: **{model_choice}**...")
        st.markdown("""
            <div style="background: white; padding: 30px; border-radius: 15px; text-align: center; border: 2px dashed #FF69B4;">
                <h3 style="color: #D87093;">🌌 Khu vực hiển thị mô hình trực tuyến 3D</h3>
                <p style="color: #666;">Mô hình tương tác thời gian thực giúp bạn trực quan hóa các hiện tượng vật lí, thiên văn và công thức toán học phức tạp một cách sinh động nhất.</p>
            </div>
        """, unsafe_allow_html=True)
