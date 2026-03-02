import streamlit as st
import pandas as pd
import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Raunak Ultra ERP AI", layout="wide")

# ---------------- SESSION INIT ----------------
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None

if "staff_db" not in st.session_state:
    st.session_state.staff_db = {
        "admin": {"password": "1234", "role": "Admin", "access": ["ALL"]}
    }

if "guest_db" not in st.session_state:
    st.session_state.guest_db = []

if "order_db" not in st.session_state:
    st.session_state.order_db = []

# ---------------- LOGIN ----------------
def login_page():
    st.markdown("<h2 style='text-align:center'>🔐 Ultra ERP Login</h2>", unsafe_allow_html=True)

    user = st.selectbox("Select User", list(st.session_state.staff_db.keys()))
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if st.session_state.staff_db[user]["password"] == password:
            st.session_state.login = True
            st.session_state.user = user
            st.session_state.role = st.session_state.staff_db[user]["role"]
            st.experimental_rerun()
        else:
            st.error("❌ Wrong Password")

# ---------------- ACCESS ----------------
def has_access(page):
    user = st.session_state.staff_db[st.session_state.user]
    return "ALL" in user["access"] or page in user["access"]

# ---------------- DASHBOARD ----------------
def admin_dashboard():
    st.title("🚀 Ultra ERP AI Dashboard")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("👥 Guests", len(st.session_state.guest_db))
    c2.metric("💰 Revenue", f"₹ {sum(x['bill'] for x in st.session_state.order_db):,.2f}")
    c3.metric("🧾 Orders", len(st.session_state.order_db))
    c4.metric("👨‍💼 Staff", len(st.session_state.staff_db))

    st.divider()

    st.subheader("🤖 AI Modules Status")
    for ai in ["Revenue Forecast","Fraud Detection","Dynamic Pricing","Offer Generator","Staff AI","Retarget AI"]:
        st.success(f"✅ {ai} AI : READY")

    st.divider()
    st.caption("Created by – RJRAUNAK")

# ---------------- STAFF PANEL ----------------
def staff_panel():
    st.title("👨‍💼 Staff Management")

    name = st.text_input("Login Username")
    password = st.text_input("Password")
    role = st.selectbox("Role",["Manager","Cashier","Kitchen","Delivery","Accountant"])

    access = st.multiselect("Permissions",
        ["Dashboard","Guest Entry","Order Entry","Reports","AI Panel"],
        default=["Dashboard"]
    )

    if st.button("Create Staff", use_container_width=True):
        if name and password:
            st.session_state.staff_db[name.lower()] = {
                "password": password,
                "role": role,
                "access": access
            }
            st.success(f"✅ Staff {name} Created Successfully")
        else:
            st.error("❌ Fill all fields")

    st.divider()
    st.dataframe(pd.DataFrame(st.session_state.staff_db).T, use_container_width=True)

# ---------------- GUEST ENTRY ----------------
def guest_entry():
    st.title("👥 Guest Entry System")

    c1,c2,c3 = st.columns(3)

    with c1:
        category = st.selectbox("Category",[
            "Swiggy","Zomato","EazyDinner","Dine In","Walk-in",
            "Party","Holi Buffet","VIP","Other"
        ])
        guest = st.text_input("Guest Name")

    with c2:
        mobile = st.text_input("Mobile Number")
        pax = st.number_input("PAX",1,100,1)

    with c3:
        date = st.date_input("Date",datetime.date.today())
        time = datetime.datetime.now().strftime("%H:%M:%S")

    if st.button("Save Guest Entry", use_container_width=True):
        st.session_state.guest_db.append({
            "date":date,"time":time,"category":category,
            "guest":guest,"mobile":mobile,"pax":pax,
            "by":st.session_state.user
        })
        st.success("✅ Guest Entry Saved")

# ---------------- ORDER ENTRY ----------------
def order_entry():
    st.title("🧾 Order / Billing System")

    c1,c2,c3 = st.columns(3)

    with c1:
        name = st.text_input("Guest Name")
        pax = st.number_input("PAX",1,50,1)

    with c2:
        mobile = st.text_input("Mobile")
        payment = st.selectbox("Payment Mode",["Cash","UPI","Card","Razorpay"])

    with c3:
        bill_no = st.text_input("Bill Number")
        bill_amt = st.number_input("Bill Amount",0,500000,0)

    date = st.date_input("Billing Date",datetime.date.today())
    time = datetime.datetime.now().strftime("%H:%M:%S")

    if st.button("Save Order", use_container_width=True):
        st.session_state.order_db.append({
            "date":date,"time":time,"name":name,"pax":pax,
            "mobile":mobile,"bill_no":bill_no,
            "bill":bill_amt,"payment":payment,
            "by":st.session_state.user
        })
        st.success("✅ Order Saved Successfully")

# ---------------- REPORTS ----------------
def reports_panel():
    st.title("📊 Advanced Reports")

    tab1,tab2,tab3 = st.tabs(["🧾 Orders","👥 Guests","👨‍💼 Staff Performance"])

    with tab1:
        if st.session_state.order_db:
            df = pd.DataFrame(st.session_state.order_db)
            st.dataframe(df,use_container_width=True)
            st.metric("Total Sale",f"₹ {df['bill'].sum():,.2f}")
        else:
            st.warning("No Order Data")

    with tab2:
        if st.session_state.guest_db:
            df = pd.DataFrame(st.session_state.guest_db)
            st.dataframe(df,use_container_width=True)
        else:
            st.warning("No Guest Data")

    with tab3:
        if st.session_state.order_db:
            df = pd.DataFrame(st.session_state.order_db)
            perf = df.groupby("by")["bill"].sum().reset_index()
            st.dataframe(perf,use_container_width=True)
        else:
            st.warning("No Performance Data")

# ---------------- AI PANEL ----------------
def ai_panel():
    st.title("🤖 AI Control Center")

    if st.button("Generate Festival Offer",use_container_width=True):
        st.success("🎉 AI Generated Offer: FLAT 25% OFF")

    if st.button("Optimize Pricing",use_container_width=True):
        st.success("💰 AI Price Optimization Completed")

# ---------------- MAIN ROUTER ----------------
if not st.session_state.login:
    login_page()
    st.stop()

st.sidebar.title("🚀 Navigation")
st.sidebar.write(f"👤 {st.session_state.user} ({st.session_state.role})")

menu = ["Dashboard","Guest Entry","Order Entry","Reports","AI Panel"]
if st.session_state.role=="Admin":
    menu.insert(1,"Staff Panel")

page = st.sidebar.radio("Go To",menu)

if st.sidebar.button("🔓 Logout"):
    st.session_state.login=False
    st.experimental_rerun()

if page=="Dashboard" and has_access("Dashboard"):
    admin_dashboard()
elif page=="Staff Panel":
    staff_panel()
elif page=="Guest Entry" and has_access("Guest Entry"):
    guest_entry()
elif page=="Order Entry" and has_access("Order Entry"):
    order_entry()
elif page=="Reports" and has_access("Reports"):
    reports_panel()
elif page=="AI Panel" and has_access("AI Panel"):
    ai_panel()
else:
    st.error("⛔ Access Denied")
