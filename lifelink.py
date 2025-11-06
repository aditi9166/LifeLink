import streamlit as st
import webbrowser

st.set_page_config(page_title="LifeLink Emergency", page_icon="🚨", layout="wide")

# ---- Custom Minimalist Background ----
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1586773860418-d37222d8fce3?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background-color: #0A0A0A;
}

.transparent-box {
    background: rgba(255, 255, 255, 0.80);
    padding: 25px;
    border-radius: 12px;
}

.center-text {
    text-align: center;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)



# ---- Sidebar Navigation ----
st.sidebar.title("🧭 Navigate")
menu = st.sidebar.radio(
    "",
    ["🏠 Home", "🏥 Hospital Locator", "🩹 First-Aid Guide", "🧑‍⚕️ Medical Profile"]
)



# ---- HOME SCREEN ----
if menu == "🏠 Home":
    st.markdown("<div class='transparent-box center-text'>", unsafe_allow_html=True)
    st.markdown("<h1>🚨 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
    st.write("Connecting people to immediate medical help ⚕️")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("### Quick Assistance")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❤️ Heart Attack Help"):
            st.warning("Call Emergency Immediately!")
            st.info("Symptoms: Chest pain, breathlessness, sweating")
            st.success("Take Aspirin if available")
            st.write("📞 Ambulance: 108")
    with col2:
        if st.button("🧠 Stroke Help"):
            st.warning("Act FAST – Face drooping, Arm weakness, Speech trouble!")
            st.write("📞 Ambulance: 108")
    with col3:
        if st.button("🚑 Accident Help"):
            st.warning("Stay Calm. Stop major bleeding immediately.")
            st.write("📞 Ambulance: 108")

    st.write("---")
    st.markdown(
        "<div class='transparent-box center-text'>"
        "<h3>📞 India Emergency Contacts</h3>"
        "<b>🚑 Ambulance: 108 | 👮 Police: 100 | 🔥 Fire: 101</b>"
        "</div>",
        unsafe_allow_html=True
    )



# ---- HOSPITAL LOCATOR ----
elif menu == "🏥 Hospital Locator":
    st.markdown("<div class='transparent-box center-text'>", unsafe_allow_html=True)
    st.header("🏥 Hospital Locator")

    st.success("Feature Coming Soon: 'Nearby Hospitals' Auto-Locator using GPS 🌍")

    st.info("Until then: Search 'Hospitals near me' below 👇")

    if st.button("🔍 Search Hospitals near me"):
        webbrowser.open("https://www.google.com/maps/search/hospitals+near+me/")
    st.markdown("</div>", unsafe_allow_html=True)



# ---- FIRST AID GUIDE ----
elif menu == "🩹 First-Aid Guide":
    st.markdown("<div class='transparent-box center-text'>", unsafe_allow_html=True)
    st.header("🩹 First-Aid Guide")

    faqs = {
        "Heavy Bleeding": "Apply pressure with a clean cloth. Do NOT remove cloth if blood soaks.",
        "Burn Injury": "Cool the burned area under running water for 15 minutes.",
        "Choking": "Perform Heimlich maneuver — 5 thrusts behind back, 5 chest compressions.",
        "Fracture": "Immobilize the injured area. Do not move bones yourself!"
    }

    for condition, help_text in faqs.items():
        if st.button(f"📌 {condition}"):
            st.warning(help_text)

    st.markdown("</div>", unsafe_allow_html=True)



# ---- MEDICAL PROFILE ----
elif menu == "🧑‍⚕️ Medical Profile":
    st.markdown("<div class='transparent-box center-text'>", unsafe_allow_html=True)
    st.header("🧑‍⚕️ My Medical Details")

    name = st.text_input("👤 Name")
    age = st.number_input("🎂 Age", 1, 120)
    blood = st.selectbox("🩸 Blood Group", ["A+","A-","B+","B-","O+","O-","AB+","AB-"])
    allergy = st.text_area("⚠️ Allergies")
    condition = st.text_area("💊 Medical Conditions")

    if st.button("💾 Save Profile"):
        st.success("✅ Profile saved! (local display only, no database)")
        st.info(f"Name: {name}, Age: {age}, Blood: {blood}")
    st.markdown("</div>", unsafe_allow_html=True)
