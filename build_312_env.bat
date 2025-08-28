@echo off
chcp 65001 > nul
setlocal

set TARGET_PY=3.12.5
set VENV_NAME=env312

echo ==============================================
echo   建立 Python %TARGET_PY% 環境並打包 (onefile)
echo ==============================================

where py >nul 2>nul
if errorlevel 1 (
  echo ❌ 未找到 py launcher，請先安裝 Windows Python Launcher。
  pause
  exit /b 1
)

echo 🔍 檢查 Python %TARGET_PY% ...
py -%TARGET_PY% -V >nul 2>nul
if errorlevel 1 (
  echo 🚀 下載/安裝 Python %TARGET_PY% (請手動安裝) 或改用已存在版本。
  echo 官方下載：https://www.python.org/downloads/release/python-3125/
  pause
  exit /b 1
)

if exist %VENV_NAME% (
  echo ⚙️  已存在 %VENV_NAME% ，略過建立
) else (
  echo 🛠️  建立虛擬環境 %VENV_NAME% ...
  py -%TARGET_PY% -m venv %VENV_NAME%
)

call %VENV_NAME%\Scripts\activate.bat
python -V

echo 📦 安裝套件...
pip install --upgrade pip >nul
if exist requirements.txt (
  pip install -r requirements.txt
) else (
  pip install pyautogui
)

pip install pyinstaller

if not exist images\Mazinger_Z.ico (
  echo ⚠️  沒找到 .ico，使用 .png 但建議提供 .ico
)

rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul

pyinstaller --clean --noconfirm --windowed --name=MouseRobot --onefile --icon=images\Mazinger_Z.ico --add-data=images;images mouse_robot.py

if exist dist\MouseRobot.exe (
  echo ✅ 建置完成：dist\MouseRobot.exe
) else (
  echo ❌ 建置失敗
)

echo 完成。
pause
endlocal
