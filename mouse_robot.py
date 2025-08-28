import tkinter as tk
from tkinter import ttk
import pyautogui
import math
import threading
import time

class MouseRobotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("滑鼠機器人")
        
        # 視窗大小設定
        window_width = 450
        window_height = 400
        
        # 獲取螢幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 計算視窗置中位置
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        
        # 設定視窗大小和位置（置中）
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.root.configure(bg='#0f0f23')
        
        # 設定視窗圖示
        try:
            # 嘗試載入圖示，支援打包後的環境
            import os
            import sys
            
            # 獲取資源路徑（支援 PyInstaller 打包）
            if hasattr(sys, '_MEIPASS'):
                # 打包後的環境
                base_path = sys._MEIPASS
            else:
                # 開發環境
                base_path = os.path.dirname(__file__)
                
            icon_path = os.path.join(base_path, 'images', 'Mazinger_Z.png')
            
            if os.path.exists(icon_path):
                icon_image = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(False, icon_image)
                # 保存圖示引用，防止被垃圾回收
                self.icon_image = icon_image
        except Exception as e:
            # 如果圖示載入失敗，使用預設圖示
            print(f"圖示載入失敗: {e}")
            pass
        
        # 建立主框架
        main_frame = tk.Frame(root, bg='#0f0f23')
        main_frame.pack(expand=True, fill='both', padx=30, pady=25)
        
        # 建立標題
        title_label = tk.Label(
            main_frame,
            text="MOUSE ROBOT",
            font=('Consolas', 22, 'bold'),
            bg='#0f0f23',
            fg='#00ffff',
            pady=15
        )
        title_label.pack()
        
        # 建立狀態顯示框架
        status_frame = tk.Frame(main_frame, bg='#0f0f23')
        status_frame.pack(pady=(15, 20))
        
        # 狀態標籤
        status_label = tk.Label(
            status_frame,
            text="狀態：",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#0f0f23',
            fg='#ffffff'
        )
        status_label.pack(side='left', padx=(0, 10))
        
        # 狀態顯示按鈕
        self.status_button = tk.Label(
            status_frame,
            text="停止",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#1a1a2e',
            fg='#ff6b6b',
            relief='sunken',
            width=8,
            height=1,
            bd=3,
            borderwidth=3
        )
        self.status_button.pack(side='left')
        
        # 建立選項框架
        options_frame = tk.Frame(main_frame, bg='#0f0f23')
        options_frame.pack(pady=(0, 20))
        
        # 選項標籤
        options_label = tk.Label(
            options_frame,
            text="轉圈方式：",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#0f0f23',
            fg='#ffffff'
        )
        options_label.pack(side='left', padx=(0, 15))
        
        # 轉圈方式選擇
        self.motion_type = tk.StringVar(value="圓形")
        motion_types = [("圓形", "圓形"), ("心臟線", "心臟線"), ("三角形", "三角形")]
        
        for text, value in motion_types:
            rb = tk.Radiobutton(
                options_frame,
                text=text,
                variable=self.motion_type,
                value=value,
                font=('Microsoft YaHei', 10),
                bg='#0f0f23',
                fg='#00ffff',
                selectcolor='#1a1a2e',
                activebackground='#0f0f23',
                activeforeground='#00ffff'
            )
            rb.pack(side='left', padx=(0, 20))
        
        # 建立啟動按鈕
        self.start_button = tk.Button(
            main_frame,
            text="啟動",
            font=('Microsoft YaHei', 16, 'bold'),
            bg='#2a2a4e',
            fg='#00ff88',
            relief='raised',
            width=15,
            height=2,
            cursor='hand2',
            activebackground='#3a3a5e',
            activeforeground='#00ff88',
            bd=4,
            highlightthickness=3,
            highlightbackground='#00ff88',
            highlightcolor='#00ff88',
            borderwidth=4,
            overrelief='ridge'
        )
        self.start_button.pack(pady=20)
        
        # 建立提示標籤
        hint_label = tk.Label(
            main_frame,
            text="按空白鍵切換啟動/停止狀態",
            font=('Microsoft YaHei', 9),
            bg='#0f0f23',
            fg='#888888'
        )
        hint_label.pack(pady=10)
        
        # 建立關於按鈕（右下角）
        about_button = tk.Button(
            self.root,
            text="?",
            font=('Microsoft YaHei', 12, 'bold'),
            bg='#1a1a2e',
            fg='#888888',
            relief='raised',
            width=2,
            height=1,
            cursor='hand2',
            activebackground='#2a2a3e',
            activeforeground='#00ffff',
            bd=2,
            command=self.show_about
        )
        about_button.place(relx=1.0, rely=1.0, anchor='se', x=-15, y=-15)
        
        # 綁定啟動按鈕點擊事件
        self.start_button.config(command=self.start_mouse_circle)
        
        # 滑鼠轉圈相關變數
        self.is_circling = False
        self.circle_thread = None
        
        # 設定 pyautogui 安全設定
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
        
        # 綁定空白鍵事件
        self.root.bind('<space>', self.toggle_mouse_circle)
        self.root.bind('<Key-space>', self.toggle_mouse_circle)
        
    def show_about(self):
        """顯示關於資訊"""
        import tkinter.messagebox as msgbox
        about_info = """作者資訊

Author: Roger Lo
GitHub: https://github.com/sobadrush/Python_MouseRobot.git
Version: v20250828"""
        msgbox.showinfo("關於", about_info)
        
    def toggle_mouse_circle(self, event=None):
        """切換滑鼠轉圈狀態（空白鍵觸發）"""
        if not self.is_circling:
            self.start_mouse_circle()
        else:
            self.stop_mouse_circle()
    
    def start_mouse_circle(self):
        """開始滑鼠轉圈"""
        if not self.is_circling:
            self.is_circling = True
            self.start_button.config(
                text="停止", 
                bg='#5a2a2a', 
                fg='white',
                activebackground='#6a3a3a',
                relief='sunken',
                bd=3
            )
            self.status_button.config(text="執行中", bg='#1a1a2e', fg='#00ff88')
            self.circle_thread = threading.Thread(target=self.mouse_circle_motion)
            self.circle_thread.daemon = True
            self.circle_thread.start()
        else:
            self.stop_mouse_circle()
    
    def stop_mouse_circle(self):
        """停止滑鼠轉圈"""
        self.is_circling = False
        self.start_button.config(
            text="啟動", 
            bg='#2a2a4e', 
            fg='#00ff88',
            activebackground='#3a3a5e',
            relief='raised',
            bd=4
        )
        self.status_button.config(text="停止", bg='#1a1a2e', fg='#ff6b6b')
    
    def mouse_circle_motion(self):
        """滑鼠轉圈運動"""
        # 獲取螢幕尺寸
        screen_width, screen_height = pyautogui.size()
        
        # 計算螢幕中心點
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # 轉圈半徑（像素）
        radius = 100
        
        # 轉圈速度（每秒轉幾圈）
        circles_per_second = 2
        
        # 計算每步的角度增量
        angle_step = 2 * math.pi / (60 * circles_per_second)  # 60 FPS
        
        angle = 0
        
        while self.is_circling:
            # 根據選擇的轉圈方式計算位置
            motion_type = self.motion_type.get()
            
            if motion_type == "圓形":
                # 圓形：以螢幕中心為圓心的標準圓形
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            elif motion_type == "心臟線":
                # 心臟線方程：調整為正向愛心（頂部朝上）
                # 使用參數方程：x = 16sin³(t), y = 13cos(t) - 5cos(2t) - 2cos(3t) - cos(4t)
                scale = radius / 20  # 縮放因子
                heart_x = 16 * (math.sin(angle) ** 3) * scale
                heart_y = -(13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle)) * scale
                x = center_x + heart_x
                y = center_y + heart_y
            elif motion_type == "三角形":
                # 等邊三角形：幾何中心在螢幕中央
                # 三角形的三個頂點相對於中心點的位置
                triangle_angle = angle % (2 * math.pi)
                
                # 將圓周分成三段，每段對應三角形的一條邊
                segment = int(triangle_angle / (2 * math.pi / 3))
                local_angle = (triangle_angle % (2 * math.pi / 3)) / (2 * math.pi / 3)
                
                # 三角形三個頂點（相對於中心）
                # 頂點向上的等邊三角形
                vertices = [
                    (0, -radius * 2/3),  # 上頂點
                    (radius * math.sqrt(3)/2, radius * 1/3),  # 右下頂點
                    (-radius * math.sqrt(3)/2, radius * 1/3)  # 左下頂點
                ]
                
                # 計算當前邊的起點和終點
                start_vertex = vertices[segment]
                end_vertex = vertices[(segment + 1) % 3]
                
                # 線性插值計算當前位置
                triangle_x = start_vertex[0] + (end_vertex[0] - start_vertex[0]) * local_angle
                triangle_y = start_vertex[1] + (end_vertex[1] - start_vertex[1]) * local_angle
                
                x = center_x + triangle_x
                y = center_y + triangle_y
            
            # 移動滑鼠
            pyautogui.moveTo(int(x), int(y))
            
            # 更新角度
            angle += angle_step
            
            # 控制轉圈速度
            time.sleep(1 / 60)  # 60 FPS
    
    def on_closing(self):
        """視窗關閉時的處理"""
        self.is_circling = False
        if self.circle_thread and self.circle_thread.is_alive():
            self.circle_thread.join(timeout=1)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MouseRobotApp(root)
    
    # 設定視窗關閉事件
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # 啟動主迴圈
    root.mainloop()

if __name__ == "__main__":
    main()
