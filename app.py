import streamlit as st
import os
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
    st.markdown("### Engine status")

    # Get primary model from config for display
    primary_model = os.getenv("PRIMARY_MODEL", "openai/gpt-4o")
    model_display = primary_model.replace("openai/", "OpenAI ").replace("anthropic/", "Anthropic ")

    st.markdown(
        f"**Model:** {model_display}<br/>"
        f"**Search Broker:** Tavily API<br/>"
        f"**Fidelity Law:** Active",
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
