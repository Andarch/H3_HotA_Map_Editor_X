@echo off
REM Activate virtual environment
call .venv\Scripts\activate.bat
REM Check if running in Windows Terminal or VS Code
if not defined WT_SESSION if not "%TERM_PROGRAM%"=="vscode" (
    REM Not in Windows Terminal or VS Code, so launch with wt
    wt -p "{55dee3dc-b1ce-40eb-bb2e-c2a10c342d4b}" --title "H3 HotA Map Editor X" -- python h3mex\h3mex.py %1
) else (
    REM Already in a terminal, just run normally
    python h3mex\h3mex.py %1
)