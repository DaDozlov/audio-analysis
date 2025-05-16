import streamlit as st
import requests
from datetime import datetime
from variables import CONTEXT_SNIPPETS

API_URL = "http://localhost:8000"

st.header("Audio Transcription and Analysis", divider="orange")

with st.form("transcribe_form"):
    uploaded_file = st.file_uploader("Upload MP3/WAV file", type=["mp3", "wav"])
    industry_options = [""] + list(CONTEXT_SNIPPETS.keys())
    industry = st.selectbox("Industry (optional)", options=industry_options, index=0)
    user_id = st.text_input("User ID")
    organisation_id = st.text_input("Organisation ID")
    file_name_input = st.text_input("File name (without extension, optional)")
    model_size = st.selectbox(
        "Whisper model size",
        options=["tiny", "base", "small", "medium", "large"],
        index=["tiny", "base", "small", "medium", "large"].index("small"),
    )
    custom_prompt = st.text_area(
        "Custom Prompt (optional)",
        value="",
        height=200,
        help="Override the default analysis prompt from the backend.",
    )
    submitted = st.form_submit_button("Transcribe and Analyze")

if submitted:
    if not uploaded_file:
        st.error("Please upload an MP3 file.")
    elif not user_id or not organisation_id:
        st.error("Please fill in User ID, Organisation ID.")
    else:
        with st.spinner("Transcribing..."):
            try:
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), "audio/mpeg")
                }
                data = {
                    "industry": industry,
                    "user_id": user_id,
                    "organisation_id": organisation_id,
                    "file_name": file_name_input,
                    "model_size": model_size,
                    "custom_prompt": custom_prompt or None,
                }
                resp = requests.post(f"{API_URL}/transcribe", files=files, data=data)
                resp.raise_for_status()
                result = resp.json()

                st.session_state.transcription = result.get("transcription", "")
                st.session_state.analysis = result.get("analysis", "")
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                txt_filename = f"{timestamp}_{file_name_input}.txt"
                content_sections = [
                    "[Transcription]\n",
                    st.session_state.transcription,
                    "\n\n",
                    "[Analysis]\n",
                    st.session_state.analysis,
                ]
                st.session_state.txt_content = "".join(content_sections)
                st.session_state.txt_filename = txt_filename
                st.session_state.ready = True
            except Exception as e:
                st.error(f"Error calling API: {e}")

# show download and save options
if st.session_state.get("ready"):
    st.subheader("Transcription")
    st.text_area("", st.session_state.transcription, height=200)
    st.subheader("Analysis")
    st.text_area("", st.session_state.analysis, height=200)

    if st.button("Generate Action Suggestion", key="intent_btn"):
        with st.spinner("Browsing web…"):
            try:
                payload = {"transcript": st.session_state.transcription}
                intent_resp = requests.post(f"{API_URL}/intent", data=payload)
                intent_resp.raise_for_status()
                suggestion = intent_resp.json().get("intent", "")
                st.subheader("Suggested actions")
                st.markdown(suggestion)
            except Exception as e:
                st.error(f"Error calling intent endpoint: {e}")

    # download button
    st.download_button(
        label="Download Results as TXT",
        data=st.session_state.txt_content,
        file_name=st.session_state.txt_filename,
        mime="text/plain",
        key="download_btn",
    )

    # save to server button
    if st.button("Save Results to Server", key="save_btn"):
        with st.spinner("Saving to server..."):
            try:
                save_data = {
                    "content": st.session_state.txt_content,
                    "user_id": user_id,
                    "organisation_id": organisation_id,
                    "file_name": st.session_state.txt_filename,
                }
                save_resp = requests.post(
                    f"{API_URL}/save_transcription", data=save_data
                )
                save_resp.raise_for_status()
                save_result = save_resp.json()
                file_path = save_result.get("file_path", "")
                st.success(f"Successfully saved on server: {file_path}")

                try:
                    download_url = f"{API_URL}/transcripts/{file_path}"
                except Exception:
                    pass
            except Exception as e:
                st.error(f"Error calling /save_transcription API: {e}")
