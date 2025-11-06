import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# ===================== PAGE CONFIG ======================
st.set_page_config(page_title="LifeLink Emergency Locator", layout="wide")

# ===================== CUSTOM UI STYLING ======================
page_bg = """
<style>

[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1584483766114-2cea6facdf57?q=80&w=1920&auto=format');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stAppViewContainer"]:before {
    content: "";
    position: fixed;
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(3px);
    z-index: -1;
}

[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.85) !important;
    border-right: 2px solid rgba(255,0,0,0.3);
}

h1, h2, h3, h4, label, p, .stMarkdown {
    color: #ffffff !important;
    font-family: 'Arial', sans-serif;
}

.card {
    backdrop-filter: blur(8px);
    background: rgba(15,15,15,0.65);
    border-radius: 14px;
    padding: 25px;
    margin-top: 15px;
    border: 1px solid rgba(255,255,255,0.2);
}

.stButton>button {
    background: linear-gradient(90deg, #ff1e1e, #b60000);
    color: white;
    padding: 12px 24px;
    border: none;
    font-weight: bold;
    border-radius: 10px;
    transition: 0.25s;
    font-size: 18px;
}
.stButton>button:hover {
    transform: scale(1.07);
    background: linear-gradient(90deg, #b60000, #ff1e1e);
}

div.row-widget.stRadio > div{
    color: white !important;
    font-size: 18px !important;
}

.footer-text {
    text-align: center;
    color: #ddd;
    margin-top: 40px;
    font-size: 14px;
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ===================== SIDEBAR NAVIGATION ======================
st.sidebar.title("Navigate")
page = st.sidebar.radio("",
                        ["🏠 Home", "🏥 Hospital Locator",
                         "🩹 First-Aid Guide", "👤 Medical Profile"])

# ===================== HOME PAGE ======================
if page == "🏠 Home":
    st.markdown("<h1>🚨 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
    st.markdown("### Helping people reach medical help faster ❤️‍🩹")

    st.markdown("---")
    st.subheader("Quick Emergency Access")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❤️ Heart Attack"):
            st.warning("Call 108 immediately! 🚑 Provide aspirin if available.")
    with col2:
        if st.button("🧠 Stroke"):
            st.warning("FAST Test: Face drooping, Arm weakness, Speech trouble!")
    with col3:
        if st.button("🚑 Accident"):
            st.warning("Check breathing + bleeding. Do not move injured unless necessary.")

    st.markdown("### 📞 Emergency Numbers in India:")
    st.info("🚑 Ambulance: 108 | 👮 Police: 100 | 🔥 Fire: 101")

# ===================== HOSPITAL LOCATOR ======================
elif page == "🏥 Hospital Locator":

    st.header("🏥 Find Nearest Hospitals")

    user_location = st.text_input("Enter your location 🔍 (Example: Mumbai, Pune, Delhi)")

    if st.button("Search Hospital"):
        if user_location.strip() == "":
            st.error("Please enter a valid location.")
        else:
            geolocator = Nominatim(user_agent="lifelink-app")
            loc = geolocator.geocode(user_location)

            if loc:
                m = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=13)
                folium.Marker([loc.latitude, loc.longitude],
                              tooltip="You are here",
                              icon=folium.Icon(color='red')).add_to(m)

                st.success(f"Location found ✅: {loc.address}")

                st_folium(m, height=450, width=900)
            else:
                st.error("Location not found. Try a different city or spelling!")

# ===================== FIRST-AID GUIDE ======================
elif page == "🩹 First-Aid Guide":
    st.header("🩹 First Aid Steps for Common Emergencies")

    with st.expander("❤️ CPR (Cardiac Arrest)"):
        st.write("""
        ✅ Check response  
        ✅ Call 108  
        ✅ Push hard + fast in chest center  
        ✅ 100-120 compressions/min  
        ✅ Keep going until help arrives
        """)

    with st.expander("🚑 Severe Bleeding"):
        st.write("""
        ✅ Apply direct pressure  
        ✅ Elevate wound  
        ✅ Do NOT remove soaked bandages  
        ✅ Call emergency services  
        """)

    with st.expander("🔥 Burns"):
        st.write("""
        ✅ Cool water 20 minutes  
        ❌ Do NOT apply toothpaste or oil  
        ✅ Cover with clean cloth  
        """)

# ===================== MEDICAL PROFILE (LOCAL STORAGE ONLY) ======================
elif page == "👤 Medical Profile":
    st.header("👤 Your Medical Details")

    if "profile" not in st.session_state:
        st.session_state.profile = {}

    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=120)
    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    conditions = st.text_area("Medical Conditions (Optional)")
    emergency = st.text_input("Emergency Contact Number")

    if st.button("Save Profile ✅"):
        st.session_state.profile = {
            "Name": name,
            "Age": age,
            "Blood Group": blood,
            "Medical Conditions": conditions,
            "Emergency Contact": emergency
        }
        st.success("Profile Saved Securely ✅")

    if st.session_state.profile:
        st.subheader("📌 Saved Information:")
        st.json(st.session_state.profile)

# Footer
st.markdown('<p class="footer-text">Made for India 🇮🇳 | LifeLink Emergency App</p>', unsafe_allow_html=True)
