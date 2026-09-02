import streamlit as st
import pandas as pd
import os

# ==========================================
# 🏫 School Information Setup
# ==========================================
SCHOOL_NAME_EN = "Jhalakathi Govt High School"
SCHOOL_NAME_BN = "ঝালকাঠি সরকারি উচ্চ বিদ্যালয়"
SCHOOL_LOGO_ICON = "🏫"

# Page Configuration
st.set_page_config(page_title=SCHOOL_NAME_BN, page_icon=SCHOOL_LOGO_ICON, layout="wide")

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

# Navigation Menu (All Options in English)
st.sidebar.title(f"{SCHOOL_LOGO_ICON} Navigation")
menu = st.sidebar.radio("Select Menu", ["Home", "Student ID Portal", "Class Schedule", "Fee Payment"])

# 1. HOME PAGE
if menu == "Home":
    # 🏃‍♂️ Moving Animated Banner (English Name moving Left to Right)
    st.markdown(f"""
        <div style="width: 100%; overflow: hidden; background-color: #0f172a; color: #38bdf8; padding: 12px; border-radius: 8px; margin-bottom: 20px; font-size: 20px; font-weight: bold; border: 1px solid #0284c7;">
            <marquee behavior="scroll" direction="right" scrollamount="8">
                🎓 Welcome to {SCHOOL_NAME_EN} 🎓 Welcome to {SCHOOL_NAME_EN}
            </marquee>
        </div>
    """, unsafe_allow_html=True)

    # Main Title in Bangla
    st.title(f"{SCHOOL_LOGO_ICON} {SCHOOL_NAME_BN}")
    st.caption(f"English: {SCHOOL_NAME_EN}")
    st.write("Welcome to the official online portal!")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        total_std = len(df_students) if df_students is not None else "File not uploaded yet"
        st.metric("Total Students Enrolled", total_std)
    with col2:
        st.metric("Active Payment Gateways", "bKash, Nagad, Rocket, Upay")

# 2. STUDENT ID PORTAL
elif menu == "Student ID Portal":
    st.title(f"🆔 {SCHOOL_NAME_BN}")
    st.subheader("Student ID Search")
    
    if df_students is None:
        st.warning("⚠️ 'students.xlsx' file has not been uploaded yet. Search will work automatically once uploaded.")
    else:
        search_id = st.text_input("Enter Student ID Number:", placeholder="e.g. 1001")
        
        if search_id:
            res = df_students[df_students['student_id'] == search_id.strip()]
            
            if not res.empty:
                info = res.iloc[0]
                st.success(f"Student Found: {info.get('name', 'N/A')}")
                
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

# 3. CLASS SCHEDULE
elif menu == "Class Schedule":
    st.title(f"📅 {SCHOOL_NAME_BN}")
    st.subheader("Class Routine")
    cls = st.selectbox("Select Class:", list(ROUTINE.keys()))
    if cls in ROUTINE:
        st.table(pd.DataFrame(ROUTINE[cls]))

# 4. FEE PAYMENT GATEWAY
elif menu == "Fee Payment":
    st.title(f"💳 {SCHOOL_NAME_BN}")
    st.subheader("Fee Payment Portal")
    
    with st.form("pay_form"):
        c1, c2 = st.columns(2)
        with c1:
            s_id = st.text_input("Student ID")
            fee_cat = st.selectbox("Fee Type", ["Monthly Tuition Fee", "Exam Fee", "Admission Fee"])
            amt = st.number_input("Amount (BDT)", min_value=100, value=1500)
        with c2:
            gateway = st.selectbox("Payment Gateway", ["bKash", "Nagad", "Rocket", "Upay"])
            phone = st.text_input("Sender Mobile Number")
            trx = st.text_input("Transaction ID (TrxID)")
            
        btn = st.form_submit_button("Complete Payment")
        if btn:
            if s_id and phone and trx:
                st.success(f"✅ BDT {amt} paid via {gateway} for Student ID {s_id}. TrxID: {trx}")
                st.balloons()
            else:
                st.error("Please fill in all required fields!")
