import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"

st.title("Audio Transcription and Analysis")

uploaded_file = st.file_uploader("Upload MP3 file", type=["mp3"])

# input fields for required form data
industry = st.text_input("Industry (optional)")
user_id = st.text_input("User ID")
organisation_id = st.text_input("Organisation ID")
file_name = st.text_input("Desired file name (without extension)")

if st.button("Transcribe and Analyze"):
    if uploaded_file is None:
        st.error("Please upload an MP3 file.")
    elif not user_id or not organisation_id or not file_name:
        st.error("Please fill in User ID, Organisation ID, and File Name.")
    else:
        with st.spinner("Transcribing..."):
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), "audio/mpeg")
            }
            data = {
                "industry": industry,
                "user_id": user_id,
                "organisation_id": organisation_id,
                "file_name": file_name
            }
            try:
                response = requests.post(f"{API_URL}/transcribe", files=files, data=data)
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                st.error(f"Error calling API: {e}")
                st.stop()

        # display results
        transcription = result.get("transcription", "")
        analysis = result.get("analysis", "")
        st.subheader("Transcription")
        st.text_area("", transcription, height=200)
        st.subheader("Analysis")
        st.text_area("", analysis, height=200)

        # prepare structured TXT content
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        txt_filename = f"{timestamp}_{file_name}.txt"
        content_sections = [
            "[Tasks]\n",
            transcription + "\n\n",
            "[Decisions]\n",
            analysis + "\n",
        ]
        txt_content = "".join(content_sections)

        st.download_button(
            label="Download Results as TXT",
            data=txt_content,
            file_name=txt_filename,
            mime="text/plain"
        )