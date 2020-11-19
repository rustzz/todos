#!/bin/bash
if [[ (-z "${API_SERVER_HOST}") || (-z "${API_SERVER_PORT}") ]]; then
    echo "Setup environment exports"
    exit 1
fi

if [[ -d ./.env ]]; then
    source ./.env/bin/activate
else
    python3 -m venv .env
    source ./.env/bin/activate
    python3 -m pip install -r requirements.txt
fi
uvicorn todos.app:app --reload --host=$API_SERVER_HOST --port=$API_SERVER_PORT --workers=4
