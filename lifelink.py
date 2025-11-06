import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import requests

# =============== UI DESIGN START =============== #
# Set full screen background image via custom CSS
background_image_url = "https://images.unsplash.com/photo-1584433144859-1fc3ab64a957"

page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🚑 LifeLink - Emergency Medical Locator")
st.write("Quickly locate nearby hospitals & get ambulance support instantly!")

geolocator = Nominatim(user_agent="lifelink_app")
# =============== UI DESIGN END =============== #

# Function to get coordinates
def get_coordinates(place):
    try:
        location = geolocator.geocode(place)
        return (location.latitude, location.longitude)
    except:
        return None

# Nearby Hospital Search API
def nearby_hospitals(lat, lon):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q=hospital&limit=8&lat={lat}&lon={lon}"
    response = requests.get(url).json()
    return response

# Input Location
st.subheader("📍 Enter Your Location")
place = st.text_input("Type your current place / city:")

if place:
    coords = get_coordinates(place)

    if coords:
        lat, lon = coords
        st.success(f"✅ Location found: {place}")

        # Map
        map_obj = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker([lat, lon], tooltip="You are here", icon=folium.Icon(color="red")).add_to(map_obj)

        # Search nearby hospitals
        hospitals = nearby_hospitals(lat, lon)
        st.subheader("🏥 Nearby Hospitals:")

        if hospitals:
            for h in hospitals:
                name = h.get("display_name", "Unknown Hospital")
                hosp_lat = h.get("lat")
                hosp_lon = h.get("lon")

                folium.Marker(
                    [float(hosp_lat), float(hosp_lon)],
                    tooltip=name,
                    icon=folium.Icon(color="green", icon="plus-sign")
                ).add_to(map_obj)

                st.write(f"✅ {name}")

            st_map = st_folium(map_obj, width=700, height=450)

        else:
            st.warning("⚠ No hospitals found nearby. Try another location!")

        # Emergency Buttons
        st.subheader("🚨 Emergency Assistance")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📞 Call Ambulance"):
                st.error("➡ Dial 102 for emergency medical support!")

        with col2:
            if st.button("🩹 First-Aid Tips"):
                st.info("""
✅ Stay Calm  
✅ Stop bleeding with pressure  
✅ Keep victim warm  
✅ Do NOT move injured if spine suspected  
Call Emergency immediately!
                """)

    else:
        st.error("❌ Location not found! Try a more specific name.")

st.markdown("---")
st.write("💙 Built with care for saving lives — Team LifeLink")
