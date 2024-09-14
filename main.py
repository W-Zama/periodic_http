import tkinter as tk
from tkinter import ttk
import threading
import time
import requests

# ネット通信を行う関数
def send_request():
    try:
        response = requests.get('https://httpbin.org/get')
        print("Request sent. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

# 60秒ごとに通信を行うループ
def run_periodic_requests():
    while running:
        send_request()
        time.sleep(60)

# 開始ボタンの処理
def start_requests():
    global running
    running = True
    threading.Thread(target=run_periodic_requests, daemon=True).start()
    status_label.config(text="Running...")

# 停止ボタンの処理
def stop_requests():
    global running
    running = False
    status_label.config(text="Stopped")

# GUIの設定
app = tk.Tk()
app.title("Network Request Monitor")

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

start_button = ttk.Button(frame, text="Start", command=start_requests)
start_button.grid(row=0, column=0, padx=5)

stop_button = ttk.Button(frame, text="Stop", command=stop_requests)
stop_button.grid(row=0, column=1, padx=5)

status_label = ttk.Label(frame, text="Stopped")
status_label.grid(row=1, column=0, columnspan=2)

running = False

app.mainloop()
