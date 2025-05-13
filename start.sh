#!/usr/bin/env bash
# start.sh

uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload &

streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0