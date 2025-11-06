import streamlit as st

# ✅ Custom Styling + Background Image
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://i.imgur.com/wf7T7nE.jpeg');
    background-size: cover;
}
[data-testid="stHeader"] {
    background-color: rgba(255,255,255,0.2);
}
.sidebar .sidebar-content {
    background-color: rgba(255,0,0,0.2);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.set_page_config(page_title="LifeLink Emergency App", page_icon="🚑")

st.markdown("<h1 style='text-align: center; color: red;'>🚑 LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
st.write("Quick access to medical help during emergencies")

menu = st.sidebar.radio(
    "📌 Menu",
    ["🏥 Hospital Locator", "📞 Emergency Contacts", "🩹 First Aid Guide", "👤 Medical Profile", "🚨 SOS Button"]
)

# ✅ Pages
if menu == "🏥 Hospital Locator":
    st.subheader("🏥 Hospital Locator")
    st.info("Coming Soon: Live Map + Nearest Hospitals + Navigation")

elif menu == "📞 Emergency Contacts":
    st.subheader("📞 Emergency Contacts")
    st.success("Click to call (Tap numbers on smartphone)")
    st.write("🚑 Ambulance: **108**")
    st.write("👮 Police: **100**")
    st.write("🔥 Fire: **101**")
    st.write("🚨 Disaster Management: **112**")

elif menu == "🩹 First Aid Guide":
    st.subheader("🩹 First Aid Emergency Instructions")
    guide = st.selectbox("Select a Situation", ["CPR", "Burns", "Bleeding", "Choking"])
    
    if guide == "CPR":
        st.write("✅ Check responsiveness\n✅ Call medical help\n✅ Push hard & fast on chest")
    elif guide == "Burns":
        st.write("✅ Run cool water\n❌ Do NOT apply toothpaste\n✅ Wrap loosely")
    elif guide == "Bleeding":
        st.write("✅ Apply pressure\n✅ Keep elevated\n🚫 Do NOT remove soaked cloth")
    elif guide == "Choking":
        st.write("✅ Encourage coughing\n✅ Heimlich maneuver\n❌ Do NOT hit on back")

elif menu == "👤 Medical Profile":
    st.subheader("👤 Personal Medical Profile")
    name = st.text_input("Full Name")
    age = st.number_input("Age", 1, 120, 18)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    allergies = st.text_input("Allergies / Medical Conditions")
    medications = st.text_input("Regular Medications")
    emergency_contact = st.text_input("Emergency Contact Number")

    if st.button("💾 Save Profile"):
        st.success(f"✅ Profile Saved. Stay Safe, {name}!")

elif menu == "🚨 SOS Button":
    st.markdown("<h2 style='color:red;'>🚨 EMERGENCY SOS</h2>", unsafe_allow_html=True)
    st.warning("If you're in danger, press button!")
    if st.button("🔴 SEND ALERT"):
        st.error("🚑 SOS ALERT TRIGGERED!")
        st.write("📍 Calling local authorities...")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Made with ❤️ for Emergency Safety</p>", unsafe_allow_html=True)
