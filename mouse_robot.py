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
        self.root.geometry("600x500")
        self.root.configure(bg='#0f0f23')
        
        # 設定視窗圖示
        self.root.iconbitmap(default='')
        
        # 建立主框架
        main_frame = tk.Frame(root, bg='#0f0f23')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # 建立標題
        title_label = tk.Label(
            main_frame,
            text="MOUSE ROBOT",
            font=('Consolas', 28, 'bold'),
            bg='#0f0f23',
            fg='#00ffff',
            pady=25
        )
        title_label.pack()
        
        # 建立狀態顯示框架
        status_frame = tk.Frame(main_frame, bg='#0f0f23')
        status_frame.pack(pady=(20, 30))
        
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
            relief='flat',
            width=8,
            height=1,
            bd=0
        )
        self.status_button.pack(side='left')
        
        # 建立選項框架
        options_frame = tk.Frame(main_frame, bg='#0f0f23')
        options_frame.pack(pady=(0, 30))
        
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
            font=('Microsoft YaHei', 18, 'bold'),
            bg='#1a1a2e',
            fg='#00ff88',
            relief='flat',
            width=18,
            height=2,
            cursor='hand2',
            activebackground='#2a2a3e',
            activeforeground='#00ff88',
            bd=0,
            highlightthickness=2,
            highlightbackground='#00ff88',
            highlightcolor='#00ff88'
        )
        self.start_button.pack(pady=30)
        
        # 建立提示標籤
        hint_label = tk.Label(
            main_frame,
            text="按空白鍵切換啟動/停止狀態",
            font=('Microsoft YaHei', 10),
            bg='#0f0f23',
            fg='#888888'
        )
        hint_label.pack(pady=20)
        
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
            self.start_button.config(text="停止", bg='#ff4444', fg='white')
            self.status_button.config(text="執行中", bg='#1a1a2e', fg='#00ff88')
            self.circle_thread = threading.Thread(target=self.mouse_circle_motion)
            self.circle_thread.daemon = True
            self.circle_thread.start()
        else:
            self.stop_mouse_circle()
    
    def stop_mouse_circle(self):
        """停止滑鼠轉圈"""
        self.is_circling = False
        self.start_button.config(text="啟動", bg='#1a1a2e', fg='#00ff88')
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
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
            elif motion_type == "心臟線":
                # 心臟線方程：r = a(1 - cos(θ))
                r = radius * (1 - math.cos(angle))
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
            elif motion_type == "三角形":
                # 三角形路徑：每轉一圈分成3段直線
                triangle_angle = (angle * 3) % (2 * math.pi)
                if triangle_angle < 2 * math.pi / 3:
                    # 第一段：從(0,0)到(1,0)
                    progress = triangle_angle / (2 * math.pi / 3)
                    x = center_x + radius * progress
                    y = center_y
                elif triangle_angle < 4 * math.pi / 3:
                    # 第二段：從(1,0)到(0.5,√3/2)
                    progress = (triangle_angle - 2 * math.pi / 3) / (2 * math.pi / 3)
                    x = center_x + radius * (1 - 0.5 * progress)
                    y = center_y + radius * (math.sqrt(3) / 2) * progress
                else:
                    # 第三段：從(0.5,√3/2)到(0,0)
                    progress = (triangle_angle - 4 * math.pi / 3) / (2 * math.pi / 3)
                    x = center_x + radius * (0.5 - 0.5 * progress)
                    y = center_y + radius * (math.sqrt(3) / 2) * (1 - progress)
            
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
