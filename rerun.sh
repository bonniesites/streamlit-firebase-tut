#!/bin/bash


# Check for updates
outdated=$(poetry show --outdated)

# If updates are available, run the update command
if [ ! -z "$outdated" ]; then
    poetry update
fi

source /Users/drushlopez/Library/Caches/pypoetry/virtualenvs/my-reddit-9QrHQESL-py3.11/bin/activate

streamlit run Home.py