#!/bin/bash
export PATH="/opt/homebrew/bin:$PATH"
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.port=8501 --server.address=0.0.0.0