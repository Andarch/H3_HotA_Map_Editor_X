@echo off
REM Get the directory of the batch file
set BATCH_DIR=%~dp0

REM Construct the full path to the Python executable
set PYTHON_EXEC=%BATCH_DIR%.venv\Scripts\python.exe

REM Run the Python script using the constructed path
wt -p "{6421bf4b-462c-4064-9559-d3d87176ce08}" --title "H3 HotA Map Editor X" -- "%PYTHON_EXEC%" "%BATCH_DIR%H3_HotA_MEX.py"