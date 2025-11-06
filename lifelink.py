st.markdown(
    """
    <style>
    :root{
        --em-red: #ff3b3b;
        --em-orange: #ff8a3d;
        --med-blue: #007bff;
        --card-bg: rgba(255,255,255,0.08);
        --glass: rgba(255,255,255,0.12);
        --text: #ffffff;
        --subtext: #d6e2f5;
    }

    /* Page background: Dark clean medical */
    [data-testid="stAppViewContainer"] {
        background: #0e1e2e;
        color: var(--text);
        font-family: "Inter", "Helvetica", Arial, sans-serif;
    }

    /* Ensure ALL headings and labels visible */
    h1, h2, h3, h4, h5, h6, label, p, span {
        color: var(--text) !important;
    }

    /* Input fields readable */
    input, select, textarea {
        color: black !important;
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    .stTextInput>div>div>input {
        color: black !important;
    }

    /* Hero Area Styling */
    .hero {
        border-radius: 16px;
        padding: 28px;
        background: linear-gradient(90deg, rgba(255,59,59,0.20), rgba(0,123,255,0.15));
        box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    }
    .hero-title {
        font-size: 40px;
        font-weight: 900;
        color: white;
        margin-bottom: 6px;
    }
    .hero-sub {
        color: var(--subtext);
        font-size: 17px;
        margin-bottom: 14px;
    }

    /* CTA Buttons */
    .cta {
        background: linear-gradient(90deg, var(--em-red), var(--em-orange));
        color: white !important;
        padding: 14px 26px;
        border-radius: 12px;
        font-weight: 800 !important;
        font-size: 18px;
        border: none !important;
        cursor:pointer;
    }

    /* Emergency Quick Panel */
    .quick-panel {
        background: var(--card-bg);
        padding: 14px;
        border-radius: 14px;
        display:flex;
        gap:12px;
        justify-content: space-between;
    }
    .quick-btn {
        background: rgba(255,255,255,0.08);
        border: 2px solid rgba(255,255,255,0.10);
        min-width: 160px;
        padding: 14px;
        border-radius: 14px;
        text-align:center;
        cursor:pointer;
        transition:0.2s;
    }
    .quick-btn:hover { background: rgba(255,255,255,0.15); }
    .quick-btn .title { font-weight:900; color:white; font-size:17px; }
    .quick-btn .desc { color: var(--subtext); font-size:13px; margin-top:6px; }

    /* Card background */
    .card {
        background: rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.45);
    }

    /* Chat Box */
    .chat-box {
        background: rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 12px;
    }
    .bot-msg, .user-msg {
        border-radius: 10px;
        margin: 6px 0;
        font-size:14px;
    }
    .user-msg {
        text-align: right;
        background: rgba(255,255,255,0.18);
        padding:8px;
    }
    .bot-msg {
        background: rgba(0,0,0,0.25);
        padding:8px;
    }

    /* Emergency Numbers contrast */
    strong { color: white !important; }
    small { color: var(--subtext) !important; }

    /* Footer */
    .footer {
        color: var(--subtext);
        font-size:13px;
        text-align:center;
        margin-top:16px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)
