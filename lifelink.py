import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# ===================== PAGE CONFIG ======================
st.set_page_config(page_title="LifeLink Emergency Locator", layout="wide")

# ===================== CLEAN SOLID UI STYLING ======================
solid_bg = """
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0A1A2F; /* Dark Navy Blue */
}

[data-testid="stSidebar"] {
    background-color: #00182A !important;
    border-right: 2px solid #FF4C4C;
}

h1, h2, h3, h4, label, p, .stMarkdown, .stRadio, .stTextInput, .stNumberInput, .stSelectbox,
.stTextArea, .stExpander, .stJson {
    color: #FFFFFF !important;  /* Pure White for high visibility */
    font-family: 'Helvetica', sans-serif;
    font-size: 18px;
}

.card {
    background-color: #11263D; 
    border-radius: 14px;
    padding: 25px;
    margin-top: 15px;
    border: 1px solid rgba(255,255,255,0.1);
}

.stButton>button {
    background: #FF3B3B;
    color: white;
    padding: 12px 20px;
    border: none;
    font-weight: bold;
    border-radius: 10px;
    transition: 0.25s;
    font-size: 18px;
}
.stButton>button:hover {
    transform: scale(1.09);
    background: #D60000;
}

.stExpander p {
    color: white !important;
}

.footer-text {
    text-align: center;
    color: #FFB9B9;
    margin-top: 40px;
    font-size: 15px;
}
</style>
"""
st.markdown(solid_bg, unsafe_allow_html=True)

# ===================== SIDEBAR NAVIGATION ======================
st.sidebar.title("Navigate")
page = st.sidebar.radio("",
                        ["🏠 Home", "🏥 Hospital Locator",
                         "🩹 First-Aid Guide", "👤 Medical Profile"])

# ===================== HOME PAGE ======================
if page == "🏠 Home":
    st.markdown("<h1>🚨 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
    st.markdown("### Helping people reach lifesaving support ⚕️")

    st.markdown("---")
    st.subheader("Quick Emergency Help")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❤️ Heart Attack"):
            st.warning("📞 Call 108 Immediately! Provide aspirin if available.")
    with col2:
        if st.button("🧠 Stroke"):
            st.warning("FAST: Face droop, Arm weakness, Speech issue — Act now!")
    with col3:
        if st.button("🚑 Accident"):
            st.warning("Keep the person calm. Control bleeding. Avoid movement.")

    st.subheader("📞 Emergency Numbers in India:")
    st.info("🚑 Ambulance: 108 | 👮 Police: 100 | 🔥 Fire: 101")

# ===================== HOSPITAL LOCATOR ======================
elif page == "🏥 Hospital Locator":

    st.header("🏥 Find Nearest Hospitals")

    user_location = st.text_input("Enter your city / location 🔍 (E.g., Mumbai)")

    if st.button("Search Hospital"):
        if not user_location.strip():
            st.error("⚠️ Please enter a valid location.")
        else:
            geolocator = Nominatim(user_agent="lifelink-app")
            loc = geolocator.geocode(user_location)

            if loc:
                m = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=13)
                folium.Marker([loc.latitude, loc.longitude],
                              tooltip="📍 You are here",
                              icon=folium.Icon(color='red')).add_to(m)

                st.success(f"✅ Location Found: {loc.address}")
                st_folium(m, height=450, width=900)
            else:
                st.error("❌ Location not found. Try again!")

# ===================== FIRST AID GUIDE ======================
elif page == "🩹 First-Aid Guide":
    st.header("🩹 First Aid Handbook")

    with st.expander("❤️ CPR (Cardiac Emergency)"):
        st.write("""
✅ Check breathing & response  
✅ Call 108  
✅ Hard chest compressions 100–120/min  
✅ Do not stop until help arrives  
        """)

    with st.expander("🩸 Severe Bleeding"):
        st.write("""
✅ Apply pressure with clean cloth  
✅ Elevate injured area  
❌ Don't remove soaked cloth  
✅ Seek urgent medical help  
        """)

    with st.expander("🔥 Burns"):
        st.write("""
✅ Cool water 20 minutes  
❌ No toothpaste / oil  
✅ Cover with clean cloth  
        """)

# ===================== MEDICAL PROFILE (No Database) ======================
elif page == "👤 Medical Profile":
    st.header("👤 Your Medical Details")

    if "profile" not in st.session_state:
        st.session_state.profile = {}

    name = st.text_input("Full Name")
    age = st.number_input("Age", 1, 120)
    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    conditions = st.text_area("Health Conditions (Optional)")
    emergency = st.text_input("Emergency Contact Number")

    if st.button("Save Profile ✅"):
        st.session_state.profile = {
            "Name": name,
            "Age": age,
            "Blood Group": blood,
            "Conditions": conditions,
            "Emergency Contact": emergency
        }
        st.success("✅ Saved! (Only stored temporarily on your device)")

    if st.session_state.profile:
        st.json(st.session_state.profile)

# Footer
st.markdown('<p class="footer-text">Made with ❤️ for India 🇮🇳 | LifeLink App</p>',
            unsafe_allow_html=True)
