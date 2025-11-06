import streamlit as st

st.set_page_config(page_title="LifeLink Emergency Locator", page_icon="🚑")

st.title("🚑 LifeLink Emergency Locator")
st.write("Connect to life-saving help instantly during emergencies")

menu = st.sidebar.radio(
    "Select Service",
    ["Hospital Locator", "Emergency Contacts", "First Aid Guide", "Medical Profile"]
)

if menu == "Hospital Locator":
    st.subheader("🏥 Hospital Locator")
    st.info("Coming Soon: Nearest hospitals with navigation")

elif menu == "Emergency Contacts":
    st.subheader("📞 Emergency Contacts")
    st.write("🚑 Ambulance: 108")
    st.write("👮 Police: 100")
    st.write("🔥 Fire: 101")

elif menu == "First Aid Guide":
    st.subheader("🩹 First Aid Guide")
    st.warning("Coming Soon: CPR, bleeding, choking support")

elif menu == "Medical Profile":
    st.subheader("👤 Medical Profile")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=1, max_value=120, value=18)
    allergies = st.text_input("Allergies / Medical Conditions")

    if st.button("Save Profile"):
        st.success("✅ Profile Saved Successfully")
