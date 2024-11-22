import streamlit as st
import speech_recognition as sr


def recognize_speech() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            st.info("Enregistrement en cours")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=30)
            st.success("Traitement en cours")
            text = recognizer.recognize_google(audio, language="fr-FR")
        except sr.UnknownValueError:
            return "Je n'ai pas compris, veuillez réessayer."
        except sr.RequestError as e:
            return f"Erreur du service : {e}"

    return text
