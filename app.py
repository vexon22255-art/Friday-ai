"""Streamlit web interface for FRIDAY."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from streamlit_mic_recorder import mic_recorder


# This must be the first Streamlit command in the script.
st.set_page_config(
    page_title="FRIDAY · Anandhu's AI assistant",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

from gtts.tts import gTTSError

from main import DEFAULT_OUTPUT, create_chat, generate_response, synthesize


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(0, 156, 255, 0.13), transparent 34rem),
            radial-gradient(circle at 90% 30%, rgba(0, 67, 116, 0.16), transparent 28rem),
            #05080f;
        color: #eef0f7;
    }
    [data-testid="stHeader"] {
        background: rgba(8, 10, 17, 0.72);
    }
    [data-testid="stSidebar"] {
        background: #070b13;
        border-right: 1px solid rgba(0, 170, 255, 0.16);
    }
    [data-testid="stChatMessage"] {
        border: 1px solid rgba(0, 164, 255, 0.16);
        border-radius: 18px;
        margin: 0.65rem 0;
        padding: 0.8rem 1rem;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(105deg, rgba(0, 119, 190, 0.16), rgba(0, 40, 75, 0.12));
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(255, 255, 255, 0.045);
    }
    .hero {
        padding: 0.4rem 0 1.5rem;
        text-align: center;
    }
    .eyebrow {
        color: #35b7ff;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }
    .hero h1 {
        color: #ffffff;
        font-size: clamp(2.4rem, 7vw, 4.7rem);
        letter-spacing: -0.06em;
        line-height: 0.95;
        margin: 0.6rem 0 1rem;
    }
    .hero p {
        color: #aeb4c8;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 40rem;
        margin-left: auto;
        margin-right: auto;
    }
    .hint {
        border: 1px solid rgba(0, 173, 255, 0.22);
        border-radius: 999px;
        color: #aeb4c8;
        font-size: 0.9rem;
        line-height: 1.5;
        margin: 1.5rem auto;
        padding: 0.55rem 1rem;
        width: fit-content;
    }
    .hud-wrap {
        align-items: center;
        display: flex;
        gap: 1.4rem;
        justify-content: center;
        padding: 1rem 0 1.2rem;
    }
    .hud-badge {
        background: rgba(5, 22, 38, 0.78);
        border: 1px solid rgba(53, 190, 255, 0.42);
        border-radius: 12px;
        box-shadow: 0 0 18px rgba(0, 153, 255, 0.13), inset 0 0 14px rgba(0, 153, 255, 0.08);
        color: #a9eaff;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        line-height: 1.5;
        padding: 0.75rem 1rem;
        text-transform: uppercase;
    }
    @media (max-width: 640px) {
        .hud-wrap {
            flex-direction: column;
            gap: 1rem;
        }
        .hud-badge {
            font-size: 0.7rem;
        }
    }
    .hud {
        align-items: center;
        background:
            radial-gradient(circle, rgba(5, 25, 44, 0.96) 0 31%, transparent 32%),
            conic-gradient(from 18deg, transparent 0 8%, rgba(0, 178, 255, 0.8) 8.5% 9%, transparent 9.5% 18%, rgba(0, 125, 255, 0.46) 18.5% 19%, transparent 19.5% 38%, rgba(39, 203, 255, 0.85) 38.5% 39%, transparent 39.5% 63%, rgba(0, 125, 255, 0.58) 63.5% 64%, transparent 64.5% 100%);
        border: 1px solid rgba(52, 201, 255, 0.85);
        border-radius: 50%;
        box-shadow:
            0 0 0 5px rgba(0, 128, 255, 0.08),
            0 0 0 13px rgba(0, 128, 255, 0.055),
            0 0 38px rgba(0, 153, 255, 0.55),
            inset 0 0 28px rgba(0, 132, 255, 0.55);
        display: flex;
        height: min(248px, 68vw);
        justify-content: center;
        position: relative;
        width: min(248px, 68vw);
    }
    .hud::before,
    .hud::after {
        border: 1px solid rgba(53, 190, 255, 0.32);
        border-radius: 50%;
        content: "";
        position: absolute;
    }
    .hud::before {
        height: 78%;
        width: 78%;
    }
    .hud::after {
        border-style: dashed;
        height: 92%;
        transform: rotate(-22deg);
        width: 92%;
    }
    .hud-core {
        align-items: center;
        background: radial-gradient(circle, rgba(21, 127, 207, 0.3), rgba(3, 17, 30, 0.86) 68%);
        border: 1px solid rgba(93, 220, 255, 0.72);
        border-radius: 50%;
        box-shadow: 0 0 24px rgba(0, 190, 255, 0.38), inset 0 0 20px rgba(0, 143, 255, 0.4);
        display: flex;
        height: 53%;
        justify-content: center;
        position: relative;
        width: 53%;
        z-index: 1;
    }
    .hud-core::after {
        background: linear-gradient(transparent 45%, rgba(76, 212, 255, 0.7) 50%, transparent 55%);
        content: "";
        inset: 0;
        position: absolute;
        animation: hud-scan 3.2s ease-in-out infinite;
    }
    .hud-label {
        color: #d9f8ff;
        filter: drop-shadow(0 0 7px rgba(0, 199, 255, 0.95));
        font-size: clamp(0.82rem, 3vw, 1.15rem);
        font-weight: 700;
        letter-spacing: 0.14em;
        position: relative;
        text-shadow: 0 0 12px #00aaff;
        z-index: 2;
    }
    @keyframes hud-scan {
        0%, 100% { transform: translateY(-22px); opacity: 0.2; }
        50% { transform: translateY(22px); opacity: 0.8; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat" not in st.session_state:
        st.session_state.chat = None
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None
    if "access_level" not in st.session_state:
        st.session_state.access_level = None


def reset_chat() -> None:
    st.session_state.messages = []
    st.session_state.chat = None
    st.session_state.gemini_client = None
    st.session_state.audio_path = None


def set_access_level(level: str) -> None:
    reset_chat()
    st.session_state.access_level = level


def render_access_gate() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">Secure access · FRIDAY core</div>
          <h1>Identify yourself.</h1>
          <p>Boss access unlocks FRIDAY's full knowledge. Guests can still use FRIDAY for general questions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        st.markdown("### Boss access")
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter Boss password",
            label_visibility="collapsed",
        )
        if st.button("Enter as Boss Anandhu", type="primary", use_container_width=True):
            if password and password == os.environ.get("FRIDAY_BOSS_PASSWORD"):
                set_access_level("boss")
                st.rerun()
            st.error("Incorrect password.")
        st.divider()
        st.markdown("### Guest access")
        st.caption("General questions are welcome. Private creation and implementation details remain confidential.")
        if st.button("Continue as Guest", use_container_width=True):
            set_access_level("guest")
            st.rerun()


initialize_state()

if st.session_state.access_level is None:
    render_access_gate()
    st.stop()

with st.sidebar:
    st.markdown("## FRIDAY")
    st.caption("Anandhu's personal AI assistant")
    if st.session_state.access_level == "boss":
        st.success("Signed in as Boss Anandhu")
    else:
        st.info("Guest mode · general questions")
    st.divider()
    st.markdown("### Voice settings")
    st.markdown("### Voice Input")
audio = mic_recorder(
    start_prompt="🎤 Click to Speak",
    stop_prompt="⏹️ Stop",
    key='mic_input'
)

if audio:
   
    audio_bytes = audio['bytes']
    st.audio(audio_bytes, format='audio/wav')

    language = st.selectbox(
        "Speech language",
        options=["en", "ml", "es", "fr", "de", "ja",⁠⁠]
        format_func=lambda code: {
            "en": "English",
            "hi": "Hindi",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ja": "Japanese",
            "ml": "Malayalam",
        }[code],
    )
    slow = st.toggle("Slower speech", value=False)
    st.caption("Each response replaces the latest `friday.mp3` file.")
    st.divider()
    if st.button("Clear conversation", use_container_width=True):
        reset_chat()
        st.rerun()

st.markdown(
    """
    <div class="hud-wrap">
      <div class="hud" aria-label="F.R.I.D.A.Y. futuristic HUD display">
        <div class="hud-core">
          <div class="hud-label">F.R.I.D.A.Y.</div>
        </div>
      </div>
      <div class="hud-badge">Project FRIDAY - Creator: Anandhu</div>
    </div>
    <div class="hero">
      <div class="eyebrow">Personal intelligence · online</div>
      <h1>Talk to F.R.I.D.A.Y.</h1>
      <p>Ask anything, keep the conversation flowing, and hear every answer in FRIDAY's voice.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.info("Start with a question below. FRIDAY remembers the conversation until you clear it.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("audio"):
            audio_path = Path(message["audio"])
            if audio_path.exists():
                st.audio(audio_path.read_bytes(), format="audio/mp3")

prompt = st.chat_input("Ask FRIDAY anything…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("FRIDAY is thinking…"):
            try:
                if st.session_state.chat is None:
                    (
                        st.session_state.gemini_client,
                        st.session_state.chat,
                    ) = create_chat(st.session_state.access_level)
                response = generate_response(st.session_state.chat, prompt)
                synthesize(response, language, DEFAULT_OUTPUT, slow)
                st.markdown(response)
                st.audio(DEFAULT_OUTPUT.read_bytes(), format="audio/mp3")
                st.download_button(
                    "Download friday.mp3",
                    data=DEFAULT_OUTPUT.read_bytes(),
                    file_name=DEFAULT_OUTPUT.name,
                    mime="audio/mpeg",
                    use_container_width=True,
                )
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                        "audio": str(DEFAULT_OUTPUT),
                    }
                )
            except gTTSError as error:
                st.error(f"Speech generation failed: {error}")
            except Exception as error:
                st.error(f"FRIDAY could not respond: {error}")
