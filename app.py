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
ADMIN_PASSWORD = "admin123"  # 🔑 কর্তৃপক্ষের গোপন পাসওয়ার্ড

st.set_page_config(page_title=SCHOOL_NAME_BN, page_icon=SCHOOL_LOGO_ICON, layout="wide")

# Session State Initialization
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

if "notices" not in st.session_state:
    st.session_state["notices"] = [
        {"Date": "2026-03-01", "Title": "Annual Sports Competition Registration Open"},
        {"Date": "2026-02-25", "Title": "First Term Examination Schedule Released"},
        {"Date": "2026-02-15", "Title": "Parent-Teacher Meeting for Class 9 & 10"}
    ]

if "gallery" not in st.session_state:
    st.session_state["gallery"] = []

# Excel Loader Function
@st.cache_data
def load_student_data():
    file_path = "students.xlsx"
    if os.path.exists(file_path):
        return pd.read_excel(file_path, dtype={'student_id': str})
    return None

df_students = load_student_data()

# Routine Data Setup
ROUTINE = {
    "Class 10": [
        {"Period": "1st (09:00 AM)", "Sunday": "Math", "Monday": "Bangla", "Tuesday": "Physics"},
        {"Period": "2nd (09:45 AM)", "Sunday": "English", "Monday": "Chemistry", "Tuesday": "Math"},
        {"Period": "3rd (10:30 AM)", "Sunday": "ICT", "Monday": "English", "Tuesday": "Biology"}
    ],
    "Class 9": [
        {"Period": "1st (09:00 AM)", "Sunday": "English", "Monday": "Math", "Tuesday": "Bangla"},
        {"Period": "2nd (09:45 AM)", "Sunday": "Physics", "Monday": "ICT", "Tuesday": "Chemistry"}
    ]
}

# Dummy Teachers Data
TEACHERS = [
    {"Name": "Md. Rafiqul Islam", "Designation": "Headmaster", "Subject": "Administration", "Phone": "+8801700000001"},
    {"Name": "Anisur Rahman", "Designation": "Assistant Headmaster", "Subject": "Mathematics", "Phone": "+8801700000002"},
    {"Name": "Nasrin Sultana", "Designation": "Senior Teacher", "Subject": "English", "Phone": "+8801700000003"},
    {"Name": "Tanvir Ahmed", "Designation": "Lecturer", "Subject": "ICT", "Phone": "+8801700000004"}
]

# Navigation Menu
st.sidebar.title(f"{SCHOOL_LOGO_ICON} Navigation")
menu = st.sidebar.radio(
    "Select Option", 
    ["Home & Dashboard", "Student ID Portal", "Class Schedule", "Fee Payment Gateway", "Teachers Directory", "Photo Gallery", "Admin Control Panel"]
)

# Sidebar Admin Login Panel
st.sidebar.divider()
st.sidebar.subheader("🔒 Admin Login")
if not st.session_state["is_admin"]:
    pwd_input = st.sidebar.text_input("Enter Admin Password", type="password")
    if st.sidebar.button("Login as Admin"):
        if pwd_input == ADMIN_PASSWORD:
            st.session_state["is_admin"] = True
            st.sidebar.success("Logged in successfully!")
            st.rerun()
        else:
            st.sidebar.error("Incorrect password!")
else:
    st.sidebar.success("✅ Logged in as Authority")
    if st.sidebar.button("Logout"):
        st.session_state["is_admin"] = False
        st.rerun()

# ----------------------------------------------------
# 1. HOME & DASHBOARD
# ----------------------------------------------------
if menu == "Home & Dashboard":
    st.markdown(f"""
        <div style="width: 100%; overflow: hidden; background-color: #0f172a; color: #38bdf8; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 20px; font-weight: bold; border: 1px solid #0284c7;">
            <marquee behavior="scroll" direction="right" scrollamount="8">
                🎓 Welcome to {SCHOOL_NAME_EN} 🎓 Welcome to {SCHOOL_NAME_EN}
            </marquee>
        </div>
    """, unsafe_allow_html=True)

    if "cover_photo" in st.session_state:
        st.image(st.session_state["cover_photo"], use_container_width=True)
    else:
        st.info("🖼️ Cover Photo Not Set. (Authority can set it from 'Admin Control Panel')")

    st.title(f"{SCHOOL_LOGO_ICON} {SCHOOL_NAME_BN}")
    st.caption(f"English Name: {SCHOOL_NAME_EN}")
    st.write("Welcome to the official digital portal of Jhalakathi Govt High School.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        total_std = len(df_students) if df_students is not None else "File Pending"
        st.metric("Total Students", total_std)
    with col2:
        st.metric("Total Teachers", len(TEACHERS))
    with col3:
        st.metric("Online Payment", "Active (bKash/Nagad)")

    st.subheader("📌 School Notice Board")
    for notice in st.session_state["notices"]:
        st.info(f"**[{notice['Date']}]** - {notice['Title']}")

# ----------------------------------------------------
# 2. STUDENT ID PORTAL
# ----------------------------------------------------
elif menu == "Student ID Portal":
    st.title(f"🆔 {SCHOOL_NAME_BN}")
    st.subheader("Student ID Verification Portal")
    
    if df_students is None:
        st.warning("⚠️ 'students.xlsx' file has not been uploaded yet. Search will work once uploaded.")
    else:
        search_id = st.text_input("Enter Student ID Number:", placeholder="e.g. 1001")
        
        if search_id:
            res = df_students[df_students['student_id'] == search_id.strip()]
            
            if not res.empty:
                info = res.iloc[0]
                st.success(f"Student Profile Found: {info.get('name', 'N/A')}")
                
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.info(f"**ID:** {info.get('student_id')}\n\n**Blood Group:** {info.get('blood_group', 'N/A')}\n\n**Status:** {info.get('status', 'Active')}")
                with c2:
                    st.table(pd.DataFrame({
                        "Field": ["Full Name", "Class", "Section", "Roll No", "Father's Name", "Mother's Name", "Phone"],
                        "Details": [
                            info.get('name', ''),
                            info.get('class', ''),
                            info.get('section', ''),
                            info.get('roll', ''),
                            info.get('father_name', ''),
                            info.get('mother_name', ''),
                            info.get('phone', '')
                        ]
                    }))
            else:
                st.error("No student record found with this ID!")

# ----------------------------------------------------
# 3. CLASS SCHEDULE
# ----------------------------------------------------
elif menu == "Class Schedule":
    st.title(f"📅 {SCHOOL_NAME_BN}")
    st.subheader("Academic Class Routine")
    cls = st.selectbox("Select Class:", list(ROUTINE.keys()))
    if cls in ROUTINE:
        st.table(pd.DataFrame(ROUTINE[cls]))

# ----------------------------------------------------
# 4. FEE PAYMENT GATEWAY & VOUCHER GENERATOR
# ----------------------------------------------------
elif menu == "Fee Payment Gateway":
    st.title(f"💳 {SCHOOL_NAME_BN}")
    st.subheader("Digital Fee Payment & Payment Receipt Generator")

    c1, c2 = st.columns(2)
    with c1:
        s_id = st.text_input("Student ID Number")
        student_name = st.text_input("Student Full Name")
        fee_cat = st.selectbox("Select Fee Category", ["Monthly Tuition Fee", "Exam Fee", "Admission Fee", "Session Fee"])
        amt = st.number_input("Amount (BDT)", min_value=100, value=1500, step=100)

    with c2:
        gateway = st.radio("Select Payment Method", ["🔴 bKash", "🟠 Nagad", "🚀 Rocket", "🟣 Upay"])
        account_no = st.text_input("Sender Mobile Account Number")
        trx_id = st.text_input("Transaction ID (TrxID)")

    if st.button("🚀 Confirm Payment & Generate Receipt"):
        if s_id and student_name and account_no and trx_id:
            st.success("✅ Payment Processed Successfully!")
            st.balloons()

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            receipt_text = f"""
            =================================================
                       {SCHOOL_NAME_BN}
                   OFFICIAL PAYMENT RECEIPT / VOUCHER
            =================================================
            Date & Time     : {now}
            Student ID      : {s_id}
            Student Name    : {student_name}
            Fee Type        : {fee_cat}
            Amount Paid     : BDT {amt}
            Payment Gateway : {gateway}
            Sender Account  : {account_no}
            Transaction ID  : {trx_id}
            Payment Status  : COMPLETED & VERIFIED
            =================================================
            Thank you for paying fees digitally!
            """
            
            st.subheader("🧾 Payment Receipt (Voucher)")
            st.code(receipt_text)
            
            st.download_button(
                label="📥 Download Money Receipt (Voucher)",
                data=receipt_text,
                file_name=f"Money_Receipt_{s_id}_{trx_id}.txt",
                mime="text/plain"
            )
        else:
            st.error("Please fill in all payment details (Student ID, Name, Account Number & TrxID)!")

# ----------------------------------------------------
# 5. TEACHERS DIRECTORY
# ----------------------------------------------------
elif menu == "Teachers Directory":
    st.title(f"👨‍🏫 {SCHOOL_NAME_BN}")
    st.subheader("Teachers & Administration Directory")
    st.table(pd.DataFrame(TEACHERS))

# ----------------------------------------------------
# 6. PHOTO GALLERY (Public View & Download Only)
# ----------------------------------------------------
elif menu == "Photo Gallery":
    st.title(f"🖼️ {SCHOOL_NAME_BN}")
    st.subheader("School Photo Gallery")

    if len(st.session_state["gallery"]) > 0:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state["gallery"]):
            with cols[idx % 3]:
                st.image(item["bytes"], caption=item["name"], use_container_width=True)
                st.download_button(
                    label="📥 Download Photo",
                    data=item["bytes"],
                    file_name=item["name"],
                    mime="image/png",
                    key=f"dl_{idx}"
                )
    else:
        st.info("No photos uploaded in the gallery yet. (Authority can upload photos from Admin Control Panel)")

# ----------------------------------------------------
# 7. ADMIN CONTROL PANEL (Only Authorized Access)
# ----------------------------------------------------
elif menu == "Admin Control Panel":
    st.title(f"⚙️ {SCHOOL_NAME_BN} - Admin Control Panel")
    
    if not st.session_state["is_admin"]:
        st.error("🔒 Access Denied! You must login with Admin Password from sidebar to access this section.")
    else:
        st.success("✅ Welcome Admin! You can now manage notices, cover photos, and gallery images.")
        
        # 1. Update Cover Photo
        st.subheader("🌄 Change Homepage Cover Photo")
        uploaded_cover = st.file_uploader("Upload New Cover Image", type=["jpg", "jpeg", "png"], key="cover_up")
        if uploaded_cover is not None:
            st.session_state["cover_photo"] = uploaded_cover.getvalue()
            st.success("✅ Cover Photo updated successfully!")

        st.divider()

        # 2. Add New Notice
        st.subheader("📌 Post New Notice")
        notice_title = st.text_input("Notice Title/Content")
        if st.button("Post Notice"):
            if notice_title:
                today = datetime.now().strftime("%Y-%m-%d")
                st.session_state["notices"].insert(0, {"Date": today, "Title": notice_title})
                st.success("✅ New Notice Posted Successfully!")
                st.rerun()
            else:
                st.error("Please enter notice text!")

        st.divider()

        # 3. Upload to Photo Gallery
        st.subheader("📸 Upload Photos to Public Gallery")
        uploaded_pic = st.file_uploader("Upload Photos to Gallery", type=["jpg", "jpeg", "png"], key="gal_up")
        if uploaded_pic is not None:
            if st.button("Add to Gallery"):
                st.session_state["gallery"].append({"name": uploaded_pic.name, "bytes": uploaded_pic.getvalue()})
                st.success(f"Uploaded {uploaded_pic.name} to Gallery!")
                st.rerun()
