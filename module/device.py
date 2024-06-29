import time
import adbutils
# from apscheduler.schedulers.background import BackgroundScheduler
import cv2
import uiautomator2 as u2
import yaml
import asyncio
from datetime import datetime, timedelta
import atexit
import os
import random
import numpy as np
from .utils import get_logger, random_rectangle_point, ensure_int, ensure_time, point2str
from .ks import Ks
from .dy import Dy
from .hg import Hg
from .fqct import Fqct
from .timer import Timer

class Device:
    def __init__(self, serial, config_path='./config.yaml', ma_window=None):
        self.serial = serial
        self.device = adbutils.adb.device(serial)
        self.logger = get_logger(serial)
        self.d = u2.connect(serial)
        # self.scheduler = BackgroundScheduler()
        self.width = self.d.info['displayWidth']
        self.height = self.d.info['displayHeight']

        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self.tasks = self.config.get('tasks', {})
        self.logger.info(self.config)

        self.current_task = None  # 当前正在执行的任务
        self.should_stop = False  # 用于指示是否应停止当前任务
        self.ma_window = ma_window

        # atexit.register(self.shutdown_scheduler)
        self.screen_folder = './screen'
        if not os.path.exists(self.screen_folder):
            os.makedirs(self.screen_folder)

    def check_stop_signal(self):
        if self.ma_window and self.ma_window.should_stop_all_devices:
            self.should_stop = True

    def click(self, rec, control_check=False):
        if control_check:
            pass
        x, y = random_rectangle_point(rec)
        x, y = ensure_int(x, y)
        self.logger.info(f'Click {point2str(x, y)} @ {rec}')
        self.d.click(x, y)

    def multi_click(self, rec, n, interval=(0.1, 0.2)):
        click_timer = Timer(0.1)
        for _ in range(n):
            remain = ensure_time(interval) - click_timer.current()
            if remain > 0:
                time.sleep(remain)
            click_timer.reset()
            self.click(rec, control_check=False)

    def long_click(self, rec, duration=(1, 1.2)):
        x, y = random_rectangle_point(rec)
        x, y = ensure_int(x, y)
        duration = ensure_time(duration)
        self.logger.info(f'Click {point2str(x, y)} @ {rec}, {duration}')
        self.d.long_click(x, y, duration=duration)

    def swipe(self, p1, p2, duration=(0.1, 0.2), name='SWIPE', distance_check=True):
        p1, p2 = ensure_int(p1, p2)
        duration = ensure_time(duration)
        self.logger.info(f'Swipe {point2str(*p1)} -> {point2str(*p2)}, {duration}')

        if distance_check:
            if np.linalg.norm(np.subtract(p1, p2)) < 10:
                self.logger.info('Swipe distance < 10px, dropped')
                return
        self.d.swipe(*p1, *p2, duration=duration)

    def swipe_direction(self, direction):
        width, height = self.width, self.height
        horizontal_offset = random.uniform(-width * 0.1, width * 0.1)
        vertical_offset = random.uniform(-height * 0.1, height * 0.1)

        if direction == 'up':
            x1 = random.uniform(100, width - 100)
            y1 = random.uniform(height * 0.6, height * 0.8)
            x2 = x1 + horizontal_offset
            y2 = random.uniform(height * 0.2, height * 0.4)
        elif direction == 'down':
            x1 = random.uniform(100, width - 100)
            y1 = random.uniform(height * 0.2, height * 0.4)
            x2 = x1 + horizontal_offset
            y2 = random.uniform(height * 0.6, height * 0.8)
        elif direction == 'left':
            x1 = random.uniform(width * 0.6, width * 0.8)
            y1 = random.uniform(100, height - 100)
            x2 = random.uniform(width * 0.2, width * 0.4)
            y2 = y1 + vertical_offset
        elif direction == 'right':
            x1 = random.uniform(width * 0.2, width * 0.4)
            y1 = random.uniform(100, height - 100)
            x2 = random.uniform(width * 0.6, width * 0.8)
            y2 = y1 + vertical_offset
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

        self.logger.info(f"Swiping from ({x1}, {y1}) to ({x2}, {y2}) in direction {direction}")

        self.swipe((x1, y1), (x2, y2))

    def press_home(self):
        self.d.press("home")

    def press_back(self):
        self.d.press("back")

    def screen_cap(self):
        return self.d.screenshot(format='opencv')

    def cap_save(self):
        # 获取当前的所有截图文件
        screenshots = [f for f in os.listdir(self.screen_folder) if f.startswith(self.serial)]
        screenshots = sorted(screenshots, key=lambda x: int(x.split('-')[-1].split('.')[0]))

        # 超过30个文件时从第一个开始覆盖
        if len(screenshots) >= 30:
            oldest_file_index = int(screenshots[0].split('-')[-1].split('.')[0])
            new_file_index = oldest_file_index
            os.remove(os.path.join(self.screen_folder, screenshots[0]))
            screenshots.pop(0)
        else:
            new_file_index = len(screenshots) + 1

        screenshot_path = os.path.join(self.screen_folder, f"{self.serial}-{new_file_index}.png")
        self.d.screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved as {screenshot_path}")

    def textinput(self, text):
        self.d.set_fastinput_ime(True)
        self.d.send_keys(text)
        self.d.set_fastinput_ime(False)

    def key_input(self, keycode):
        self.d.press(keycode)

    def is_app_installed(self, package_name):
        return package_name in self.d.app_list()

    def install_app(self, apk_path):
        self.d.app_install(apk_path)

    def launch_app(self, package_name):
        self.d.app_start(package_name)

    def close_app(self, package_name):
        self.d.app_stop(package_name)

    def get_current_app(self):
        try:
            return self.d.app_current()['package']
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_current_activity(self):
        try:
            return self.d.app_current()['activity']
        except Exception as e:
            self.logger.error(f"Error getting current activity: {e}")
            return None

    async def start(self):
        self.logger.info(f"Starting device: {self.serial}")
        task_classes = {'Hg': Hg, 'Ks': Ks, 'Dy': Dy, "Fqct": Fqct}
        # {'Ks': Ks, 'Dy': Dy, 'Hg': Hg}
        start_time = datetime.now() + timedelta(seconds=10)

        async def task_wrapper(task_class, task_config):
            self.current_task = task_class(self, task_config)
            await self.current_task.run()
            self.current_task = None

        tasks = []
        for task_name, task_config in self.tasks.items():
            if not task_config.get('enabled', False):
                self.logger.info(f"Task {task_name} is disabled and will be skipped.")
                continue

            run_duration = task_config.get('runDuration', 15)  # 默认运行时长为15分钟
            sleep_duration = task_config.get('sleepDuration', 1)  # 默认休息时长为1分钟

            task_class = task_classes.get(task_name)
            if task_class:
                # self.scheduler.add_job(task_wrapper, 'date', run_date=start_time, args=[task_class, task_config])
                task = asyncio.create_task(task_wrapper(task_class, task_config))
                tasks.append(task)
                self.logger.info(f"Scheduled {task_name} to run at {start_time}.")
                start_time += timedelta(minutes=run_duration + sleep_duration)
            else:
                self.logger.error(f"Task class for {task_name} not found.")

        # self.scheduler.start()
        # self.logger.info("Scheduler started.")

        try:
            while not self.should_stop:
                self.check_stop_signal()
                await asyncio.sleep(1)
            # self.shutdown_scheduler()
        except (KeyboardInterrupt, SystemExit):
            self.should_stop = True
            if self.current_task:
                self.current_task.on_stop()

        for task in tasks:
            await task
            # self.shutdown_scheduler()
    #
    # def shutdown_scheduler(self):
    #     if self.scheduler.running:
    #         self.scheduler.shutdown()
    #
    #     self.should_stop = True
    #     if self.current_task:
    #         self.current_task.on_stop()
