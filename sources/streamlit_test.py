import streamlit as st

from agent_test import launch_rag, rag_chain
from text_to_speech import generate_audio
from speech_to_text import recognize_speech

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

# Utilisation de st.image pour charger le logo local
st.markdown('<div class="center-logo">', unsafe_allow_html=True)
st.image("sources/logo_idfm.png", width=2000)  # Ajustez la largeur selon vos besoins
st.markdown('</div>', unsafe_allow_html=True)

# Ajouter un titre
st.title("Assistant vocal recherche itinéraire")
st.write("Bienvenue sur l'assistant vocal de recherche d'itinéraire!")

if st.button("Enregistrement"):
    recherche_itineraire = recognize_speech()
    st.text_area("Demande :", recherche_itineraire)
    response = launch_rag(rag_chain, recherche_itineraire)
    st.text_area("Réponse :", response)
    audio = generate_audio(response)
    st.audio(audio)
