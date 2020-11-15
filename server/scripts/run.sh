#!/bin/bash
if [[ -d ./.env ]]; then
    source ./.env/bin/activate
fi
uvicorn todos.app:app --reload --host=0.0.0.0 --port 8000 --workers=4
