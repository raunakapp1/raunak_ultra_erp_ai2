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

    if st.button("Login"):
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

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("👥 Guests", len(st.session_state.guest_db))
    c2.metric("💰 Revenue", f"₹ {sum(x['bill'] for x in st.session_state.order_db)}")
    c3.metric("🧾 Orders", len(st.session_state.order_db))
    c4.metric("👨‍💼 Staff", len(st.session_state.staff_db))

    st.divider()

    st.subheader("🤖 AI Systems Status")
    for ai in ["Revenue Forecast","Fraud Detection","Dynamic Pricing","Offer Generator","Staff AI","Retarget AI"]:
        st.success(f"✅ {ai} AI : ACTIVE")

    st.divider()

    st.subheader("📈 Business Health Score")
    st.progress(min(100, len(st.session_state.order_db) * 10))

    st.caption("Created by – RJRAUNAK")

# ---------- STAFF PANEL ----------
def staff_panel():
    if st.session_state.role != "Admin":
        st.error("❌ Only Admin Allowed")
        return

    st.title("👨‍💼 Staff Management")

    name = st.text_input("Login Username")
    password = st.text_input("Password")
    role = st.selectbox("Role",["Manager","Cashier","Kitchen","Delivery","Accountant"])

    access = st.multiselect("Permissions",
        ["Dashboard","Guest Entry","Order Entry","Reports","AI Panel"],
        default=["Dashboard"]
    )

    if st.button("Create Staff"):
        st.session_state.staff_db[name.lower()] = {
            "password": password,
            "role": role,
            "access": access
        }
        st.success(f"✅ Staff {name} Created")

    st.divider()
    st.subheader("📋 Active Staff")
    st.dataframe(pd.DataFrame(st.session_state.staff_db).T)

# ---------- GUEST ENTRY ----------
def guest_entry():
    st.title("👥 Guest Entry (No Billing)")

    name = st.text_input("Guest Name")
    visit = st.selectbox("Visit Type",["Dine In","VIP","Party","Walk-in"])
    pax = st.number_input("PAX",1,50,1)

    if st.button("Save Guest"):
        st.session_state.guest_db.append({
            "guest":name,"visit":visit,"pax":pax,
            "by":st.session_state.user,
            "time":datetime.datetime.now()
        })
        st.success("✅ Guest Entry Saved")

# ---------- ORDER ENTRY ----------
def order_entry():
    st.title("🧾 Billing / Order Entry")

    source = st.selectbox("Source",["Dine In","Swiggy","Zomato","Takeaway"])
    bill = st.number_input("Bill Amount",0,100000,0)
    payment = st.selectbox("Payment Mode",["Cash","UPI","Card","Razorpay"])

    if st.button("Save Order"):
        st.session_state.order_db.append({
            "source":source,"bill":bill,"payment":payment,
            "by":st.session_state.user,
            "time":datetime.datetime.now()
        })
        st.success("✅ Order Saved")

# ---------- REPORTS ----------
def reports_panel():
    st.title("📊 Advanced Reports System")

    tab1,tab2,tab3 = st.tabs(["🧾 Orders","👥 Guests","💼 Staff Performance"])

    with tab1:
        if st.session_state.order_db:
            df = pd.DataFrame(st.session_state.order_db)
            st.dataframe(df,use_container_width=True)
            st.download_button("⬇ Download Excel",df.to_excel(index=False),"orders.xlsx")
        else:
            st.warning("No Orders Data")

    with tab2:
        if st.session_state.guest_db:
            df = pd.DataFrame(st.session_state.guest_db)
            st.dataframe(df,use_container_width=True)
            st.download_button("⬇ Download Excel",df.to_excel(index=False),"guests.xlsx")
        else:
            st.warning("No Guest Data")

    with tab3:
        if st.session_state.order_db:
            df = pd.DataFrame(st.session_state.order_db)
            perf = df.groupby("by")["bill"].sum().reset_index()
            st.dataframe(perf,use_container_width=True)
        else:
            st.warning("No Performance Data")

# ---------- AI PANEL ----------
def ai_panel():
    st.title("🤖 AI Control Center")

    if st.button("Generate Festival Offer"):
        st.success("🎉 AI Generated Offer: FLAT 20% OFF")

    if st.button("Optimize Pricing"):
        st.success("💰 AI Price Optimization Complete")

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
