import streamlit as st
import os
import hmac
from dotenv import load_dotenv
from src.ui.views import ArenaViews

# Load environment configuration
load_dotenv()

# Set up page configurations
st.set_page_config(
    page_title="Cloud Bloodbath - Multi-Agent Tug-of-War",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS stylesheet
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS styling file {file_name} not found.")

local_css("src/static/style.css")


def _check_password() -> bool:
    """
    Gates the whole app behind a single shared password (APP_PASSWORD in the
    environment) - not per-user accounts, just a doorway. If APP_PASSWORD
    isn't set, the gate stays open so a fresh checkout without a .env still
    runs locally.
    """
    if st.session_state.get("authenticated"):
        return True

    app_password = os.getenv("APP_PASSWORD")
    if not app_password:
        return True

    st.markdown(
        "<h1 style='font-family: \"Cinzel Decorative\", serif; text-align: center; "
        "color: var(--ember); margin-bottom: 6px; text-shadow: 0 0 18px rgba(217,164,65,0.35);'>"
        "CLOUD BLOODBATH</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color: var(--bone-dim); font-family: \"IBM Plex Mono\", monospace; "
        "letter-spacing: 0.04em; margin-bottom: 24px;'>The gates are sealed. "
        "Speak the password to enter the war room.</p>",
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        with st.form("login_form"):
            entered_password = st.text_input(
                "Password", type="password", label_visibility="collapsed", placeholder="Password"
            )
            submitted = st.form_submit_button("Enter the Arena", width="stretch")

        if submitted:
            if hmac.compare_digest(entered_password, app_password):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Wrong password. The gates remain sealed.")

    return False


if not _check_password():
    st.stop()

# Initialize Session states
if "battle_state" not in st.session_state:
    st.session_state["battle_state"] = "setup"

if "app_tab" not in st.session_state:
    st.session_state["app_tab"] = "Arena"

# Render sidebar navigation
with st.sidebar:
    st.markdown(
        "<h2 style='font-family: \"Cinzel Decorative\", serif; color: var(--ember); "
        "text-align: center; margin-bottom: 20px; text-shadow: 0 0 14px rgba(217,164,65,0.3);'>"
        "CLOUD REALMS</h2>",
        unsafe_allow_html=True
    )

    st.session_state["app_tab"] = st.radio(
        "Navigate the realms:",
        ["Arena", "Codex History"],
        index=0 if st.session_state["app_tab"] == "Arena" else 1
    )

    st.markdown("---")
    st.markdown(
        "<h4 style='font-family: \"Cinzel Decorative\", serif; color: var(--ember); "
        "letter-spacing: 0.03em; margin-bottom: 10px;'>The Council's instruments</h4>",
        unsafe_allow_html=True
    )

    # Get primary model from config for display
    primary_model = os.getenv("PRIMARY_MODEL", "openai/gpt-4o")
    model_display = primary_model.replace("openai/", "OpenAI ").replace("anthropic/", "Anthropic ")

    def _instrument_row(label: str, value: str, color: str) -> str:
        return (
            f"<div style='margin-bottom: 8px;'>"
            f"<span style='color: {color}; font-family: \"IBM Plex Mono\", monospace; "
            f"font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;'>{label}</span><br/>"
            f"<span style='color: var(--bone); font-family: \"IBM Plex Mono\", monospace; font-size: 13px;'>{value}</span>"
            f"</div>"
        )

    st.markdown(
        _instrument_row("Oracle consulted", model_display, "var(--cyan)")
        + _instrument_row("Scouts draw from", "Tavily API", "var(--ember)")
        + _instrument_row("Fidelity Law", "Upheld", "var(--blood)"),
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(
        "<p class='skeleton-note'> Bloodsport of Cloud Factions</p>",
        unsafe_allow_html=True
    )

views = ArenaViews()

# Route Views
if st.session_state["app_tab"] == "Arena":
    if st.session_state["battle_state"] == "setup":
        views.render_setup_view()
    elif st.session_state["battle_state"] == "fighting":
        views.render_fight_view()
else:
    views.render_codex_view()
