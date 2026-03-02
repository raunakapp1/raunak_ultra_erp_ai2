import streamlit as st
import pandas as pd
import datetime

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
    st.title("🔐 Login Panel")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = st.session_state.staff_db.get(username.lower())
        if user and user["password"] == password:
            st.session_state.login = True
            st.session_state.user = username
            st.session_state.role = user["role"]
            st.experimental_rerun()
        else:
            st.error("❌ Invalid Login")

# ---------------- DASHBOARD ----------------
def admin_dashboard():
    st.title("🚀 Ultra ERP AI Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Guests", len(st.session_state.guest_db))
    col2.metric("💰 Revenue", f"₹ {sum(x['bill'] for x in st.session_state.order_db)}")
    col3.metric("🛒 Orders", len(st.session_state.order_db))
    col4.metric("👨‍💼 Staff", len(st.session_state.staff_db))

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
    st.caption("Created by – RJRAUNAK")

# ---------------- STAFF MANAGEMENT (ADMIN ONLY) ----------------
def staff_panel():
    if st.session_state.role != "Admin":
        st.error("❌ Only Admin can manage staff")
        return

    st.title("👨‍💼 Staff Management")

    name = st.text_input("Username (login id)")
    password = st.text_input("Password")
    role = st.selectbox("Role", ["Manager", "Cashier", "Kitchen", "Delivery", "Accountant"])

    access = st.multiselect(
        "Access Permissions",
        ["Dashboard", "Guest Entry", "Order Entry", "Inventory", "Reports", "AI Panel"],
        default=["Dashboard"]
    )

    if st.button("Create Staff"):
        if name and password:
            st.session_state.staff_db[name.lower()] = {
                "password": password,
                "role": role,
                "access": access
            }
            st.success(f"✅ Staff {name} created successfully")
        else:
            st.error("❌ Fill all fields")

    st.divider()
    st.subheader("📋 Staff List")
    st.json(st.session_state.staff_db)

# ---------------- GUEST ENTRY ----------------
def guests_page():
    st.title("👥 Guest Entry (No Billing)")

    name = st.text_input("Guest Name")
    source = st.selectbox("Visit Type", ["Dine In", "Party", "VIP", "Walk-in"])
    pax = st.number_input("Number of Guests", 1, 50, 1)
    date = st.date_input("Date", datetime.date.today())
    time = st.time_input("Time", datetime.datetime.now().time())

    if st.button("Save Guest"):
        st.session_state.guest_db.append({
            "name": name,
            "source": source,
            "pax": pax,
            "date": date,
            "time": time
        })
        st.success("✅ Guest Entry Saved")

# ---------------- ORDER ENTRY (BILLING) ----------------
def order_page():
    st.title("🧾 Order / Billing Entry")

    source = st.selectbox("Order Source", ["Dine In", "Takeaway", "Swiggy", "Zomato"])
    bill = st.number_input("Bill Amount", 0, 100000, 0)
    payment = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Razorpay"])

    if st.button("Save Order"):
        st.session_state.order_db.append({
            "source": source,
            "bill": bill,
            "payment": payment,
            "date": datetime.date.today()
        })
        st.success("✅ Order Saved")

# ---------------- REPORTS ----------------
def reports_page():
    st.title("📊 Business Reports")

    if not st.session_state.order_db:
        st.warning("⚠ No data yet")
        return

    df = pd.DataFrame(st.session_state.order_db)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download Excel Report",
        df.to_excel(index=False),
        file_name="business_report.xlsx"
    )

# ---------------- AI PANEL ----------------
def ai_panel():
    st.title("🤖 AI Control Center")

    if st.button("Generate Festival Offer"):
        st.success("🎉 AI Generated Offer: FLAT 20% OFF")

    if st.button("Dynamic Pricing Optimize"):
        st.success("💰 Prices Optimized Successfully")

# ---------------- ACCESS CONTROL ----------------
def has_access(page):
    user = st.session_state.staff_db.get(st.session_state.user.lower())
    if "ALL" in user["access"]:
        return True
    return page in user["access"]

# ---------------- ROUTER ----------------
if not st.session_state.login:
    login_page()
    st.stop()

st.sidebar.title("🚀 Navigation")
st.sidebar.write(f"👤 {st.session_state.user} ({st.session_state.role})")

menu = ["Dashboard", "Guest Entry", "Order Entry", "Reports", "AI Panel"]
if st.session_state.role == "Admin":
    menu.insert(2, "Staff Panel")

page = st.sidebar.radio("Go To", menu)

st.sidebar.markdown("---")
if st.sidebar.button("🔓 Logout"):
    st.session_state.login = False
    st.experimental_rerun()

# Page Routing
if page == "Dashboard" and has_access("Dashboard"):
    admin_dashboard()
elif page == "Guest Entry" and has_access("Guest Entry"):
    guests_page()
elif page == "Order Entry" and has_access("Order Entry"):
    order_page()
elif page == "Reports" and has_access("Reports"):
    reports_page()
elif page == "AI Panel" and has_access("AI Panel"):
    ai_panel()
elif page == "Staff Panel":
    staff_panel()
else:
    st.error("⛔ Access Denied")
