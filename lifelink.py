import streamlit as st
from datetime import datetime
import time

# -------------------- Page Config --------------------
st.set_page_config(page_title="LifeLink • Emergency Locator", page_icon="🚨", layout="wide")

# -------------------- Custom CSS (Same UI Design) --------------------
st.markdown("""
<style>
:root {
    --lifelink-red: #FF3B30;
    --lifelink-blue: #007BFF;
    --lifelink-dark-bg: #1C1C1E;
    --lifelink-light-bg: #F9F9F9;
    --lifelink-card-bg: #2C2C2E;
}

body {
    background-color: var(--lifelink-light-bg);
    font-family: Arial, sans-serif;
}

.tab-btn {
    width: 100%;
    padding: 14px;
    text-align: center;
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
}

.navbar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: white;
    padding: 12px 0;
    display: flex;
    justify-content: space-around;
    border-top: 2px solid #ddd;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 18px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Navigation State --------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate_to(page):
    st.session_state.page = page

# -------------------- Emergency Alert --------------------
def emergency_trigger():
    st.error("🚨 Emergency Alert Sent!\nNearby services are notified.")
    time.sleep(2)

# -------------------- Pages --------------------
def home_page():
    st.title("🚑 LifeLink Emergency Locator")

    st.subheader("Quick Actions")
    st.button("🚨 Emergency SOS", on_click=emergency_trigger)

    st.write("Tap an option below:")
    st.button("🏥 Find Hospitals", on_click=lambda: navigate_to("Hospitals"))
    st.button("⛑ First Aid", on_click=lambda: navigate_to("FirstAid"))
    st.button("👤 Profile", on_click=lambda: navigate_to("Profile"))

def hospitals_page():
    st.title("🏥 Nearby Hospitals")
    st.write("Tap to call or navigate")

    hospitals = [
        {"name": "City Care Hospital", "contact": "108", "distance": "1.4 km"},
        {"name": "LifeAid Trauma Center", "contact": "102", "distance": "3.0 km"},
        {"name": "Metro Emergency Clinic", "contact": "101", "distance": "4.2 km"}
    ]

    for hos in hospitals:
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <b>{hos['name']}</b><br>
                📍 {hos['distance']} away <br>
                📞 Call: {hos['contact']}
            </div>
            """, unsafe_allow_html=True)

def firstaid_page():
    st.title("⛑ First Aid Guidance")
    st.info("Select guidance category below:")
    st.button("💥 Injury — Bleeding Control")
    st.button("🔥 Burns Treatment Steps")
    st.button("⚡ Electric Shock — Do's & Don’ts")

def profile_page():
    st.title("👤 Your Profile")
    st.text_input("Enter your name")
    st.text_input("Emergency Contact")
    st.button("Save")

# -------------------- Render Based on Navigation --------------------
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Hospitals":
    hospitals_page()
elif st.session_state.page == "FirstAid":
    firstaid_page()
elif st.session_state.page == "Profile":
    profile_page()

# -------------------- Bottom Navigation --------------------
st.markdown("""
<div class='navbar'>
    <div class='tab-btn' onclick="window.location.href='/?page=Home'">🏠 Home</div>
    <div class='tab-btn' onclick="window.location.href='/?page=Hospitals'">🏥</div>
    <div class='tab-btn' onclick="window.location.href='/?page=FirstAid'">⛑</div>
    <div class='tab-btn' onclick="window.location.href='/?page=Profile'">👤</div>
</div>
""", unsafe_allow_html=True)
