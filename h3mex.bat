@echo off
REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Check if running in Windows Terminal or VS Code
if not defined WT_SESSION if not "%TERM_PROGRAM%"=="vscode" (
    REM Not in Windows Terminal or VS Code, so launch with wt
    wt -p "{ed82cbca-d0eb-43b9-ab28-3a57145ceb49}" --title "H3 HotA Map Editor X" -- "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%h3mex\h3mex.py" %1
) else (
    REM Already in a terminal, just run with venv python
    "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%h3mex\h3mex.py" %1
)