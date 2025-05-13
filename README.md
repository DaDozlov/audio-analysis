# audio-analysis

A standalone Python application and small web UI for uploading MP3/WAV files, transcribing speech via OpenAI Whisper, and running a AI-powered (LLM) analysis to extract Tasks, Decisions, Questions, Insights, Deadlines, Participants, Follow-ups, Risks, and Agenda Items. Results are served via a FastAPI backend and a Streamlit frontend, and can be saved to disk for auditing or further review.

## Installation (for Linux OS)

1. Clone the repository:

```bash
git clone git@github.com:DaDozlov/audio-analysis.git
cd audio-analysis
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure you have Python 3.11+ installed.

4. Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

5. Install audio libraries:
```bash
sudo apt-get update && sudo apt-get install ffmpeg
```

## Configuration

The app is running by default with Whisper small model and ollama llama3.2:1b (with 1b params). You can directly change your Whisper model using the UI (the last field). If you want to adapt your ollama model, simply change the model in the **config.py** file and run **ollama pull your_model** instead of the default one.

## Quick‑start
```bash
ollama pull llama3.2:1b
uvicorn app.main:app --reload
streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0
```

## Quick‑start frontend and backend at the same time
```bash
ollama pull llama3.2:1b
chmod +x start.sh
./start.sh
```
