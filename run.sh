#!/bin/bash
# Script to run the todo application with proper encoding

cd "$(dirname "$0")"

# Set the Python IO encoding to handle Unicode characters properly
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m src.todo_app
