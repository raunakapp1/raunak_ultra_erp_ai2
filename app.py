import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Raunak Ultra ERP AI", layout="wide")

# ---------- SESSION ----------
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

# ---------- LOGIN ----------
def login_page():
    st.markdown("<h2 style='text-align:center'>🔐 Ultra ERP Login</h2>", unsafe_allow_html=True)
    staff_names = list(st.session_state.staff_db.keys())
    user = st.selectbox("Select User", staff_names)
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if st.session_state.staff_db[user]["password"] == password:
            st.session_state.login = True
            st.session_state.user = user
            st.session_state.role = st.session_state.staff_db[user]["role"]
            st.experimental_rerun()
        else:
            st.error("❌ Wrong Password")

# ---------- ACCESS ----------
def has_access(page):
    user = st.session_state.staff_db[st.session_state.user]
    return "ALL" in user["access"] or page in user["access"]

# ---------- DASHBOARD ----------
def admin_dashboard():
    st.title("🚀 Ultra ERP AI Dashboard")

    total_rev = sum(x['bill'] for x in st.session_state.order_db)
    total_orders = len(st.session_state.order_db)
    total_guests = len(st.session_state.guest_db)
    avg_bill = round(total_rev / total_orders,2) if total_orders else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("👥 Guests", total_guests)
    c2.metric("🧾 Orders", total_orders)
    c3.metric("💰 Revenue", f"₹ {total_rev:,.2f}")
    c4.metric("📊 Avg Bill", f"₹ {avg_bill}")
    c5.metric("👨‍💼 Staff", len(st.session_state.staff_db))

    st.progress(min(100, total_orders*3))

    st.divider()

    if st.session_state.order_db:
        df = pd.DataFrame(st.session_state.order_db)
        peak_hour = df['time'].str[:2].value_counts().idxmax()
        top_staff = df.groupby("by")["bill"].sum().idxmax()

        c6,c7 = st.columns(2)
        c6.metric("🔥 Peak Hour", f"{peak_hour}:00")
        c7.metric("🏆 Top Staff", top_staff)

    st.caption("Created by – RJRAUNAK")

# ---------- STAFF PANEL ----------
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
        st.session_state.staff_db[name.lower()] = {
            "password": password,
            "role": role,
            "access": access
        }
        st.success(f"✅ Staff {name} Created")

    st.divider()
    st.dataframe(pd.DataFrame(st.session_state.staff_db).T, use_container_width=True)

# ---------- GUEST ENTRY ----------
def guest_entry():
    st.title("👥 Guest Entry — Ultra Advanced")

    c1,c2,c3 = st.columns(3)

    with c1:
        category = st.selectbox("Category",[
            "Swiggy","Zomato","EazyDinner","Dine In","Walk-in",
            "Party","Holi Buffet","VIP","Other"
        ])
        guest = st.text_input("Guest Name")

    with c2:
        mobile = st.text_input("Mobile Number")
        pax = st.number_input("Number of PAX",1,100,1)

    with c3:
        date = st.date_input("Visit Date",datetime.date.today())
        time = datetime.datetime.now().strftime("%H:%M:%S")

    if st.button("Save Guest Entry", use_container_width=True):
        st.session_state.guest_db.append({
            "date":date,"time":time,"category":category,
            "guest":guest,"mobile":mobile,"pax":pax,
            "by":st.session_state.user
        })
        st.success("✅ Guest Entry Saved")

# ---------- ORDER ENTRY ----------
def order_entry():
    st.title("🧾 Order Entry — Ultra Billing System")

    c1,c2,c3 = st.columns(3)

    with c1:
        name = st.text_input("Guest Name")
        pax = st.number_input("PAX",1,50,1)

    with c2:
        mobile = st.text_input("Mobile Number")
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

# ---------- REPORTS ----------
def reports_panel():
    st.title("📊 Ultra Advanced Reports")

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
            st.warning("No Staff Performance Data")

# ---------- AI PANEL ----------
def ai_panel():
    st.title("🤖 AI Control Center")

    c1,c2,c3 = st.columns(3)

    with c1:
        if st.button("🎯 Generate Festival Offer",use_container_width=True):
            st.success("🎉 AI Generated Offer: FLAT 25% OFF")

    with c2:
        if st.button("💰 Optimize Pricing",use_container_width=True):
            st.success("Price Optimization Completed")

    with c3:
        if st.button("📊 Forecast Tomorrow Sale",use_container_width=True):
            st.success("Tomorrow Sale Prediction: ₹ 75,000")

# ---------- MAIN ----------
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
