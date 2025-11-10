@echo off
title H3 HotA Map Editor X
cd /d "%~dp0"

REM Check if running in Windows Terminal or VS Code
if defined WT_SESSION goto run_python
if "%TERM_PROGRAM%"=="vscode" goto run_python

REM Not in Windows Terminal or VS Code, so launch with wt
wt -p "{ed82cbca-d0eb-43b9-ab28-3a57145ceb49}" --title "H3 HotA Map Editor X"
goto end

:run_python
REM Already in a terminal, just run with venv python
.venv\Scripts\python.exe h3mex\h3mex.py %*
exit

:end