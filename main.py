import tkinter as tk
from tkinter import ttk
import threading
import time
import requests


class PeriodicHttpApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Periodic HTTP")

        # 初期設定
        self.interval_option = [10, 30, 60]
        self.default_interval = 60
        self.url_option = ["https://httpbin.org/get"]
        self.default_url = "https://httpbin.org/get"
        self.running = False

        # GUIの設定
        self.setup_gui()

    def setup_gui(self):
        # overall frame
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.rowconfigure([1, 2], pad=20)

        # interval frame
        interval_frame = ttk.Frame(frame)
        interval_frame.grid(row=0, column=0)

        interval_label = ttk.Label(
            interval_frame, text="HTTP Request Interval (s)")
        interval_label.grid(row=0, column=0)

        self.interval_selector = ttk.Combobox(
            interval_frame, values=self.interval_option, state="readonly")
        self.interval_selector.set(self.default_interval)
        self.interval_selector.grid(row=1, column=0)

        # URL frame
        url_frame = ttk.Frame(frame)
        url_frame.grid(row=0, column=1)

        url_label = ttk.Label(url_frame, text="URL")
        url_label.grid(row=0, column=1)

        self.url_selector = ttk.Combobox(
            url_frame, values=self.url_option, state="readonly")
        self.url_selector.set(self.default_url)
        self.url_selector.grid(row=1, column=1)

        # button frame
        start_button = ttk.Button(
            frame, text="Start", command=self.start_requests)
        start_button.grid(row=2, column=0, padx=5)

        stop_button = ttk.Button(
            frame, text="Stop", command=self.stop_requests)
        stop_button.grid(row=2, column=1, padx=5)

        # status label
        self.status_label = ttk.Label(frame, text="Stopped")
        self.status_label.grid(row=3, column=0, columnspan=2)

        # status message
        self.status_message = ttk.Label(frame, text="")
        self.status_message.grid(row=4, column=0, columnspan=2)

    def send_request(self):
        try:
            # Send the request and get the response
            response = requests.get(self.url_selector.get())

            # Raise an exception if an HTTP error occurred
            response.raise_for_status()

            # Display the status code and time if the response is successful
            self.status_message.config(
                text="OK: " + "(Status code: " + str(response.status_code) + ") at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        except requests.exceptions.HTTPError as http_err:
            # If an HTTP error occurs, display the error message and status code
            self.status_message.config(
                text="HTTP Error: " + " (Status code: " + str(http_err.response.status_code) + ") at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

        except Exception as e:
            # If any other error occurs, display the error message
            self.status_message.config(
                text="Error other than HTTP error occured" + " at " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

    def run_periodic_requests(self):
        while self.running:
            self.send_request()
            time.sleep(int(self.interval_selector.get()))

    def start_requests(self):
        # update running flag
        self.running = True

        threading.Thread(target=self.run_periodic_requests,
                         daemon=True).start()

        # invalidates the comboboxes
        self.interval_selector.config(state="disabled")
        self.url_selector.config(state="disabled")

        self.status_label.config(text="Running...")

    def stop_requests(self):
        # update running flag
        self.running = False

        # valid the comboboxes
        self.interval_selector.config(state="readonly")
        self.url_selector.config(state="readonly")

        self.status_label.config(text="Stopped")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = PeriodicHttpApp(root)
    root.mainloop()
