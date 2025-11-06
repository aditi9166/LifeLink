# lifelink.py
import streamlit as st
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time

# -------------------- Page config --------------------
st.set_page_config(page_title="LifeLink • Emergency Locator", page_icon="🚨", layout="wide")

# -------------------- Styles (gradient, typography, animations) --------------------
st.markdown(
    """
    <style>
    :root{
        --em-red: #ff2e2e;
        --em-orange: #ff7a2d;
        --med-blue: #0f6fbf;
        --card-bg: rgba(255,255,255,0.03);
        --glass: rgba(255,255,255,0.06);
        --text: #eaf2ff;
    }

    /* Page background (minimal, solid + subtle texture) */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #071427 0%, #0b2336 100%);
        color: var(--text);
        font-family: "Inter", "Helvetica", Arial, sans-serif;
    }

    /* Hero */
    .hero {
        border-radius: 14px;
        padding: 28px;
        background: linear-gradient(90deg, rgba(255,46,46,0.12), rgba(255,122,45,0.06));
        box-shadow: 0 8px 40px rgba(0,0,0,0.5);
        margin-bottom: 18px;
    }
    .hero-title {
        font-size: 38px;
        font-weight: 800;
        color: white;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: rgba(235,245,255,0.85);
        font-size: 16px;
        margin-bottom: 14px;
    }
    .cta {
        background: linear-gradient(90deg, var(--em-red), var(--em-orange));
        color: white;
        padding: 14px 22px;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        font-size: 18px;
    }
    .cta:active { transform: scale(0.99); }

    /* Quick selectors */
    .quick-panel {
        background: var(--card-bg);
        padding: 14px;
        border-radius: 12px;
        display:flex;
        gap:12px;
        justify-content: space-between;
    }
    .quick-btn {
        background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 2px solid rgba(255,255,255,0.06);
        min-width: 160px;
        padding: 12px;
        border-radius: 12px;
        text-align:center;
        cursor:pointer;
    }
    .quick-btn .title { font-weight:800; color:white; font-size:16px; }
    .quick-btn .desc { color: rgba(235,245,255,0.8); font-size:13px; margin-top:6px; }

    /* Cards */
    .card {
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 6px 30px rgba(0,0,0,0.45);
    }

    /* Feature showcase */
    .feature {
        background: linear-gradient(180deg, rgba(15,78,146,0.12), rgba(10,40,80,0.04));
        border-radius: 10px;
        padding: 12px;
        text-align:center;
    }
    .feature h4 { color: white; margin-bottom:6px; }
    .feature p { color: rgba(235,245,255,0.8); font-size:13px; }

    /* Chat box */
    .chat-box {
        background: var(--glass);
        border-radius: 12px;
        padding: 12px;
    }
    .user-msg { text-align: right; color: white; background: rgba(255,255,255,0.04); padding:8px; margin:6px 0; border-radius:8px; }
    .bot-msg { text-align: left; color: white; background: rgba(255,255,255,0.02); padding:8px; margin:6px 0; border-radius:8px; }

    /* Footer */
    .footer { color: rgba(255,255,255,0.6); font-size:13px; padding:8px; text-align:center; margin-top:18px; }

    /* Responsive small screens */
    @media (max-width: 800px) {
        .hero-title { font-size: 28px; }
        .quick-panel { flex-direction: column; gap:10px; }
    }

    /* subtle pulse animation for CTA */
    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(255,46,46,0.6); }
      70% { box-shadow: 0 0 0 14px rgba(255,46,46,0.0); }
      100% { box-shadow: 0 0 0 0 rgba(255,46,46,0.0); }
    }
    .cta.pulse { animation: pulse 2s infinite; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Layout: Hero + two-column --------------------
st.markdown(
    """
    <div class="hero">
      <div style="display:flex; align-items:center; justify-content:space-between; gap:12px;">
        <div style="flex:1;">
          <div class="hero-title">🚨 LifeLink • Emergency Locator</div>
          <div class="hero-sub">Fast access to help: hospitals, ambulance numbers, first-aid instructions and instant ChatHelp guidance.</div>
          <div style="display:flex; gap:12px; align-items:center;">
            <button class="cta pulse" onclick="window.scrollTo(0,600)">SOS • Call Ambulance</button>
            <button class="cta" style="background:transparent; border:2px solid rgba(255,255,255,0.12); color: white; font-weight:700;" onclick="window.scrollTo(0,1000)">Find Hospital</button>
          </div>
        </div>
        <div style="width:320px; text-align:right;">
          <img src="https://images.unsplash.com/photo-1580281657524-25f79b9b6a4d?auto=format&fit=crop&w=700&q=60" style="width:280px; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.5);" alt="medical">
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- Quick emergency selector --------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<strong style='font-size:18px'>Quick Emergency Type</strong>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="quick-panel" style="margin-top:12px;">
      <div class="quick-btn" onclick="document.getElementById('heart-btn').click();">
        <div class="title">💔 Heart Attack</div>
        <div class="desc">Chest pain / shortness of breath — call ambulance</div>
      </div>
      <div class="quick-btn" onclick="document.getElementById('stroke-btn').click();">
        <div class="title">🧠 Stroke</div>
        <div class="desc">Face/arm/speech weakness — note time and act</div>
      </div>
      <div class="quick-btn" onclick="document.getElementById('accident-btn').click();">
        <div class="title">🚗 Major Accident</div>
        <div class="desc">Severe bleeding or trauma — stabilize & call</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
# hidden buttons hooked to JS clicks above
col_hidden = st.container()
with col_hidden:
    heart = st.button("hidden_heart", key="heart-btn", help="hidden")
    stroke = st.button("hidden_stroke", key="stroke-btn", help="hidden")
    accident = st.button("hidden_accident", key="accident-btn", help="hidden")
# handle those
if st.session_state.get("hidden_heart"):
    st.warning("Heart Attack — Call Ambulance: 108 • Start CPR if trained.")
if st.session_state.get("hidden_stroke"):
    st.warning("Stroke — FAST: Face/Arm/Speech • Get to hospital quickly.")
if st.session_state.get("hidden_accident"):
    st.warning("Major Accident — Control bleeding • Call ambulance.")

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Two-column main area --------------------
left_col, right_col = st.columns([2, 1])

# --- LEFT: Hospital Locator preview, First-aid, Feature showcase
with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🏥 Hospital Locator (Preview)")
    st.markdown("<em>Type a city or address — we show a map preview and sample nearby hospitals</em>", unsafe_allow_html=True)

    with st.form("locator_form", clear_on_submit=False):
        user_loc = st.text_input("Enter location (city, locality) — e.g., 'Pune' or 'MG Road, Bengaluru'")
        radius = st.slider("Search radius (approx meters)", min_value=1000, max_value=10000, value=3000, step=500)
        submit = st.form_submit_button("Search hospitals")
        if submit:
            if not user_loc.strip():
                st.error("Please enter a location")
            else:
                # geocode and show folium map
                geolocator = Nominatim(user_agent="lifelink_demo_app")
                try:
                    point = geolocator.geocode(user_loc, timeout=10)
                except Exception as e:
                    point = None
                if not point:
                    st.error("Location not found. Try more specific input.")
                else:
                    lat, lon = point.latitude, point.longitude
                    st.success(f"Found: {point.address}")
                    fmap = folium.Map(location=[lat, lon], zoom_start=13)
                    folium.Marker([lat, lon], popup="You are here", icon=folium.Icon(color="red")).add_to(fmap)

                    # add sample hospital pins (generated offsets)
                    sample_hospitals = [
                        ("City General Hospital", lat + 0.008, lon + 0.006),
                        ("Emergency Care Center", lat - 0.007, lon - 0.004),
                        ("Round-the-clock Clinic", lat + 0.003, lon - 0.009),
                    ]
                    for h in sample_hospitals:
                        folium.Marker([h[1], h[2]], popup=h[0], icon=folium.Icon(color="green", icon="plus")).add_to(fmap)
                    st_folium(fmap, width=700, height=420)

    st.markdown("</div>", unsafe_allow_html=True)

    # First-aid quick guide
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🩹 First-Aid Quick Guide")
    with st.expander("CPR — Adult (compressions)"):
        st.write(
            "1. Check responsiveness. 2. Call emergency services. "
            "3. If not breathing, start chest compressions: 30 compressions at 100-120/min. "
            "4. If trained, give rescue breaths in cycles of 30:2."
        )
    with st.expander("Severe Bleeding"):
        st.write(
            "Apply direct pressure, use clean cloth. If bleeding soaks through, add layers. "
            "Consider tourniquet only if trained and life-threatening."
        )
    with st.expander("Stroke (FAST)"):
        st.write("F — Face droop, A — Arm weakness, S — Speech issues, T — Time, act fast.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Feature showcase
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("✨ Features (First Version)")
    feat_cols = st.columns(3)
    with feat_cols[0]:
        st.markdown("<div class='feature'><h4>Emergency CTA</h4><p>Large, accessible panic CTA for immediate action.</p></div>", unsafe_allow_html=True)
    with feat_cols[1]:
        st.markdown("<div class='feature'><h4>Hospital Preview</h4><p>Map preview & sample hospitals for quick decision.</p></div>", unsafe_allow_html=True)
    with feat_cols[2]:
        st.markdown("<div class='feature'><h4>First-Aid</h4><p>Concise instructions for high-impact care.</p></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT: ChatHelp (AI intro), emergency numbers, profile summary
with right_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🤖 ChatHelp • Quick Guidance")
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("bot", "Hi — I'm LifeLink ChatHelp. Type your emergency or ask for instructions (e.g., 'how to do CPR').")
        ]

    # chat display
    for who, msg in st.session_state.chat_history:
        if who == "user":
            st.markdown(f"<div class='user-msg'>{st.session_state.get('user_style','You')}: {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'>LifeLink: {msg}</div>", unsafe_allow_html=True)

    # input area
    user_input = st.text_input("Ask ChatHelp (no personal data):", key="chat_input")
    if st.button("Send", key="send_chat"):
        q = user_input.strip()
        if q:
            st.session_state.chat_history.append(("user", q))

            # SIMPLE rule-based responses (safe, offline)
            q_low = q.lower()
            if "cpr" in q_low or "cardiac" in q_low:
                answer = "For adult CPR: Call for help, 30 chest compressions then 2 rescue breaths (if trained). Compress at 100-120/min."
            elif "bleed" in q_low or "bleeding" in q_low:
                answer = "Apply firm direct pressure to the wound, elevate limb if possible. Call emergency services."
            elif "stroke" in q_low:
                answer = "Check for FAST signs: Face, Arm, Speech, Time. If any positive — get to hospital immediately."
            elif "ambulance" in q_low or "call" in q_low:
                answer = "In India, call 108 for ambulance. If unsafe, call local emergency numbers."
            elif "hospital" in q_low:
                answer = "Use 'Find Hospital' above and type your city to view nearest hospitals."
            else:
                # fallback helpful guidance
                answer = "I recommend: 1) Ensure scene safety. 2) Call emergency services. 3) Give brief details: location, condition, number of injured."
            st.session_state.chat_history.append(("bot", answer))
            # clear input
            st.session_state.chat_input = ""

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Emergency Contacts card
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📞 Emergency Contacts")
    st.markdown("<strong>Ambulance</strong>: 108  &nbsp;&nbsp; <strong>Police</strong>: 100  &nbsp;&nbsp; <strong>Fire</strong>: 101", unsafe_allow_html=True)
    st.markdown("<small>Tip: On mobile, tap the number to call (browser dependent).</small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Medical Profile quick view (session-only)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("👤 Medical Profile (Temporary)")
    if "profile" not in st.session_state:
        st.session_state.profile = {"Name": "", "Age": "", "Blood": "", "Allergies": "", "Emergency": ""}
    name = st.text_input("Name", st.session_state.profile.get("Name", ""), key="p_name")
    age = st.text_input("Age", st.session_state.profile.get("Age", ""), key="p_age")
    blood = st.selectbox("Blood Group", ["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"], index=0, key="p_blood")
    allergies = st.text_input("Allergies", st.session_state.profile.get("Allergies", ""), key="p_allergies")
    emergency = st.text_input("Emergency Contact", st.session_state.profile.get("Emergency", ""), key="p_emergency")

    if st.button("Save Profile (local)"):
        st.session_state.profile = {"Name": name, "Age": age, "Blood": blood, "Allergies": allergies, "Emergency": emergency}
        st.success("Profile saved locally (session only).")

    if st.session_state.profile.get("Name"):
        st.markdown("<small>Saved in session</small>", unsafe_allow_html=True)
        st.json(st.session_state.profile)

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- Footer --------------------
st.markdown("<div class='footer'>Designed for quick action — Red urgency + Blue medical trust • Large touch targets • Minimal navigation</div>", unsafe_allow_html=True)
