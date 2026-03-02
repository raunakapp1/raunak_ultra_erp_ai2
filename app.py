import streamlit as st
import pandas as pd
import datetime
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Raunak Ultra ERP AI", layout="wide")

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = None

# ---------------- LOGIN ----------------
def login_page():
    st.title("🔐 Login Panel")

    users = {
        "Admin": "1234",
        "Manager": "1111",
        "Cashier": "2222",
        "Accountant": "3333",
        "Kitchen": "4444",
        "Delivery": "5555"
    }

    role = st.selectbox("Select Role", list(users.keys()))
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == users[role]:
            st.session_state.login = True
            st.session_state.role = role
            st.experimental_rerun()
        else:
            st.error("❌ Wrong Password")

# ---------------- DASHBOARD ----------------
def admin_dashboard():
    st.title("🚀 Ultra ERP AI Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Guests", random.randint(50,200))
    col2.metric("💰 Revenue", f"₹ {random.randint(15000,70000)}")
    col3.metric("🛒 Orders", random.randint(100,600))
    col4.metric("🚨 Fraud Alerts", random.randint(0,3))

    st.divider()

    st.subheader("🤖 AI Modules Status")
    ai_list = [
        "Revenue Forecast AI",
        "Fraud Detection AI",
        "Dynamic Pricing AI",
        "Offer Generator AI",
        "Staff Performance AI",
        "Customer Retargeting AI"
    ]

    for ai in ai_list:
        st.success(f"✅ {ai} : READY")

    st.divider()

    st.subheader("📈 Tomorrow Business Prediction")
    prediction = random.randint(30000,90000)
    st.metric("Tomorrow Revenue Forecast", f"₹ {prediction}")

# ---------------- GUEST ENTRY ----------------
def guests_page():
    st.title("👥 Guest / Order Entry")

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox("Order Source", ["Dine In", "Takeaway", "Swiggy", "Zomato", "Easy Dinner", "Party", "VIP"])
        pax = st.number_input("Number of Guests", 1, 50, 1)
        bill = st.number_input("Bill Amount", 0, 100000, 0)
        pay_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Razorpay"])

    with col2:
        date = st.date_input("Date", datetime.date.today())
        time = st.time_input("Time", datetime.datetime.now().time())

    if st.button("Save Entry"):
        st.success("✅ Guest Entry Saved Successfully")

# ---------------- STAFF PANEL ----------------
def staff_panel():
    st.title("👨‍💼 Staff Management")

    name = st.text_input("Staff Name")
    mobile = st.text_input("Mobile")
    role = st.selectbox("Role", ["Manager", "Cashier", "Kitchen", "Delivery", "Accountant"])
    salary = st.number_input("Salary", 0, 100000, 0)

    if st.button("Create Staff"):
        if name and mobile:
            st.success(f"✅ Staff {name} Created Successfully")
        else:
            st.error("❌ Fill all required fields")

# ---------------- INVENTORY ----------------
def inventory_page():
    st.title("📦 Inventory Management")

    item = st.text_input("Item Name")
    qty = st.number_input("Quantity", 1, 1000, 1)
    price = st.number_input("Unit Cost", 0, 10000, 0)

    if st.button("Add Stock"):
        st.success("✅ Stock Added")

# ---------------- REPORTS ----------------
def reports_page():
    st.title("📊 Reports")

    df = pd.DataFrame({
        "Date": pd.date_range(start="2025-01-01", periods=10),
        "Revenue": [random.randint(10000,80000) for _ in range(10)]
    })

    st.dataframe(df, use_container_width=True)

    st.download_button("⬇ Download Excel", df.to_excel(index=False), file_name="report.xlsx")

# ---------------- AI PANEL ----------------
def ai_panel():
    st.title("🤖 AI Control Center")

    st.success("🔥 All AI Systems Running")

    if st.button("Generate Festival Offer"):
        st.success("🎉 AI Offer Generated: FLAT 20% OFF")

    if st.button("Dynamic Price Optimize"):
        st.success("💰 Price Optimized Successfully")

# ---------------- MAIN ROUTER ----------------
if not st.session_state.login:
    login_page()
    st.stop()

st.sidebar.title("🚀 Navigation")
page = st.sidebar.radio("Go To", [
    "Dashboard",
    "Guest Entry",
    "Staff Panel",
    "Inventory",
    "Reports",
    "AI Control"
])

st.sidebar.markdown("---")

if st.sidebar.button("🔓 Logout"):
    st.session_state.login = False
    st.experimental_rerun()

# Page Routing
if page == "Dashboard":
    admin_dashboard()
elif page == "Guest Entry":
    guests_page()
elif page == "Staff Panel":
    staff_panel()
elif page == "Inventory":
    inventory_page()
elif page == "Reports":
    reports_page()
elif page == "AI Control":
    ai_panel()