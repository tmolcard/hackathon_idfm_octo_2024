import streamlit as st

from gtts import gTTS
from io import BytesIO


def generate_audio(text: str) -> BytesIO:
    st.write('création de l\'audio')
    sound_file = BytesIO()
    tts = gTTS(text, lang='fr')
    tts.write_to_fp(sound_file)

    return sound_file
