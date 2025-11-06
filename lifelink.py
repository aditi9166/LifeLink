

import streamlit as st
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from folium import Map, Marker
from streamlit_folium import st_folium

# Set Streamlit app config
st.set_page_config(page_title="LifeLink Emergency Locator", layout="mobile", initial_sidebar_state="collapsed")

# Dummy in-memory profile storage (not saved permanently)
saved_profiles = []

# --- Helper function for geocoding ---
def geocode_address(address):
    geolocator = Nominatim(user_agent="lifelink_app")
    loc = geolocator.geocode(address, timeout=10)
    if loc:
        return loc.latitude, loc.longitude
    return None

# --- Helper function for hospital search using Overpass API ---
def find_hospitals(lat, lon, radius=3000):
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      way["amenity"="hospital"](around:{radius},{lat},{lon});
    );
    out center;
    """
    url = "https://overpass-api.de/api/interpreter"
    res = requests.post(url, data={"data": query})
    data = res.json()
    results = []

    for el in data.get("elements", []):
        if "tags" in el:
            name = el["tags"].get("name", "Unnamed Hospital")
            if el["type"] == "node":
                lat2, lon2 = el["lat"], el["lon"]
            else:
                lat2, lon2 = el["center"]["lat"], el["center"]["lon"]
            results.append({"name": name, "lat": lat2, "lon": lon2})

    return pd.DataFrame(results)

# --- Main UI Title ---
st.markdown("<h1 style='color:#B00020;'>LifeLink Emergency Locator</h1>", unsafe_allow_html=True)
st.write("Find hospitals fast. Get first aid guidance. Save your medical profile.")

# --- Navigation buttons ---
page = st.radio("Select section", ["Hospital Locator", "Emergency", "First-Aid", "Medical Profile"])

# -------- Hospital Locator Page --------
if page == "Hospital Locator":
    st.subheader("Find Nearby Hospitals")
    address = st.text_input("Enter your address / city:")

    if st.button("Search"):
        with st.spinner("Locating hospitals..."):
            loc = geocode_address(address)
            if not loc:
                st.error("Location not found.")
            else:
                lat, lon = loc
                hospitals = find_hospitals(lat, lon)

                if hospitals.empty:
                    st.warning("No hospitals found nearby.")
                else:
                    st.success(f"Found {len(hospitals)} hospitals")
                    st.dataframe(hospitals)

                    # Show hospitals on map
                    fmap = Map(location=[lat, lon], zoom_start=13)
                    Marker([lat, lon], popup="Your location").add_to(fmap)

                    for _, row in hospitals.iterrows():
                        Marker([row["lat"], row["lon"]], popup=row["name"]).add_to(fmap)

                    st_folium(fmap, width=350, height=500)

# -------- Emergency Page --------
elif page == "Emergency":
    st.subheader("Emergency Quick Actions")

    if st.button("🚨 Heart Attack"):
        st.error("Call Ambulance Now!")
        st.write("Chest pain, shortness of breath. Start CPR if unresponsive.")
    if st.button("🧠 Stroke"):
        st.warning("FAST: Face, Arm, Speech — Time to hospital quickly!")
    if st.button("🩸 Major Bleeding"):
        st.info("Apply pressure on wound, elevate limb.")

    st.markdown("📞 **Emergency Calling**")
    st.markdown("[Call Ambulance (108)](tel:108)")

# -------- First Aid Info Page --------
elif page == "First-Aid":
    st.subheader("Basic First Aid Guide")

    with st.expander("CPR Instructions"):
        st.write("""
1. Tap and shout — check response.
2. Call emergency services.
3. Start chest compressions: 30 compressions then 2 breaths.
4. Continue until help arrives.
        """)

    with st.expander("Severe Bleeding"):
        st.write("Apply direct pressure and call ambulance immediately.")

# -------- Medical Profile Page --------
elif page == "Medical Profile":
    st.subheader("Save Medical Information")

    name = st.text_input("Full Name")
    allergies = st.text_input("Allergies")
    conditions = st.text_input("Medical Conditions")
    emergency = st.text_input("Emergency Contact Number")

    if st.button("Save Profile"):
        saved_profiles.append({
            "name": name,
            "allergies": allergies,
            "conditions": conditions,
            "emergency": emergency
        })
        st.success("Profile saved!")

    st.write("Saved Profiles:")
    st.write(saved_profiles)

