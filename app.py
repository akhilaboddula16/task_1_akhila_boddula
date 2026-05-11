import streamlit as st

from chatbot import get_ai_response, initialize_chat


DESTINATIONS = [
    {
        "title": "Maldives Escape",
        "subtitle": "Water villas and private dining",
        "prompt": "Plan a luxury Maldives getaway with a private pool villa and sunset experiences.",
    },
    {
        "title": "Swiss Summer",
        "subtitle": "Scenic rail and alpine luxury stays",
        "prompt": "Suggest a luxury Switzerland itinerary with scenic trains, lake-view hotels, and private transfers.",
    },
    {
        "title": "Dubai Indulgence",
        "subtitle": "Skyline suites and VIP access",
        "prompt": "Create a premium Dubai itinerary with luxury shopping, fine dining, and private city experiences.",
    },
]


st.set_page_config(
    page_title="Luxury Travel Consultant AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(214, 190, 123, 0.18), transparent 28%),
            radial-gradient(circle at top right, rgba(80, 127, 169, 0.16), transparent 24%),
            linear-gradient(180deg, #06101d 0%, #0d1727 44%, #0c1321 100%);
        color: #f7f2e8;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(8, 14, 24, 0.96), rgba(10, 18, 31, 0.96));
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1.4rem;
    }

    .sidebar-card, .hero-shell, .panel-card, .chat-stage, .destination-card {
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
        box-shadow: 0 20px 70px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(14px);
    }

    .sidebar-card {
        padding: 1rem 1rem 0.9rem 1rem;
        margin-bottom: 1rem;
    }

    .sidebar-title {
        color: #fff3d4;
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .sidebar-copy {
        color: #bfccdd;
        font-size: 0.92rem;
        line-height: 1.5;
        margin-bottom: 0;
    }

    .hero-shell {
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .hero-kicker {
        color: #d6be7b;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.16rem;
        margin-bottom: 0.55rem;
    }

    .hero-title {
        font-size: 2.75rem;
        line-height: 1.05;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        color: #d7deea;
        font-size: 1rem;
        margin-top: 0.75rem;
        margin-bottom: 0;
        max-width: 760px;
    }

    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 0 0 1rem 0;
    }

    .stat-card, .destination-card {
        padding: 1rem 1.05rem;
        border-radius: 22px;
        background: rgba(9, 16, 29, 0.82);
        border: 1px solid rgba(214, 190, 123, 0.15);
    }

    .stat-label, .section-kicker {
        color: #9fb0c8;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08rem;
        margin-bottom: 0.3rem;
    }

    .stat-value {
        color: #fff6df;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .panel-card {
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .panel-title {
        color: #fff4da;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .panel-copy {
        color: #bfd0e2;
        margin-bottom: 0;
    }

    .destination-title {
        color: #fff5de;
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .destination-subtitle {
        color: #bfd0e2;
        font-size: 0.93rem;
        margin-bottom: 0.9rem;
    }

    .chat-stage {
        padding: 1.1rem;
        background: rgba(8, 14, 24, 0.74);
    }

    .stChatMessage {
        background: transparent;
    }

    [data-testid="stChatMessageContent"] {
        border-radius: 22px;
        padding: 1rem 1.1rem;
        border: 1px solid rgba(255, 255, 255, 0.06);
        background: rgba(20, 28, 43, 0.94);
    }

    [data-testid="stChatMessageAvatarUser"] + [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(176, 54, 54, 0.95), rgba(124, 21, 47, 0.95));
        border: 1px solid rgba(255, 190, 190, 0.16);
    }

    [data-testid="stChatMessageAvatarAssistant"] + [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, rgba(184, 134, 11, 0.18), rgba(22, 31, 46, 0.95));
        border: 1px solid rgba(214, 190, 123, 0.18);
    }

    .stButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(214, 190, 123, 0.18);
        background: rgba(12, 20, 34, 0.94);
        color: #f8f1df;
        padding: 0.8rem 0.9rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: rgba(214, 190, 123, 0.45);
        color: white;
    }

    [data-testid="stChatInput"] {
        background: rgba(8, 14, 24, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
    }

    .stSelectbox label, .stSlider label {
        color: #d8e1ef !important;
        font-weight: 600;
    }

    @media (max-width: 900px) {
        .hero-title {
            font-size: 2rem;
        }

        .stats-row {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def submit_prompt(prompt_text: str) -> None:
    st.session_state.pending_prompt = prompt_text


def reset_chat() -> None:
    st.session_state.messages = initialize_chat()
    st.session_state.pending_prompt = None


if "messages" not in st.session_state:
    st.session_state.messages = initialize_chat()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Aurelia Concierge</div>
            <p class="sidebar-copy">
                A premium planning desk for curated getaways, family escapes, luxury city breaks,
                and villa-led experiences.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    travel_style = st.selectbox(
        "Travel style",
        ["Luxury retreat", "Relaxed luxury", "Family premium", "Adventure with comfort", "City indulgence"],
    )
    budget_band = st.selectbox(
        "Budget band",
        ["Rs. 1.5L - 3L", "Rs. 3L - 5L", "Rs. 5L - 8L", "Rs. 8L+"],
    )
    stay_length = st.slider("Stay length", min_value=3, max_value=10, value=5)

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">Planning Notes</div>
            <p class="sidebar-copy">
                Replies are optimized for point-wise recommendations with budget fit, ideal stay
                style, premium inclusions, and a clear next step.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start a fresh chat"):
        reset_chat()


main_col, side_col = st.columns([1.55, 1], gap="large")

with main_col:
    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-kicker">Private Concierge Experience</div>
            <h1 class="hero-title">Luxury Travel Consultant AI</h1>
            <p class="hero-subtitle">
                Plan premium journeys with a polished app-style travel desk that responds in clear
                points, curated recommendations, and tailored next steps.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">Planning Style</div>
                <div class="stat-value">Concise, premium, point-based guidance</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Configured Mood</div>
                <div class="stat-value">Luxury tone with practical recommendations</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Current Trip Lens</div>
                <div class="stat-value">"""
        + f"{travel_style} | {budget_band} | {stay_length} nights"
        + """</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chat-stage">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue

        avatar = "🧳" if message["role"] == "user" else "🛎️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    st.markdown("</div>", unsafe_allow_html=True)

with side_col:
    st.markdown(
        """
        <div class="panel-card">
            <div class="section-kicker">Quick Launch</div>
            <div class="panel-title">Travel Brief Builder</div>
            <p class="panel-copy">
                Launch a polished prompt fast, then let the concierge refine it in points.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    brief_col1, brief_col2 = st.columns(2)
    with brief_col1:
        if st.button("Luxury getaway"):
            submit_prompt(
                f"Plan a {stay_length}-night {travel_style.lower()} luxury getaway with a budget of {budget_band}."
            )
    with brief_col2:
        if st.button("VIP family trip"):
            submit_prompt(
                f"Plan a {stay_length}-night family luxury vacation within {budget_band} with premium experiences."
            )

    st.markdown(
        """
        <div class="panel-card">
            <div class="section-kicker">Destination Picks</div>
            <div class="panel-title">Curated Inspiration</div>
            <p class="panel-copy">
                Choose a destination card to preload a premium travel request.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for item in DESTINATIONS:
        st.markdown(
            f"""
            <div class="destination-card">
                <div class="destination-title">{item["title"]}</div>
                <div class="destination-subtitle">{item["subtitle"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"Explore {item['title']}", key=item["title"]):
            submit_prompt(item["prompt"])

    st.markdown(
        """
        <div class="panel-card">
            <div class="section-kicker">What To Ask</div>
            <div class="panel-title">Great prompts</div>
            <p class="panel-copy">
                Ask for villa options, sample itineraries, upgrade perks, transfers, dining, or the
                best season to travel.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


user_input = st.chat_input("Describe your dream journey, budget, and travel style...")
active_prompt = st.session_state.pending_prompt or user_input

if active_prompt:
    st.session_state.pending_prompt = None
    enriched_prompt = (
        f"{active_prompt}\n\n"
        f"Traveler profile:\n"
        f"- Travel style: {travel_style}\n"
        f"- Budget band: {budget_band}\n"
        f"- Preferred stay length: {stay_length} nights\n"
        f"- Please answer in clear points with a premium tone."
    )

    st.session_state.messages.append({"role": "user", "content": active_prompt})

    with main_col:
        with st.chat_message("user", avatar="🧳"):
            st.markdown(active_prompt)

        with st.chat_message("assistant", avatar="🛎️"):
            with st.spinner("Designing your luxury travel plan..."):
                assistant_reply = get_ai_response(
                    st.session_state.messages[:-1] + [{"role": "user", "content": enriched_prompt}]
                )
            st.markdown(assistant_reply)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
