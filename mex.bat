@echo off
REM Get the directory of the batch file
set BATCH_DIR=%~dp0

REM Construct the full path to the Python executable
set PYTHON_EXEC=%BATCH_DIR%.venv\Scripts\python.exe

REM Run the Python script using the constructed path
wt -p "{55dee3dc-b1ce-40eb-bb2e-c2a10c342d4b}" --title "H3 HotA Map Editor X" -- "%PYTHON_EXEC%" "%BATCH_DIR%mex\mex.py"
