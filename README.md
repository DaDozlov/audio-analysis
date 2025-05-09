# audio-analysis

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

> Make sure you have Python 3.10+ installed.

4. Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

5. Install audio libraries:
```bash
sudo apt-get update && sudo apt-get install ffmpeg
```