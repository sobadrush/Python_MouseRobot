#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
建置 Mouse Robot 為 exe 檔案的腳本
"""

import os
import subprocess
import sys
import shutil

def build_exe():
    """建置 exe 檔案"""
    
    # 確認必要檔案存在
    if not os.path.exists('mouse_robot.py'):
        print("❌ 找不到 mouse_robot.py 檔案")
        return False
        
    if not os.path.exists('images/Mazinger_Z.png'):
        print("❌ 找不到 images/Mazinger_Z.png 圖示檔案")
        return False
    
    print("🚀 開始建置 Mouse Robot exe 檔案...")
    
    # 清理舊的建置檔案
    if os.path.exists('dist'):
        print("🧹 清理舊的 dist 資料夾...")
        shutil.rmtree('dist')
    
    if os.path.exists('build'):
        print("🧹 清理舊的 build 資料夾...")
        shutil.rmtree('build')
    
    # PyInstaller 指令
    cmd = [
        'pyinstaller',
        '--onefile',                           # 單一檔案
        '--windowed',                          # 不顯示命令列視窗
        '--name=MouseRobot',                   # 輸出檔案名稱
        '--icon=images/Mazinger_Z.png',        # 圖示檔案
        '--add-data=images;images',            # 包含 images 資料夾
        '--distpath=dist',                     # 輸出資料夾
        'mouse_robot.py'                       # 主程式檔案
    ]
    
    try:
        print("📦 執行 PyInstaller...")
        print(f"指令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 建置成功！")
            
            # 檢查輸出檔案
            exe_path = os.path.join('dist', 'MouseRobot.exe')
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path)
                size_mb = size / (1024 * 1024)
                print(f"📁 輸出檔案: {exe_path}")
                print(f"📊 檔案大小: {size_mb:.1f} MB")
                return True
            else:
                print("❌ 找不到輸出的 exe 檔案")
                return False
        else:
            print("❌ 建置失敗！")
            print(f"錯誤訊息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 建置過程發生錯誤: {e}")
        return False

if __name__ == "__main__":
    print("=== Mouse Robot EXE 建置工具 ===")
    success = build_exe()
    
    if success:
        print("\n🎉 建置完成！")
        print("✨ 您可以在 dist 資料夾中找到 MouseRobot.exe")
        print("🚀 現在可以將 exe 檔案複製到任何地方獨立執行！")
    else:
        print("\n💥 建置失敗，請檢查錯誤訊息")
        
    input("\n按 Enter 鍵結束...")
