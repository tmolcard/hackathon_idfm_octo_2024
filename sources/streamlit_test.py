import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
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
st.image("logo1.png", width=200)  # Ajustez la largeur selon vos besoins
st.markdown('</div>', unsafe_allow_html=True)

# Ajouter un titre pour tester
st.title("Assistant vocal recherche itinéraire")
st.write("Bienvenue sur l'assistant vocal de recherche d'itinéraire!")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            st.info("Enregistrement en cours")
            audio = recognizer.listen(source, timeout=5)
            st.success("Traitement en cours")
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.UnknownValueError:
            return "Je n'ai pas compris, veuillez réessayer."
        except sr.RequestError as e:
            return f"Erreur du service : {e}"

# user_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
# st.write('Customized Message:', user_input)

if st.button("Enregistrement"):
    recherche_itineraire = recognize_speech()
    st.text_area("Retranscription :", recherche_itineraire)

    #sound_file = BytesIO()
    #tts = gTTS(recherche_itineraire, lang='en')
    #tts.write_to_fp(sound_file)
