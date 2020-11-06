#!/bin/bash
source ./.env/bin/activate
uvicorn todos.app:app --reload --host=0.0.0.0 --workers=4
