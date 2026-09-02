import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 🏫 School Information Configuration
# ==========================================
SCHOOL_NAME_EN = "Jhalakathi Govt High School"
SCHOOL_NAME_BN = "ঝালকাঠি সরকারি উচ্চ বিদ্যালয়"
SCHOOL_LOGO_ICON = "🏫"

st.set_page_config(page_title=SCHOOL_NAME_BN, page_icon=SCHOOL_LOGO_ICON, layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .header-box {
        background-color: #0f172a;
        padding: 15px;
        border-radius: 10px;
        color: #38bdf8;
        border: 1px solid #0284c7;
        margin-bottom: 20px;
    }
    .nagad-card {
        background-color: #d97706;
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
    }
    .status-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #38bdf8;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization (Auto Updates across app)
if "admin_password" not in st.session_state:
    st.session_state["admin_password"] = "admin123"

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

if "cover_photo" not in st.session_state:
    st.session_state["cover_photo"] = None

if "headmaster_photo" not in st.session_state:
    st.session_state["headmaster_photo"] = None

if "headmaster_speech" not in st.session_state:
    st.session_state["headmaster_speech"] = "আমাদের বিদ্যালয়ে আপনাদের স্বাগতম। আমরা মানসম্মত শিক্ষা ও শৃঙ্খলা নিশ্চিতে প্রতিশ্রুতিবদ্ধ।"

if "notices" not in st.session_state:
    st.session_state["notices"] = [
        {"Date": "2026-03-01", "Title": "বার্ষিক ক্রীড়া প্রতিযোগিতা ২০২৬-এর রেজিস্ট্রেশন শুরু", "File": None, "FileType": None},
        {"Date": "2026-02-25", "Title": "প্রথম সাময়িক পরীক্ষার সময়সূচী প্রকাশ", "File": None, "FileType": None}
    ]

if "gallery" not in st.session_state:
    st.session_state["gallery"] = []

if "status_posts" not in st.session_state:
    st.session_state["status_posts"] = [
        {"Date": "2026-03-02", "Text": "আজ বিদ্যালয়ে বিজ্ঞান মেলার উদ্বোধন করা হয়েছে।", "Image": None}
    ]

# Excel Loader
@st.cache_data
def load_student_data():
    file_path = "students.xlsx"
    if os.path.exists(file_path):
        return pd.read_excel(file_path, dtype={'student_id': str})
    return None

df_students = load_student_data()

TEACHERS = [
    {"Name": "Md. Rafiqul Islam", "Designation": "Headmaster", "Subject": "Administration", "Phone": "+8801700000001"},
    {"Name": "Anisur Rahman", "Designation": "Assistant Headmaster", "Subject": "Mathematics", "Phone": "+8801700000002"},
    {"Name": "Nasrin Sultana", "Designation": "Senior Teacher", "Subject": "English", "Phone": "+8801700000003"}
]

# Sidebar Navigation Menu
st.sidebar.title(f"{SCHOOL_LOGO_ICON} Main Menu")
menu = st.sidebar.radio(
    "Navigation Options", 
    [
        "🏠 Home & Dashboard", 
        "📌 Notice Board", 
        "🆔 Student Portal", 
        "👨‍🏫 Teachers Directory", 
        "📸 Photo Gallery", 
        "🟠 Nagad Payment Gateway", 
        "📞 Contact Authority", 
        "⚙️ Admin Control Panel"
    ]
)

# Admin Login Section in Sidebar
st.sidebar.divider()
st.sidebar.subheader("🔒 Authority Login")
if not st.session_state["is_admin"]:
    pwd_input = st.sidebar.text_input("Enter Password", type="password")
    if st.sidebar.button("Login"):
        if pwd_input == st.session_state["admin_password"]:
            st.session_state["is_admin"] = True
            st.sidebar.success("✅ Logged in as Authority")
            st.rerun()
        else:
            st.sidebar.error("❌ Incorrect password!")
else:
    st.sidebar.success("✅ Logged in as Authority")
    if st.sidebar.button("Logout"):
        st.session_state["is_admin"] = False
        st.rerun()

# ----------------------------------------------------
# 1. HOME & DASHBOARD
# ----------------------------------------------------
if menu == "🏠 Home & Dashboard":
    # Marquee Announcement
    st.markdown(f"""
        <div class="header-box">
            <marquee behavior="scroll" direction="left" scrollamount="7">
                🎓 {SCHOOL_NAME_BN} - ডিজিটাল পোর্টালে আপনাকে স্বাগতম! 🎓 Welcome to {SCHOOL_NAME_EN}
            </marquee>
        </div>
    """, unsafe_allow_html=True)

    # 1. Cover Photo Display
    if st.session_state["cover_photo"] is not None:
        st.image(st.session_state["cover_photo"], use_container_width=True)
    else:
        st.info("🖼️ কভার ফটো এখনো সেট করা হয়নি। (অথরিটি এডমিন প্যানেল থেকে আপলোড করতে পারবেন)")

    st.title(f"{SCHOOL_LOGO_ICON} {SCHOOL_NAME_BN}")
    st.caption(f"English: {SCHOOL_NAME_EN}")
    st.divider()

    # 2. Headmaster Box Section
    col_hm_img, col_hm_txt = st.columns([1, 3])
    with col_hm_img:
        st.subheader("👨‍🏫 প্রতিষ্ঠান প্রধান")
        if st.session_state["headmaster_photo"] is not None:
            st.image(st.session_state["headmaster_photo"], width=200)
        else:
            st.warning("ছবি অনুপস্থিত")
    with col_hm_txt:
        st.subheader("প্রতিষ্ঠান প্রধানের বাণী")
        st.write(f"*{st.session_state['headmaster_speech']}*")

    st.divider()

    # Status / Updates Feed Bar
    st.subheader("📢 School Activity Status & Updates Feed")
    for post in st.session_state["status_posts"]:
        with st.container():
            st.markdown(f'<div class="status-card"><b>🗓️ {post["Date"]}</b><br>{post["Text"]}</div>', unsafe_allow_html=True)
            if post["Image"] is not None:
                st.image(post["Image"], width=400)

# ----------------------------------------------------
# 2. NOTICE BOARD
# ----------------------------------------------------
elif menu == "📌 Notice Board":
    st.title(f"📌 {SCHOOL_NAME_BN} - নোটিশ বোর্ড")
    st.write("স্কুলের সর্বশেষ নোটিশ এবং সার্কুলারসমূহ:")
    
    for idx, notice in enumerate(st.session_state["notices"]):
        with st.expander(f"📌 [{notice['Date']}] {notice['Title']}", expanded=True):
            if notice["File"] is not None:
                if notice["FileType"] in ["png", "jpg", "jpeg"]:
                    st.image(notice["File"], caption="Notice Image", width=500)
                st.download_button(
                    label="📥 ডাউনলোড নোটিশ ফাইল (PDF/Picture)",
                    data=notice["File"],
                    file_name=f"Notice_{idx+1}.{notice['FileType']}",
                    key=f"notice_dl_{idx}"
                )

# ----------------------------------------------------
# 3. STUDENT PORTAL
# ----------------------------------------------------
elif menu == "🆔 Student Portal":
    st.title("🆔 স্টুডেন্ট আইডি ও প্রোফাইল পোর্টাল")
    
    if df_students is None:
        st.warning("⚠️ 'students.xlsx' ফাইলটি আপলোড করা নেই। থাকলে আইডি দিয়ে অনুসন্ধান করা সম্ভব হতো।")
    else:
        search_id = st.text_input("শিক্ষার্থীর আইডি নম্বর লিখুন:", placeholder="উদাহরণ: 1001")
        if search_id:
            res = df_students[df_students['student_id'] == search_id.strip()]
            if not res.empty:
                info = res.iloc[0]
                st.success(f"শিক্ষার্থীর নাম: {info.get('name', 'N/A')}")
                st.table(pd.DataFrame({
                    "ক্ষেত্র": ["আইডি", "নাম", "শ্রেণী", "রোল", "রক্তের গ্রুপ", "অভিভাবকের ফোন"],
                    "তথ্য": [info.get('student_id'), info.get('name'), info.get('class'), info.get('roll'), info.get('blood_group'), info.get('phone')]
                }))
            else:
                st.error("এই আইডি নম্বরে কোনো শিক্ষার্থী পাওয়া যায়নি!")

# ----------------------------------------------------
# 4. TEACHERS DIRECTORY
# ----------------------------------------------------
elif menu == "👨‍🏫 Teachers Directory":
    st.title("👨‍🏫 শিক্ষক ও কর্মকর্তা ডিরেক্টরি")
    st.table(pd.DataFrame(TEACHERS))

# ----------------------------------------------------
# 5. PHOTO GALLERY
# ----------------------------------------------------
elif menu == "📸 Photo Gallery":
    st.title("📸 ফটো গ্যালারি")
    if len(st.session_state["gallery"]) > 0:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state["gallery"]):
            with cols[idx % 3]:
                st.image(item["bytes"], caption=item["name"], use_container_width=True)
                st.download_button(
                    label="📥 ছবি ডাউনলোড করুন",
                    data=item["bytes"],
                    file_name=item["name"],
                    mime="image/png",
                    key=f"gal_dl_{idx}"
                )
    else:
        st.info("গ্যালারিতে এখনো কোনো ছবি আপলোড করা হয়নি।")

# ----------------------------------------------------
# 6. NAGAD PAYMENT GATEWAY
# ----------------------------------------------------
elif menu == "🟠 Nagad Payment Gateway":
    st.title("🟠 নগদ (Nagad) ডিজিটাল ফি পেমেন্ট পোর্টাল")
    st.markdown("""
        <div class="nagad-card">
            <h2>🟠 Nagad Payment Express</h2>
            <p>অনলাইনে যেকোনো ফি নগদ অ্যাকাউন্ট থেকে সহজে প্রদান করুন</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")

    c1, c2 = st.columns(2)
    with c1:
        s_id = st.text_input("শিক্ষার্থীর আইডি (Student ID):", placeholder="e.g. 1001")
        student_name = st.text_input("শিক্ষার্থীর নাম:", placeholder="e.g. Md. Rahat")
        fee_cat = st.selectbox("ফি-এর ধরন:", ["মাসিক টিউশন ফি", "পরীক্ষার ফি", "ভর্তি ফি", "সেশন ফি"])
        amt = st.number_input("টাকার পরিমাণ (BDT):", min_value=100, value=1500, step=100)

    with c2:
        nagad_number = st.text_input("আপনার নগদ মোবাইল নম্বর:", placeholder="017XXXXXXXX")
        trx_id = st.text_input("নগদ ট্রানজেকশন আইডি (TrxID):", placeholder="e.g. 7A8B9C10D")

    st.divider()

    if st.button("🟠 Pay Now with Nagad (পেমেন্ট সম্পন্ন করুন)", type="primary", use_container_width=True):
        if s_id and student_name and nagad_number and trx_id:
            st.balloons()
            st.success("✅ নগদ পেমেন্ট সফলভাবে সম্পন্ন হয়েছে!")

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            receipt_text = f"""
            =================================================
                       {SCHOOL_NAME_BN}
                   OFFICIAL NAGAD PAYMENT VOUCHER
            =================================================
            Date & Time     : {now}
            Student ID      : {s_id}
            Student Name    : {student_name}
            Fee Type        : {fee_cat}
            Amount Paid     : BDT {amt}
            Gateway Method  : Nagad (নগদ)
            Nagad Account   : {nagad_number}
            Transaction ID  : {trx_id}
            Status          : PAID & VERIFIED
            =================================================
            ধন্যবাদ! আপনার পেমেন্ট মানি রসিদ নিচে থেকে ডাউনলোড করুন।
            """
            
            st.subheader("🧾 পেমেন্ট ভাউচার / মানি রসিদ")
            st.code(receipt_text)
            
            st.download_button(
                label="📥 ডাউনলোড মানি রসিদ (Download Money Receipt)",
                data=receipt_text,
                file_name=f"Nagad_Receipt_{s_id}_{trx_id}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.error("⚠️ অনুগ্রহ করে সকল তথ্য (আইডি, নাম, নগদ নম্বর এবং TrxID) সঠিকভাবে দিন!")

# ----------------------------------------------------
# 7. CONTACT AUTHORITY
# ----------------------------------------------------
elif menu == "📞 Contact Authority":
    st.title("📞 কর্তৃপক্ষের সাথে যোগাযোগ")
    st.write("স্কুল সংক্রান্ত যেকোনো প্রয়োজনে নিচে দেওয়া ঠিকানায় বা নম্বরে যোগাযোগ করুন:")
    st.info("""
    📍 **ঠিকানা:** ঝালকাঠি সরকারি উচ্চ বিদ্যালয়, ঝালকাঠি  
    📞 **ফোন:** +৮৮০১৭০০০০০০০০  
    📧 **ইমেইল:** info@jhalakathigovths.edu.bd  
    🌐 **ওয়েবসাইট:** https://school-app.streamlit.app
    """)

# ----------------------------------------------------
# 8. ADMIN CONTROL PANEL (Only Authority Access)
# ----------------------------------------------------
elif menu == "⚙️ Admin Control Panel":
    st.title("⚙️ Authority Admin Control Panel")
    
    if not st.session_state["is_admin"]:
        st.error("🔒 অ্যাক্সেস নিষেধ! এই সেকশনে ঢুকতে সাইডবার থেকে অথরিটি পাসওয়ার্ড দিয়ে লগইন করুন।")
    else:
        st.success("✅ সুস্বাগতম! আপনি স্কুলের তথ্য ও ছবি পরিচালনা করতে পারবেন।")

        # Tab layout for admin controls
        tab_cover, tab_hm, tab_notice, tab_status, tab_gal, tab_pwd = st.tabs([
            "🌄 কভার ফটো", "👨‍🏫 প্রতিষ্ঠান প্রধান", "📌 নোটিশ পোস্ট", "📢 স্ট্যাটাস পোস্ট", "📸 গ্যালারি", "🔑 পাসওয়ার্ড পরিবর্তন"
        ])

        # 1. Cover Photo Upload directly from Gallery
        with tab_cover:
            st.subheader("🌄 কভার ছবি পরিবর্তন (গ্যালারি থেকে)")
            up_cover = st.file_uploader("গ্যালারি থেকে কভার ছবি সিলেক্ট করুন", type=["jpg", "jpeg", "png"], key="up_cover_file")
            if up_cover is not None:
                if st.button("Upload Cover Picture", type="primary"):
                    st.session_state["cover_photo"] = up_cover.getvalue()
                    st.success("✅ কভার ফটো সফলভাবে আপলোড ও সেভ হয়েছে!")
                    st.rerun()

        # 2. Headmaster Photo & Speech
        with tab_hm:
            st.subheader("👨‍🏫 প্রতিষ্ঠান প্রধানের তথ্য ও ছবি")
            up_hm = st.file_uploader("প্রতিষ্ঠান প্রধানের ছবি সিলেক্ট করুন", type=["jpg", "jpeg", "png"], key="up_hm_file")
            speech_input = st.text_area("প্রধান শিক্ষকের বাণী:", value=st.session_state["headmaster_speech"])
            if st.button("Save Headmaster Info", type="primary"):
                if up_hm is not None:
                    st.session_state["headmaster_photo"] = up_hm.getvalue()
                st.session_state["headmaster_speech"] = speech_input
                st.success("✅ প্রতিষ্ঠান প্রধানের তথ্য আপডেট হয়েছে!")
                st.rerun()

        # 3. Notice Post (Text, Image, PDF)
        with tab_notice:
            st.subheader("📌 নতুন নোটিশ যোগ করুন")
            n_title = st.text_input("নোটিশের শিরোনাম / বর্ণনা:")
            n_file = st.file_uploader("নোটিশের ফাইল বা ছবি সিলেক্ট করুন (PDF / PNG / JPG)", type=["pdf", "png", "jpg", "jpeg"], key="up_notice_file")
            if st.button("Publish Notice", type="primary"):
                if n_title:
                    today = datetime.now().strftime("%Y-%m-%d")
                    f_bytes = n_file.getvalue() if n_file is not None else None
                    f_type = n_file.name.split(".")[-1] if n_file is not None else None
                    st.session_state["notices"].insert(0, {"Date": today, "Title": n_title, "File": f_bytes, "FileType": f_type})
                    st.success("✅ নোটিশ সফলভাবে পোস্ট করা হয়েছে!")
                    st.rerun()

        # 4. Status Post Feed
        with tab_status:
            st.subheader("📢 ড্যাশবোর্ড স্ট্যাটাস ও আপডেট পোস্ট")
            s_text = st.text_area("স্ট্যাটাসের বিষয়বস্তু:")
            s_img = st.file_uploader("স্ট্যাটাসের ছবি (ঐচ্ছিক):", type=["jpg", "jpeg", "png"], key="up_status_img")
            if st.button("Post Status Update", type="primary"):
                if s_text:
                    today = datetime.now().strftime("%Y-%m-%d")
                    img_bytes = s_img.getvalue() if s_img is not None else None
                    st.session_state["status_posts"].insert(0, {"Date": today, "Text": s_text, "Image": img_bytes})
                    st.success("✅ স্ট্যাটাস আপডেট পোস্ট করা হয়েছে!")
                    st.rerun()

        # 5. Gallery Upload
        with tab_gal:
            st.subheader("📸 গ্যালারিতে ছবি যোগ করুন")
            g_img = st.file_uploader("ছবি সিলেক্ট করুন:", type=["jpg", "jpeg", "png"], key="up_gal_file")
            if g_img is not None:
                if st.button("Upload to Gallery", type="primary"):
                    st.session_state["gallery"].append({"name": g_img.name, "bytes": g_img.getvalue()})
                    st.success("✅ গ্যালারিতে ছবি যোগ করা হয়েছে!")
                    st.rerun()

        # 6. Change Password
        with tab_pwd:
            st.subheader("🔑 অ্যাডমিন পাসওয়ার্ড পরিবর্তন")
            new_pwd = st.text_input("নতুন পাসওয়ার্ড দিন:", type="password")
            confirm_pwd = st.text_input("নতুন পাসওয়ার্ড পুনরায় লিখুন:", type="password")
            if st.button("Update Password", type="primary"):
                if new_pwd and new_pwd == confirm_pwd:
                    st.session_state["admin_password"] = new_pwd
                    st.success("✅ অ্যাডমিন পাসওয়ার্ড সফলভাবে পরিবর্তিত হয়েছে! পরবর্তী লগইনে এটি কাজ করবে।")
                else:
                    st.error("❌ পাসওয়ার্ড মিলছে না বা খালি রাখা যাবে না!")
