@echo off
setlocal

set "AI_DIR=E:\AI"
set "COMFY_DIR=E:\AI\ComfyUI"
set "COMFY_BAT=E:\AI\ComfyUI\run_nvidia_gpu.bat"
set "ST_DIR=E:\AI\SillyTavern"
set "ST_BAT=E:\AI\SillyTavern\Start.bat"

title Start AI Stack

echo Checking files...

if not exist "%COMFY_BAT%" (
    echo ERROR: "%COMFY_BAT%" not found
    pause
    exit /b 1
)

if not exist "%ST_BAT%" (
    echo ERROR: "%ST_BAT%" not found
    pause
    exit /b 1
)

echo Checking Ollama...
call :check_port 11434

if errorlevel 1 (
    if not exist "E:\AI\Ollama\ollama.exe" (
        echo ERROR: E:\AI\Ollama\ollama.exe not found
    ) else (
        echo Starting Ollama...
        start "Ollama" /min "E:\AI\Ollama\ollama.exe" serve
        ping 127.0.0.1 -n 6 >nul

        call :check_port 11434
        if errorlevel 1 (
            echo Ollama started, but port 11434 is not responding yet.
        ) else (
            echo Ollama is running.
        )
    )
) else (
    echo Ollama is already running.
)

echo Checking ComfyUI...
call :check_port 8188

if errorlevel 1 (
    echo Starting ComfyUI...
    start "ComfyUI" /D "%COMFY_DIR%" /min cmd.exe /c run_nvidia_gpu.bat
) else (
    echo ComfyUI is already running.
)

echo Checking SillyTavern...
call :check_port 8000

if errorlevel 1 (
    echo Starting SillyTavern...
    start "SillyTavern" /min cmd.exe /c call "%ST_BAT%"
) else (
    echo SillyTavern is already running.
)

echo.
echo Startup commands sent.
echo For mobile access use: http://YOUR-IP-ADDRESS:8000
echo Get your IP via command: ipconfig
exit /b 0

:check_port
powershell -NoProfile -Command "try { $c=New-Object Net.Sockets.TcpClient; $c.Connect('127.0.0.1',%~1); $c.Close(); exit 0 } catch { exit 1 }" >nul 2>&1
exit /b %errorlevel%