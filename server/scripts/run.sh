#!/bin/bash
if [[ -d ./.env ]]; then
    source ./.env/bin/activate
fi
uvicorn todos.app:app --reload --host=$API_SERVER_HOST --port=$API_SERVER_PORT --workers=4
