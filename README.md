# 滑鼠機器人程式

這是一個使用 Python tkinter 建立的視窗程式，可以控制滑鼠游標進行轉圈運動。

## 功能特色

- **狀態顯示**: 即時顯示程式執行狀態（執行中/停止）
- **啟動/停止按鈕**: 控制滑鼠轉圈運動的開始和停止
- **多種轉圈方式**: 支援圓形、心臟線、三角形三種不同的運動軌跡
- **活動類型選擇**: 提供三種不同程度的防螢幕保護程式活動模式
- **現代科技風格**: 採用深色主題，具有強烈的現代感和科技感介面

## 安裝需求

1. 推薦 Python 3.12（若用 3.13 將只能穩定使用 onedir 模式）
2. 安裝所需套件：

```bash
pip install -r requirements.txt
```

## 使用方法

1. 執行程式：
```bash
python mouse_robot.py
```

2. 選擇轉圈方式：
   - **圓形**：傳統的圓形軌跡
   - **心臟線**：浪漫的心臟線軌跡
   - **三角形**：幾何三角形軌跡

3. 選擇活動類型：
   - **僅移動**：安靜模式，只移動滑鼠游標，不會干擾其他程式
   - **滑鼠移動+點擊**：標準模式，移動滑鼠並進行左鍵點擊
   - **滑鼠+鍵盤**：強效模式，同時模擬滑鼠和鍵盤活動，最有效的防螢幕保護程式方式

3. 開始/停止滑鼠轉圈有兩種方式：
   - **點擊按鈕**：點擊 "啟動" 按鈕開始，再次點擊（顯示 "停止"）停止
   - **按空白鍵**：按空白鍵可以切換啟動/停止狀態

4. 關閉視窗結束程式

**活動類型選擇建議**：
- **安靜環境**（如辦公室、圖書館）：選擇「僅移動」
- **一般使用**：選擇「滑鼠移動+點擊」
- **強制防鎖定**：選擇「滑鼠+鍵盤」

## 安全功能

- 程式使用 `pyautogui.FAILSAFE = True`，將滑鼠移動到螢幕左上角可以緊急停止
- 轉圈運動在背景執行緒中進行，不會阻塞主視窗

## 技術細節

- 使用 tkinter 建立 GUI 介面
- 使用 pyautogui 控制滑鼠移動和鍵盤模擬
- 使用 threading 處理背景任務
- 支援空白鍵快捷鍵切換啟動/停止狀態
- 支援三種不同的運動軌跡算法（圓形、心臟線、三角形）
- 支援三種活動類型（僅移動、滑鼠移動+點擊、滑鼠+鍵盤）
- 轉圈運動以 60 FPS 的頻率執行，每秒轉 2 圈
- 轉圈半徑為 100 像素
- 採用現代深色科技風格設計，具有強烈的視覺衝擊力

## 注意事項

- 請確保在安全的環境中使用此程式
- 轉圈過程中請勿強制關閉程式，建議使用停止按鈕停止
- 程式會自動檢測螢幕尺寸並計算中心點
- 選擇「滑鼠+鍵盤」模式時，會模擬按下 Shift 鍵，請確保不會干擾其他程式
- 建議根據使用環境選擇合適的活動類型

## 打包為可執行檔（Windows）

目前預設與穩定做法：
- Python 3.13：使用 onedir 模式（整個資料夾）
- 想要單一 exe：改用 Python 3.12 再打包 onefile



### 手動打包（自訂）
啟動現有環境（例：`env01`）：
```bash
env01\Scripts\activate
pip install pyinstaller
pyinstaller --clean --windowed --onedir --name=MouseRobot --icon=images\Mazinger_Z.ico --add-data="images;images" mouse_robot.py
```
（若已在 Python 3.12 環境且要單檔）
```bash
pyinstaller --clean --windowed --onefile --name=MouseRobot --icon=images\Mazinger_Z.ico --add-data="images;images" mouse_robot.py
```

### 參數重點
| 參數 | 說明 |
|------|------|
| --onedir | 產生資料夾（穩定） |
| --onefile | 產生單一 exe（3.13 可能失敗） |
| --windowed | 隱藏 console 視窗 |
| --icon | 指定 .ico 圖示 |
| --add-data="images;images" | 打包資源資料夾 |

### 分發建議
| 模式 | 內容 | 分發方式 |
|------|------|-----------|
| onedir | `dist/MouseRobot/` 整包 | 壓縮整個資料夾再發送 |
| onefile | `dist/MouseRobot.exe` | 直接送出檔案 |

首次啟動時可能會有短暫初始化延遲。

## 打包相容性 / 疑難排解

目前使用 Python 3.13 搭配 PyInstaller 6.15.0 在 `--onefile` 模式下可能出現：

```
Could not load PyInstaller's embedded PKG archive
或 視窗：錯誤 380 無法正確連結自某庫
```

這是 Python 3.13 onefile 未完全相容的狀況。建議：

1. Python 3.13：請使用 `--onedir`（已驗證可行）。
2. 需要單檔：改用 **Python 3.12 + --onefile**。
3. 圖示建議使用 **.ico**（已提供 `images/Mazinger_Z.ico`）。

### 快速使用 onedir 模式
```bash
pyinstaller --clean --windowed --onedir --name=MouseRobot --icon=images\Mazinger_Z.ico --add-data="images;images" mouse_robot.py
```
發佈時請整個 `dist/MouseRobot` 資料夾一起複製。

### 仍出錯時排查清單
| 問題 | 檢查項 | 解法 |
|------|--------|------|
| 執行時彈錯誤找不到 PKG | Python 版本 | 降到 3.12 再打包 |
| 沒有圖示 | 使用 PNG | 轉成 .ico (256x256) |
| 仍開啟黑色 console | 缺少 --windowed | 在命令加入 `--windowed` |
| 資料夾模式 OK 單檔不行 | onefile 解壓失敗 | 使用 onedir 或降版本 |

### 為什麼 onedir 正常、onefile 失敗？
onefile 會把程式與依賴打包進壓縮存檔，自我解壓到暫存資料夾再執行。Python 版本更新（3.13）導致部分 bootloader / 內部 layout 尚未完全同步，故會出現 embedded PKG 錯誤；onedir 則不需要解壓步驟，較少踩到這個問題。

---
更新日期：2025-08-31
