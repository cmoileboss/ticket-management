@echo off
cd /d "%~dp0"
python -m uvicorn controller:app --reload