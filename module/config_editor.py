import yaml
import os
from .ma_window import *

class ConfigEditor:
    def __init__(self, config_path=None):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        self.config_path = config_path
        self.config = self.load_config()
        self.root = tk.Tk()
        # self.root.iconbitmap = ''
        self.root.title("基础设置")
        self.create_widgets()

    def load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def save_config(self):
        with open(self.config_path, 'w') as file:
            yaml.safe_dump(self.config, file)

    def update_config(self):
        # self.config['params']['port'] = self.service_port_var.get()

        self.config['tasks']['Ks']['enabled'] = self.ks_enabled_var.get()
        self.config['tasks']['Ks']['openBox'] = self.ks_openBox_var.get()
        self.config['tasks']['Ks']['runDuration'] = int(self.ks_runDuration_var.get())
        self.config['tasks']['Ks']['sleepDuration'] = int(self.ks_sleepDuration_var.get())
        self.config['tasks']['Ks']['watchAd'] = self.ks_watchAd_var.get()
        self.config['tasks']['Ks']['likeRate'] = int(self.ks_likeRate_var.get())
        self.config['tasks']['Ks']['collectRate'] = int(self.ks_collectRate_var.get())
        self.config['tasks']['Ks']['followRate'] = int(self.ks_followRate_var.get())

        self.config['tasks']['Dy']['enabled'] = self.dy_enabled_var.get()
        self.config['tasks']['Dy']['runDuration'] = int(self.dy_runDuration_var.get())
        self.config['tasks']['Dy']['sleepDuration'] = int(self.dy_sleepDuration_var.get())
        self.config['tasks']['Dy']['watchAd'] = self.dy_watchAd_var.get()
        self.config['tasks']['Dy']['openBox'] = self.dy_openBox_var.get()
        self.config['tasks']['Dy']['likeRate'] = int(self.dy_likeRate_var.get())
        self.config['tasks']['Dy']['collectRate'] = int(self.dy_collectRate_var.get())
        self.config['tasks']['Dy']['followRate'] = int(self.dy_followRate_var.get())

        self.config['tasks']['Hg']['enabled'] = self.hg_enabled_var.get()
        self.config['tasks']['Hg']['runDuration'] = int(self.hg_runDuration_var.get())
        self.config['tasks']['Hg']['sleepDuration'] = int(self.hg_sleepDuration_var.get())
        self.config['tasks']['Hg']['watchAd'] = self.hg_watchAd_var.get()
        self.config['tasks']['Hg']['openBox'] = self.hg_openBox_var.get()
        self.config['tasks']['Hg']['likeRate'] = int(self.hg_likeRate_var.get())
        self.config['tasks']['Hg']['collectRate'] = int(self.hg_collectRate_var.get())

        self.config['tasks']['Fqct']['enabled'] = self.fqct_enabled_var.get()
        self.config['tasks']['Fqct']['runDuration'] = int(self.fqct_runDuration_var.get())
        self.config['tasks']['Fqct']['sleepDuration'] = int(self.fqct_sleepDuration_var.get())
        self.config['tasks']['Fqct']['watchAd'] = self.fqct_watchAd_var.get()
        self.config['tasks']['Fqct']['openBox'] = self.fqct_openBox_var.get()

        self.save_config()

    def start(self):
        self.update_config()
        self.save_config()
        self.root.withdraw()
        ma_window = MAWindow(self.config)
        ma_window.run()


    def create_widgets(self):
        # # Basic Para
        # basic_frame = ttk.LabelFrame(self.root, text="基础参数")
        # basic_frame.grid(row=0, column=0, padx=10, pady=10)
        #
        # self.service_port_var = tk.StringVar(value=self.config['params']['port'])
        #
        # ttk.Label(basic_frame, text="服务端口").grid(row=0, column=0, sticky=tk.W)
        # ttk.Entry(basic_frame, textvariable=self.service_port_var).grid(row=0, column=1)

        # Ks Task
        ks_frame = ttk.LabelFrame(self.root, text="快手极速版")
        ks_frame.grid(row=0, column=1, padx=10, pady=10)

        self.ks_enabled_var = tk.BooleanVar(value=self.config['tasks']['Ks']['enabled'])
        self.ks_openBox_var = tk.BooleanVar(value=self.config['tasks']['Ks']['openBox'])
        self.ks_runDuration_var = tk.StringVar(value=self.config['tasks']['Ks']['runDuration'])
        self.ks_sleepDuration_var = tk.StringVar(value=self.config['tasks']['Ks']['sleepDuration'])
        self.ks_watchAd_var = tk.BooleanVar(value=self.config['tasks']['Ks']['watchAd'])
        self.ks_likeRate_var = tk.StringVar(value=self.config['tasks']['Ks']['likeRate'])
        self.ks_collectRate_var = tk.StringVar(value=self.config['tasks']['Ks']['collectRate'])
        self.ks_followRate_var = tk.StringVar(value=self.config['tasks']['Ks']['followRate'])

        ttk.Checkbutton(ks_frame, text="启用", variable=self.ks_enabled_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(ks_frame, text="运行时长").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(ks_frame, textvariable=self.ks_runDuration_var).grid(row=1, column=1)
        ttk.Label(ks_frame, text="休眠时长").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(ks_frame, textvariable=self.ks_sleepDuration_var).grid(row=2, column=1)
        ttk.Checkbutton(ks_frame, text="看广告", variable=self.ks_watchAd_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(ks_frame, text="开箱子", variable=self.ks_openBox_var).grid(row=4, column=0, sticky=tk.W)
        ttk.Label(ks_frame, text="点赞率").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(ks_frame, textvariable=self.ks_likeRate_var).grid(row=5, column=1)
        ttk.Label(ks_frame, text="收藏率").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(ks_frame, textvariable=self.ks_collectRate_var).grid(row=6, column=1)
        ttk.Label(ks_frame, text="关注率").grid(row=7, column=0, sticky=tk.W)
        ttk.Entry(ks_frame, textvariable=self.ks_followRate_var).grid(row=7, column=1)

        # Dy Task
        dy_frame = ttk.LabelFrame(self.root, text="抖音极速版")
        dy_frame.grid(row=0, column=2, padx=10, pady=10)

        self.dy_enabled_var = tk.BooleanVar(value=self.config['tasks']['Dy']['enabled'])
        self.dy_runDuration_var = tk.StringVar(value=self.config['tasks']['Dy']['runDuration'])
        self.dy_sleepDuration_var = tk.StringVar(value=self.config['tasks']['Dy']['sleepDuration'])
        self.dy_watchAd_var = tk.BooleanVar(value=self.config['tasks']['Dy']['watchAd'])
        self.dy_openBox_var = tk.BooleanVar(value=self.config['tasks']['Dy']['openBox'])
        self.dy_likeRate_var = tk.StringVar(value=self.config['tasks']['Dy']['likeRate'])
        self.dy_collectRate_var = tk.StringVar(value=self.config['tasks']['Dy']['collectRate'])
        self.dy_followRate_var = tk.StringVar(value=self.config['tasks']['Dy']['followRate'])

        ttk.Checkbutton(dy_frame, text="启用", variable=self.dy_enabled_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(dy_frame, text="运行时长").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(dy_frame, textvariable=self.dy_runDuration_var).grid(row=1, column=1)
        ttk.Label(dy_frame, text="休眠时长").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(dy_frame, textvariable=self.dy_sleepDuration_var).grid(row=2, column=1)
        ttk.Checkbutton(dy_frame, text="看广告", variable=self.dy_watchAd_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(dy_frame, text="开箱子", variable=self.dy_openBox_var).grid(row=4, column=0, sticky=tk.W)
        ttk.Label(dy_frame, text="点赞率").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(dy_frame, textvariable=self.dy_likeRate_var).grid(row=5, column=1)
        ttk.Label(dy_frame, text="收藏率").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(dy_frame, textvariable=self.dy_collectRate_var).grid(row=6, column=1)
        ttk.Label(dy_frame, text="关注率").grid(row=7, column=0, sticky=tk.W)
        ttk.Entry(dy_frame, textvariable=self.dy_followRate_var).grid(row=7, column=1)

        # Hg Task
        hg_frame = ttk.LabelFrame(self.root, text="红果短剧")
        hg_frame.grid(row=0, column=3, padx=10, pady=10)

        self.hg_enabled_var = tk.BooleanVar(value=self.config['tasks']['Hg']['enabled'])
        self.hg_runDuration_var = tk.StringVar(value=self.config['tasks']['Hg']['runDuration'])
        self.hg_sleepDuration_var = tk.StringVar(value=self.config['tasks']['Hg']['sleepDuration'])
        self.hg_watchAd_var = tk.BooleanVar(value=self.config['tasks']['Hg']['watchAd'])
        self.hg_openBox_var = tk.BooleanVar(value=self.config['tasks']['Hg']['openBox'])
        self.hg_likeRate_var = tk.StringVar(value=self.config['tasks']['Hg']['likeRate'])
        self.hg_collectRate_var = tk.StringVar(value=self.config['tasks']['Hg']['collectRate'])

        ttk.Checkbutton(hg_frame, text="启用", variable=self.hg_enabled_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(hg_frame, text="运行时长").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(hg_frame, textvariable=self.hg_runDuration_var).grid(row=1, column=1)
        ttk.Label(hg_frame, text="休眠时长").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(hg_frame, textvariable=self.hg_sleepDuration_var).grid(row=2, column=1)
        ttk.Checkbutton(hg_frame, text="看广告", variable=self.hg_watchAd_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(hg_frame, text="开箱子", variable=self.hg_openBox_var).grid(row=4, column=0, sticky=tk.W)
        ttk.Label(hg_frame, text="点赞率").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(hg_frame, textvariable=self.hg_likeRate_var).grid(row=5, column=1)
        ttk.Label(hg_frame, text="收藏率").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(hg_frame, textvariable=self.hg_collectRate_var).grid(row=6, column=1)

        # Fqct Task
        fqct_frame = ttk.LabelFrame(self.root, text="番茄畅听")
        fqct_frame.grid(row=0, column=4, padx=10, pady=10)

        self.fqct_enabled_var = tk.BooleanVar(value=self.config['tasks']['Fqct']['enabled'])
        self.fqct_runDuration_var = tk.StringVar(value=self.config['tasks']['Fqct']['runDuration'])
        self.fqct_sleepDuration_var = tk.StringVar(value=self.config['tasks']['Fqct']['sleepDuration'])
        self.fqct_watchAd_var = tk.BooleanVar(value=self.config['tasks']['Fqct']['watchAd'])
        self.fqct_openBox_var = tk.BooleanVar(value=self.config['tasks']['Fqct']['openBox'])

        ttk.Checkbutton(fqct_frame, text="启用", variable=self.fqct_enabled_var, ).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(fqct_frame, text="运行时长").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(fqct_frame, textvariable=self.fqct_runDuration_var).grid(row=1, column=1)
        ttk.Label(fqct_frame, text="休眠时长").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(fqct_frame, textvariable=self.fqct_sleepDuration_var).grid(row=2, column=1)
        ttk.Checkbutton(fqct_frame, text="看广告", variable=self.fqct_watchAd_var).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(fqct_frame, text="开箱子", variable=self.fqct_openBox_var).grid(row=4, column=0, sticky=tk.W)

        ttk.Button(self.root, text="启动", command=self.start).grid(row=1, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.mainloop()
