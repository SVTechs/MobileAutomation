@echo off
echo starting...

set "PROJECT_DIR=%~dp0"
set "PYTHON_HOME=%PROJECT_DIR%bin\python"

set PATH=%PYTHON_HOME%;%PYTHON_HOME%\Scripts;%PATH%

%PYTHON_HOME%\python.exe %PROJECT_DIR%\module\get_device_info.py %PROJECT_DIR%
pause
