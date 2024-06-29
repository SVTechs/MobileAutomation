@echo off
echo starting...

set "PROJECT_DIR=%~dp0"
set "PYTHON_HOME=%PROJECT_DIR%bin\python"

set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%

echo Checking and installing dependencies...
%PYTHON_HOME%\python.exe -m pip install --upgrade pip
%PYTHON_HOME%\python.exe -m pip install -r %PYTHON_HOME%\requirements.txt

pause
