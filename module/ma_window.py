import tkinter as tk
from tkinter import ttk
import threading
import asyncio
import adbutils
import queue
import logging
import signal
import sys
from .device import Device

class MAWindow:
    def __init__(self, config):
        self.logger = logging.getLogger('MAWindow')
        self.config = config
        self.root = tk.Tk()
        self.root.title("MA")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill='both')
        self.device_threads = []
        self.log_queue = queue.Queue()
        self.create_tabs()
        self.should_stop_all_devices = False

        signal.signal(signal.SIGINT, self.signal_handler)

    def create_tabs(self):
        devices = adbutils.adb.device_list()
        self.logger.info(f"Found {len(devices)} devices.")
        for device in devices:
            if device.serial == '127.0.0.1:16384':
                continue
            self.logger.info(f"Setting up device: {device.serial}")
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=device.serial)
            log_text = tk.Text(tab)
            log_text.pack(expand=1, fill='both')

            device_instance = Device(device.serial, ma_window=self)
            device_instance.logger.addHandler(self.create_log_handler(log_text))
            device_thread = threading.Thread(target=self.device_task, args=(device_instance,))
            device_thread.start()

            self.device_threads.append(device_thread)

        self.root.after(100, self.update_log_text)

    def create_log_handler(self, log_text):
        class TextHandler(logging.Handler):
            def __init__(self, log_text, log_queue):
                super().__init__()
                self.log_text = log_text
                self.log_queue = log_queue

            def emit(self, record):
                log_entry = self.format(record)
                self.log_queue.put((self.log_text, log_entry))  # 使用队列传递日志消息

        handler = TextHandler(log_text, self.log_queue)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        return handler

    def update_log_text(self):
        while not self.log_queue.empty():
            log_text, log = self.log_queue.get()
            log_text.insert(tk.END, log + '\n')
            log_text.see(tk.END)
        self.root.after(100, self.update_log_text)

    def device_task(self, device_instance):
        self.logger.info(f"Starting device task for: {device_instance.serial}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(device_instance.start())
        loop.close()
        self.logger.info(f"Device task for {device_instance.serial} has started.")

    def stop_all_threads(self, event=None):
        self.should_stop_all_devices = True
        for thread in self.device_threads:
            if thread.is_alive():
                thread.join(0)

    def signal_handler(self, sig, frame):
        self.logger.info("Ctrl+C detected. Stopping all devices...")
        self.stop_all_threads()
        sys.exit(0)

    def run(self):
        self.root.mainloop()
