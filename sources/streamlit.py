import streamlit as st
from streamlit_geolocation import streamlit_geolocation

from sources.agent.agent import invoke_agent
from sources.converter.text_to_speech import generate_audio
from sources.converter.speech_to_text import recognize_speech

st.markdown(
    """
    <style>
    .center-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if location := streamlit_geolocation():
    if location.get('longitude') is not None:
        user_location = ';'.join([str(location.get('longitude')), str(location.get('latitude'))])
    else:
        user_location = "Inconnue"

# Utilisation de st.image pour charger le logo local
st.markdown('<div class="center-logo">', unsafe_allow_html=True)
st.image("sources/images/logo_idfm.png", width=2000)  # Ajustez la largeur selon vos besoins
st.markdown('</div>', unsafe_allow_html=True)

# Ajouter un titre
st.title("Assistant vocal recherche itinéraire")
st.write("Bienvenue sur l'assistant vocal de recherche d'itinéraire!")


if 'button' not in st.session_state:
    st.session_state.button = False


def click_button():
    st.session_state.button = True


st.button("Enregistrement", on_click=click_button)

if st.session_state.button:
    user_input = recognize_speech()
    st.text_area("Retranscription :", user_input)
    agent_response = invoke_agent(user_input, user_location)
    audio = generate_audio(agent_response)
    st.audio(audio, autoplay=True)

    st.session_state.button = False
