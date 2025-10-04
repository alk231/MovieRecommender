#!/bin/bash

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create Streamlit config
mkdir -p ~/.streamlit/

echo "\
[server]
headless = true
port = \$PORT
enableCORS = false
" > ~/.streamlit/config.toml
