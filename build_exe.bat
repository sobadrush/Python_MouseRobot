@echo off
setlocal ENABLEDELAYEDEXPANSION
chcp 65001 > nul
echo ==============================================
echo         Mouse Robot EXE 建置工具
echo ==============================================
echo.

REM 檢查是否在正確的專案目錄
if not exist "mouse_robot.py" (
    echo ❌ 錯誤：找不到 mouse_robot.py 檔案
    echo 請確保您在正確的專案目錄中執行此批次檔
    pause
    exit /b 1
)

REM 支援 .ico / .png 圖示（優先使用 .ico）
set ICON_PATH=
if exist "images\Mazinger_Z.ico" set ICON_PATH=images\Mazinger_Z.ico
if not defined ICON_PATH if exist "images\Mazinger_Z.png" set ICON_PATH=images\Mazinger_Z.png
if not defined ICON_PATH (
    echo ❌ 錯誤：找不到圖示檔案 images\Mazinger_Z.ico 或 .png
    pause
    exit /b 1
)

echo ✅ 檔案檢查完成
echo.

REM 激活虛擬環境
if exist "env01\Scripts\activate.bat" (
    echo 🔧 激活虛擬環境...
    call env01\Scripts\activate.bat
) else (
    echo ⚠️  警告：找不到虛擬環境，將使用系統 Python
)

REM 檢查 PyInstaller
echo 🔍 檢查 PyInstaller...
python -c "import PyInstaller; print('PyInstaller ok')" 1>nul 2>nul
if errorlevel 1 (
    echo 📦 安裝 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstaller 安裝失敗
        pause
        exit /b 1
    )
)

REM 偵測 Python 版本
for /f "tokens=2 delims= " %%v in ('python -V') do set PYV=%%v
for /f "tokens=1,2,3 delims=." %%a in ("!PYV!") do (
  set PYMAJOR=%%a
  set PYMINOR=%%b
  set PYPATCH=%%c
)
echo � 目前 Python 版本: !PYMAJOR!.!PYMINOR!.!PYPATCH!
set FORCE_ONEFILE=
set MODE=

REM 預設：Python 3.13 以上使用 onedir（較穩定）
if !PYMAJOR! GEQ 3 if !PYMINOR! GEQ 13 (
    echo ⚠️  已偵測 Python 3.13+，onefile 模式可能失敗。
    set MODE=onedir
) else (
    set MODE=onefile
)

echo.
echo 選擇打包模式：
echo   1) 預設模式 (建議)  -> !MODE!
echo   2) 強制 onefile (可能在 3.13 失敗)
echo   3) onedir (資料夾形式)
set /p OPT=請輸入選項 (直接 Enter 使用預設): 
if "!OPT!"=="2" set MODE=onefile
if "!OPT!"=="3" set MODE=onedir
if not defined MODE set MODE=onedir
echo ▶ 使用模式: !MODE!

if /i "!MODE!"=="onefile" (
    set BUILD_CMD=pyinstaller --clean --windowed --noconfirm --name=MouseRobot --icon="%ICON_PATH%" --add-data=images;images mouse_robot.py
) else (
    set BUILD_CMD=pyinstaller --clean --windowed --noconfirm --name=MouseRobot --onedir --icon="%ICON_PATH%" --add-data=images;images mouse_robot.py
)

echo.
echo 🚀 開始建置 EXE 檔案（模式: !MODE!）...
echo.

REM 清理舊檔案
if exist "dist" (
    echo 🧹 清理舊的 dist 資料夾...
    rmdir /s /q dist
)

if exist "build" (
    echo 🧹 清理舊的 build 資料夾...
    rmdir /s /q build
)

REM 建置 EXE/資料夾
echo 🛠️ 指令: !BUILD_CMD!
!BUILD_CMD!

if errorlevel 1 (
    echo.
    echo ❌ 建置失敗！
    pause
    exit /b 1
)

REM 檢查結果
set SUCCESS=0
if /i "!MODE!"=="onefile" if exist "dist\MouseRobot.exe" set SUCCESS=1
if /i "!MODE!"=="onedir" if exist "dist\MouseRobot\MouseRobot.exe" set SUCCESS=1

if !SUCCESS! EQU 1 (
    echo.
    echo ✅ 建置成功！
    echo.
    if /i "!MODE!"=="onefile" (
        echo 📁 輸出檔案：dist\MouseRobot.exe
        for %%A in ("dist\MouseRobot.exe") do set size=%%~zA
        set /a size_kb=!size!/1024
        echo 📊 檔案大小：!size_kb! KB
    ) else (
        echo 📁 輸出資料夾：dist\MouseRobot
        for %%A in ("dist\MouseRobot\MouseRobot.exe") do set size=%%~zA
        set /a size_kb=!size!/1024
        echo 📊 主執行檔大小：!size_kb! KB
    )
    
    echo.
    echo 🎉 建置完成！您可以在 dist 資料夾找到 MouseRobot.exe
    echo ✨ 此檔案可以獨立執行，不需要安裝 Python
    echo.
    echo 是否要測試執行程式？ (y/N)
    set /p test_run=
    
    if /i "%test_run%"=="y" (
        echo 🏃 執行測試...
        if /i "!MODE!"=="onefile" (
            start "" "dist\MouseRobot.exe"
        ) else (
            start "" "dist\MouseRobot\MouseRobot.exe"
        )
    )
) else (
    echo ❌ 建置失敗或輸出檔案不存在
)

echo.
echo 按任意鍵結束...
pause >nul
endlocal
