import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# ============ PAGE CONFIG ============
st.set_page_config(page_title="LifeLink - Emergency Locator",
                   page_icon="🚨",
                   layout="wide")

# ============ CUSTOM BACKGROUND ============
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1582550945154-66ea8fff07a7');
    background-size: cover;
    background-position: center;
}
[data-testid="stSidebar"] {
    background-color: rgba(0,0,0,0.7) !important;
}
h1, h2, h3, label, p {
    color: white !important;
}
.stButton>button {
    background-color: red;
    color: white;
    border-radius: 8px;
    padding: 10px;
}
.card {
    background-color: rgba(0,0,0,0.6);
    padding: 20px;
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ============ APP TITLE ============
st.markdown("<h1 class='card'>🚨 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
st.write("Helping people reach medical help faster ❤️‍🩹")

# ============ SIDEBAR NAVIGATION ============
menu = st.sidebar.radio("Navigate", ["🏠 Home", "🏥 Hospital Locator", "🩹 First-Aid Guide", "👤 Medical Profile"])

# ============ HOME PAGE ============
if menu == "🏠 Home":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Quick Emergency Access")
    col1, col2, col3 = st.columns(3)
    
    col1.button("💔 Heart Attack", key="heart")
    col2.button("🧠 Stroke", key="stroke")
    col3.button("🚗 Accident", key="accident")
    
    st.warning("📞 Emergency Numbers in India:")
    st.info("🚑 Ambulance: 108 | 👮 Police: 100 | 🔥 Fire: 101")
    st.markdown("</div>", unsafe_allow_html=True)

# ============ HOSPITAL LOCATOR ============
elif menu == "🏥 Hospital Locator":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Find Nearby Hospitals 🏥")

    city = st.text_input("Enter Location (City Name):", placeholder="e.g., Mumbai")

    if st.button("Search"):
        geolocator = Nominatim(user_agent="lifelink_app")
        location = geolocator.geocode(city)

        if location:
            lat, lon = location.latitude, location.longitude
            m = folium.Map(location=[lat, lon], zoom_start=13)

            # Example hospitals (static for now)
            hospitals = [
                ("City Hospital", lat + 0.01, lon + 0.01),
                ("Care MultiSpeciality", lat - 0.01, lon - 0.01),
                ("Apollo Emergency Center", lat + 0.015, lon - 0.005)
            ]

            for hos in hospitals:
                folium.Marker([hos[1], hos[2]], popup=hos[0], icon=folium.Icon(color="red")).add_to(m)

            st_folium(m, width=700, height=450)
        else:
            st.error("📍 Location not found! Try another city.")

    st.markdown("</div>", unsafe_allow_html=True)

# ============ FIRST-AID GUIDE ============
elif menu == "🩹 First-Aid Guide":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Life-Saving First Aid Instructions")

    help_option = st.selectbox("Select Emergency", 
                               ["CPR for Cardiac Arrest", 
                                "Bleeding Control", 
                                "Choking", 
                                "Burn Injury"])

    guides = {
        "CPR for Cardiac Arrest": "1️⃣ Check responsiveness\n2️⃣ Call 108\n3️⃣ Push hard & fast, 100-120 bpm\n4️⃣ Continue until help arrives",
        "Bleeding Control": "Apply pressure + bandage | Keep wound elevated",
        "Choking": "Perform Heimlich Maneuver | Back blows for children",
        "Burn Injury": "Cool with water 20 min | Do NOT pop blisters"
    }

    st.info(guides[help_option])
    st.markdown("</div>", unsafe_allow_html=True)

# ============ MEDICAL PROFILE (Local Session) ============
elif menu == "👤 Medical Profile":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Your Emergency Health Details")

    name = st.text_input("Full Name")
    age = st.text_input("Age")
    allergies = st.text_input("Allergies (if any)")
    medications = st.text_input("Current Medications")
    emergency_contact = st.text_input("Emergency Contact Number")

    if st.button("Save Profile"):
        st.session_state["profile"] = [name, age, allergies, medications, emergency_contact]
        st.success("✅ Saved Successfully!")

    if "profile" in st.session_state:
        st.write("### Stored Medical Profile 📌")
        st.table({
            "Detail": ["Name", "Age", "Allergies", "Medications", "Emergency Contact"],
            "Value": st.session_state["profile"]
        })

    st.markdown("</div>", unsafe_allow_html=True)

