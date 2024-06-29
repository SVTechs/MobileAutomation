import time
import threading
import asyncio
from .image_processor import ImageProcessor
from .utils import *

class Dy:
    def __init__(self, device, config):
        self.device = device
        self.config = config
        self.logger = self.device.logger
        self.run_duration = self.config.get('runDuration', 1) * 60  # 将运行时间从分钟转换为秒
        self.enableAd = self.config.get('watchAd', False)
        self.enableBox = self.config.get('openBox', False)
        self.likeRate = self.config.get('likeRate', 15)
        self.collectRate = self.config.get('collectRate', 10)
        self.followRate = self.config.get('followRate', 5)
        self.processor = ImageProcessor()
        self.packageName = "com.ss.android.ugc.aweme.lite"
        self.packageDir = './bin/package/dy.apk'
        self.stop_timer = None
        # self.home = [53.0, 2157.0, 166.0, 2224.0]
        # self.welfare = [829.0, 159.0, 899.0, 199.0]
        self.like = [940, 1140, 1052, 1278]
        self.follow = [958, 1026, 1012, 1076]
        self.collect = [944, 1542, 1024, 1668]
        self.mission = ["openBox", "watchAd", "watchVideo"]
        self.current_task_completed = True
        self.standard_width = 1080
        self.standard_height = 2388
        self.scale_width = 1
        self.scale_height = 1

        self.activities = {
            'main': 'SplashActivity',
            'ad': 'ExcitingVideoActivity',
            'ad_stream': 'PhotoDetailActivity',
            'stream':'LivePlayActivity'
        }

        # self.stop_announcement_thread = False
        # self.announcement_task = asyncio.create_task(self.handle_announcements())

    # async def close_annoucement(self):
    #     image = self.device.screen_cap()
    #     ocr_results = self.processor.ocr_text(image)
    #     young_float = filter_by_text(ocr_results, ['青少年模式'])
    #     cumulative = filter_by_text(ocr_results, ['获得累计'])
    #     renew = filter_by_text(ocr_results, ['检测到更新'])
    #     reserve = filter_by_text(ocr_results, ['立即预约领'])
    #     reserve_get = filter_by_text(ocr_results, ['预约领金币'])
    #     sing_in = filter_by_text(ocr_results, ['立即签到'])
    #
    #     if len(young_float) > 0:
    #         self.logger.info(f"{self.device.serial} find young float")
    #         young_click= await self.cap_and_find(['关闭'])
    #         self.device.click(young_click[0].rec)
    #
    #     elif len(cumulative) > 0:
    #         self.logger.info(f"{self.device.serial} get cumulative2 float")
    #         i_know_click = await self.cap_and_find(['我知道'])
    #         self.device.click(i_know_click[0].rec)
    #
    #     elif len(renew) > 0:
    #         self.logger.info(f"{self.device.serial} get renew float")
    #         later_click = await self.cap_and_find(['以后再说'])
    #         self.device.click(later_click[0].rec)
    #
    #     # check_in = self.cap_and_find(['立即签到'])
    #     # if len(check_in) > 0:
    #     #     self.logger.info(f"{self.device.serial} find checkin float")
    #     #     self.device.click(check_in[0].rec)
    #     #     self.random_sleep(2)
    #     #     self.device.press_back()
    #     #     self.random_sleep(1)
    #     #     self.click_home()
    #     #     self.random_sleep(1)
    #     #     self.click_welfare()
    #
    #     elif len(reserve) > 0:
    #         self.logger.info(f"{self.device.serial} find reserve float")
    #         self.device.click(reserve[0].rec)
    #         self.random_sleep(2)
    #         await self.click_home()
    #         self.random_sleep(1)
    #         await self.click_welfare()
    #
    #     elif len(reserve_get) > 0:
    #         self.logger.info(f"{self.device.serial} get reserve get float")
    #         earn_click = await self.cap_and_find(['一键领取'])
    #         self.device.click(earn_click[0].rec)
    #
    #     elif len(sing_in) > 0:
    #         self.logger.info(f"{self.device.serial} get sign in float")
    #         self.device.click(sing_in[0].rec)
    #
    # async def handle_announcements(self):
    #     while not self.stop_announcement_thread:
    #         await self.close_annoucement()
    #         await asyncio.sleep(1)

    async def app_back(self):
        self.random_sleep(10)
        self.device.launch_app(self.packageName)

    async def get_ocr_results(self):
        image = self.device.screen_cap()
        ocr_results = self.processor.ocr_text(image)
        return ocr_results

    async def handle_popups(self):
        max_attempts = 3  # 设置最大尝试次数
        attempts = 0
        while attempts < max_attempts:
            if not self.find_popups():
                break
            await self.close_popups()
            attempts += 1
            self.random_sleep(0.2)

    async def find_popups(self):
        popups = {
            'sign': ['立即签到'],
            'friend': ["朋友推荐"],
            'renew': ['检测到更新'],
            'new_user': ["新用户"],
            'young': ['青少年模式'],
            'guess': ['猜你喜欢'],
            'cumulative': ['获得累计'],
            'reserve': ['立即预约领'],
            'reserve_get': ['预约领金币'],
            'ad': ['再看一个']
        }
        ocr_results = await self.get_ocr_results()
        # activity = page.activity()
        # if activity == self.activities['main']:
        for pop_type, feature in popups:
            if len(filter_by_text(ocr_results, feature)) > 0:
                self.logger.info(f"{self.device.serial} find popups")
                return True
        return False

    async def close_popups(self):
        ocr_results = await self.get_ocr_results()
        sign_popups = filter_by_text(ocr_results, ['立即签到'])
        if len(sign_popups) > 0:
            self.logger.info(f"{self.device.serial} find sign popups")
            self.device.click(sign_popups[0].rec)
            return

        friend_popups = filter_by_text(ocr_results, ['朋友推荐'])
        if len(friend_popups) > 0:
            self.logger.info(f"{self.device.serial} find friend popups")
            self.device.press_back()
            return

        renew_popups = filter_by_text(ocr_results, ['检测到更新'])
        if len(renew_popups) > 0:
            self.logger.info(f"{self.device.serial} find renew popups")
            later_click = await self.cap_and_find(['以后再说'])
            self.device.click(later_click[0].rec)
            return

        new_user_popups = filter_by_text(ocr_results, ['新用户'])
        if len(new_user_popups) > 0:
            self.logger.info(f"{self.device.serial} find new user popups")
            self.device.press_back()
            return

        young_popups = filter_by_text(ocr_results, ['青少年模式'])
        if len(young_popups) > 0:
            self.logger.info(f"{self.device.serial} find young popups")
            click= await self.cap_and_find(['关闭'])
            self.device.click(click[0].rec)
            return

        guess_popups = filter_by_text(ocr_results, ['猜你喜欢'])
        if len(guess_popups) > 0:
            self.logger.info(f"{self.device.serial} find guess popups")
            self.device.press_back()
            return

        cumulative_popups = filter_by_text(ocr_results, ['获得累计'])
        if len(cumulative_popups) > 0:
            self.logger.info(f"{self.device.serial} get cumulative popups")
            i_know_click = await self.cap_and_find(['我知道'])
            self.device.click(i_know_click[0].rec)

        reserve_popups = filter_by_text(ocr_results, ['立即预约领'])
        if len(reserve_popups) > 0:
            self.logger.info(f"{self.device.serial} find reserve popups")
            self.device.click(reserve_popups[0].rec)
            self.device.press_back()
            return

        reserve_get_popups = filter_by_text(ocr_results, ['预约领金币'])
        if len(reserve_get_popups) > 0:
            self.logger.info(f"{self.device.serial} find reserve get popups")
            click = await self.cap_and_find(['一键领取'])
            self.device.click(click[0].rec)
            return

        ad_popups = filter_by_text(ocr_results, ['再看一个'])
        if len(ad_popups) > 0:
            self.logger.info(f"{self.device.serial} find stuck ad popups")
            click = filter_by_text(ocr_results, ["放弃奖励","坚持退出"])
            self.device.click(click[0].rec)
            return

    def _scaled_coordinates(self, coord):
        return [
            coord[0] * self.scale_width,
            coord[1] * self.scale_height,
            coord[2] * self.scale_width,
            coord[3] * self.scale_height
        ]

    def calculate_scale_factors(self):
        self.scale_width = self.device.width / self.standard_width
        self.scale_height = self.device.height / self.standard_height

    async def cap_and_find(self, text_list, exclude_list=None, print_results=False):
        ocr_results = await self.get_ocr_results()
        if print_results:
            self.logger.info(ocr_results)
        target_ocr = filter_by_text(ocr_results, text_list, exclude_list)
        return target_ocr

    # async def init_loc(self):
    #     self.logger.info(f"Init Button Loc")
    #
    #     image = self.device.screen_cap()
    #     ocr_results = self.processor.ocr_text(image)
    #
    #     home_ocr = filter_by_text(ocr_results, ['首页'])
    #     welfare_ocr = filter_by_text(ocr_results, ['赚钱'])
    #
    #     if len(home_ocr) > 0:
    #         print(home_ocr[0])
    #         self.home = home_ocr[0].rec
    #
    #     if len(welfare_ocr) > 0:
    #         print(welfare_ocr[0])
    #         self.welfare = welfare_ocr[0].rec
    #     self.logger.info(f"Init Button Loc Done")

    def on_start(self):
        # if not self.device.is_app_installed(self.packageName):
        #     self.logger.info(f"{self.device.serial} did not install Dy.")
        #     self.on_stop()
        #     return
            # if not os.path.exists(self.packageDir):
            #     self.logger.error(f"{self.device.serial} Package path {self.packageDir} does not exist.")
            #     return
            # self.logger.info(f"{self.device.serial} Installing Dy from {self.packageDir}...")
            # self.device.install_app(self.packageDir)
            # self.logger.info(f"{self.device.serial} installed Dy.")

        self.logger.info(f"{self.device.serial} started the Dy task.")
        self.device.close_app(self.packageName)
        self.logger.info(f"{self.device.serial} close {self.packageName}.")
        self.random_sleep(2)
        self.device.launch_app(self.packageName)
        self.logger.info(f"{self.device.serial} launch {self.packageName}.")

    def on_stop(self):
        try:
            self.logger.info(f"{self.device.serial} stopped the Dy task.")
            self.device.close_app(self.packageName)
            if self.stop_timer:
                self.stop_timer.cancel()
            # self.stop_announcement_thread = True
            # if self.announcement_task:
            #     self.announcement_task.cancel()
        except Exception as e:
            self.logger.error(f"Error in on_stop: {e}")

    async def check_in_walfare(self):
        ocr_results = await self.get_ocr_results()
        activity = self.device.get_current_activity()
        if not self.activities['main'] in activity :
            self.logger.info(f"{self.device.serial} check in walfare False")
            return False
        elif len(filter_by_text(ocr_results, ['金币收益', '现金收益'], [])) >= 2:
            self.logger.info(f"{self.device.serial} check in walfare True")
            return True
        else:
            self.logger.info(f"{self.device.serial} check in walfare False")
            return False

    async def check_in_home(self):
        ocr_results = await self.get_ocr_results()
        activity = self.device.get_current_activity()
        if not self.activities['main'] in activity :
            self.logger.info(f"{self.device.serial} check in home False")
            return False
        elif len(filter_by_text(ocr_results, ['商城', '推荐', '关注'])) >= 3:
            self.logger.info(f"{self.device.serial} check in home True")
            return True
        else:
            self.logger.info(f"{self.device.serial} check in home False")
            return False

    async def click_home(self):
        while not await self.check_in_home():
            self.device.press_back()
            await self.handle_popups()

        ocr_results = await self.get_ocr_results()
        click = filter_by_text(ocr_results, ['首页'])
        if len(click) > 0:
            self.device.click(click[0].rec)
            await self.handle_popups()
        else:
            self.logger.info(f"{self.device.serial} click home False")

    async def click_welfare(self):
        await self.click_home()
        self.random_sleep(1)

        ocr_results = await self.get_ocr_results()
        click = filter_by_text(ocr_results, ['赚钱'])
        if len(click) > 0:
            self.device.click(click[0].rec)
            await self.handle_popups()
        else:
            self.logger.info(f"{self.device.serial} click welfare False")

    async def video_like(self):
        if within_percentage(self.likeRate):
            self.logger.info("click like")
            self.device.click(self._scaled_coordinates(self.like))
            self.random_sleep(1)

    async def video_collect(self):
        if within_percentage(self.collectRate):
            self.logger.info("click collect")
            # self.device.click(self.collect)
            self.device.click(self._scaled_coordinates(self.collect))
            self.random_sleep(1)

    async def video_follow(self):
        if within_percentage(self.followRate):
            self.logger.info("click follow")
            # self.device.click(self.follow)
            self.device.click(self._scaled_coordinates(self.follow))
            self.random_sleep(1)

    async def run(self):
        try:
            while not self.device.should_stop:
                self.calculate_scale_factors()

                self.logger.info(f"{self.device.serial} Source Width: {self.device.width}, Height: {self.device.height}")
                self.logger.info(f"{self.device.serial} Scale factors - Width: {self.scale_width}, Height: {self.scale_height}")

                self.on_start()
                self.stop_timer = threading.Timer(self.run_duration, self.on_stop)
                self.stop_timer.setDaemon(False)
                self.stop_timer.start()
                self.logger.info(f"{self.device.serial} start stop timer, active after {self.run_duration} seconds")
                self.random_sleep(5)

                while not await self.check_in_home() and not self.device.should_stop:
                    self.random_sleep(2)

                # for i in range(5):
                #     stream = await self.cap_and_find(['直播间','直播中'])
                #     if len(stream) > 0:
                #         self.logger.info(f"{self.device.serial} current in stream")
                #         # await self.click_home()
                #         self.device.swipe_direction('up')
                #
                # await self.init_loc()
                # self.random_sleep(2)
                # self.logger.info(f"{self.device.serial}: init done")
                # self.random_sleep(1)

                await self.reserve()

                self.logger.info(f"{self.device.serial}: start mission")
                while not self.device.should_stop:
                    if self.current_task_completed:
                        await self.do_mission()
                    self.random_sleep(5)
                self.on_stop()
        except Exception as e:
            self.logger.error(f"Exception in run method: {e}")
            self.on_stop()


    async def do_mission(self):
        mission = random.choice(self.mission)
        self.current_task_completed = False
        if mission == "openBox":
            self.logger.info("Open Box")
            await self.open_box()
        elif mission == "watchAd":
            self.logger.info("Watch Ad")
            await self.watch_ad()
        elif mission == "watchVideo":
            self.logger.info("Watch Video")
            await self.watch_video()

    async def reserve(self):
        if not await self.check_in_walfare():
            await self.click_welfare()
            self.random_sleep(3)

        #swipe to top
        for i in range(7):
            self.device.swipe_direction('down')
            self.random_sleep(0.5)

        # swipe 5 times to daily welfare
        for i in range(5):
            ocr = await self.cap_and_find(['日常任务'])
            if len(ocr) > 0:
                self.logger.info(f'{self.device.serial} daily welfare at {ocr[0].rec}')
                break
            self.device.swipe_direction('up')

        #swipe 5 times to find watch ad
        for i in range(3):
            reserve_ocr = await self.cap_and_find(['预约领'])
            reserved_ocr = await self.cap_and_find(['已预约'])
            if len(reserved_ocr) > 0:
                self.logger.info(f'{self.device.serial} reserved')
                return
            # if len(reserved_ocr) > 0:
            if len(reserve_ocr) > 0:
                self.logger.info(f'{self.device.serial} reserve_ocr find at {reserve_ocr[0].rec}')
                break
            self.device.swipe_direction('up')
        reserve_click_ocr = []
        for i in range(3):
            reserve_click_ocr = await self.cap_and_find(['去预约'], [], True)
            if len(reserve_click_ocr) > 0:
                break
            self.random_sleep(2)
        if len(reserve_click_ocr) == 0:
            self.logger.info(f"{self.device.serial} reserved")
            self.device.press_back()
        else:
            self.logger.info(f'{self.device.serial} reserve click find at {reserve_click_ocr[0].rec}')
            self.device.click(reserve_click_ocr[0].rec)
            self.random_sleep(5)
            reserve2_click_ocr = await self.cap_and_find(['立即预约'])
            if len(reserve2_click_ocr) > 0:
                self.device.click(reserve2_click_ocr[0].rec)
                self.device.press_back()
                self.random_sleep(1)
                self.device.press_back()
            else:
                await self.click_home()

    async def open_box(self):
        if not self.enableBox:
            self.logger.info(f"{self.device.serial} set open box false")

        if not await self.check_in_walfare():
            await self.click_welfare()

        box_ocr = await self.cap_and_find(['开宝箱得金币','点击领'])
        if len(box_ocr) == 0:
            self.logger.info(f"{self.device.serial} box cannot open now")
            self.current_task_completed = True
            return

        self.logger.info(f"{self.device.serial} find box loc {box_ocr[0].rec}")
        self.device.click(box_ocr[0].rec)
        self.random_sleep(2)
        watch_ocr = await self.cap_and_find(['看广告'])
        if len(watch_ocr) == 0:
            self.logger.info(f"{self.device.serial} after open box, no ad to watch")
            await self.click_home()
            self.random_sleep(2)
            self.current_task_completed = True
            return
        else:
            self.device.click(watch_ocr[0].rec)
            self.logger.info(f"{self.device.serial} watch ad")
            self.random_sleep(5)
            await self.close_ad()

    async def watch_video(self):
        if not await self.check_in_home():
            await self.click_home()

        self.logger.info(f"{self.device.serial} video watch start")

        #ignore stream and recommend
        for i in range(10):
            # image = self.device.screen_cap()
            ocr_results = await self.get_ocr_results()

            stream = filter_by_text(ocr_results, ['直播中', '上滑继续'])
            earn_gold = filter_by_text(ocr_results, ['看完视频最高'])

            # stream = await self.cap_and_find(['直播', '上滑继续'])
            # product_recommend = self.cap_and_find('上滑继续')

            if len(stream) > 0:
                self.logger.info(f"{self.device.serial} current in stream")
                self.device.swipe_direction('up')

            elif len(earn_gold) > 0:
                self.logger.info(f"{self.device.serial} current catch earn gold")
                self.random_sleep(31)
                self.device.swipe_direction('up')
            # elif len(product_recommend) > 0:
            #     self.logger.info(f"{self.device.serial} current in product recommend")
            #     self.click_home()
            else:
                break
        # stream_sign = self.cap_and_find('直播中')
        # if len(stream_sign) > 0:
        #     self.logger.info(f"{self.device.serial} current in stream")
        #     self.device.swipe_direction('up')

        click_to_activate = await self.cap_and_find(["点击激活"])
        if len(click_to_activate) > 0:
            self.device.click(click_to_activate[0].rec)
            self.logger(f"{self.device.serial} click to activate")

        self.random_sleep(random.uniform(7, 21))
        await self.video_like()
        await self.video_follow()
        await self.video_collect()
        #swipe after watch
        self.device.swipe_direction('up')
        self.current_task_completed = True
        self.logger.info(f"{self.device.serial} video watch done")

    async def watch_ad(self):
        if not self.enableAd:
            self.logger.info(f"{self.device.serial} set watch ad false")

        if not await self.check_in_walfare():
            await self.click_welfare()
            self.random_sleep(3)

        #swipe to top
        for i in range(7):
            self.device.swipe_direction('down')
            self.random_sleep(0.5)

        # swipe 5 times to daily welfare
        for i in range(5):
            ocr = await self.cap_and_find(['日常任务'])
            if len(ocr) > 0:
                self.logger.info(f'{self.device.serial} daily welfare at {ocr[0].rec}')
                break
            self.device.swipe_direction('up')
            self.random_sleep(1)

        #swipe 5 times to find watch ad
        for i in range(5):
            ad_ocr = await self.cap_and_find(['看广告'])
            if len(ad_ocr) > 0:
                self.logger.info(f'{self.device.serial} ad find at {ad_ocr[0].rec}')
                break
            self.device.swipe_direction('up')
            self.random_sleep(1)

        ad_click_ocr =[]
        for i in range(3):
            ad_click_ocr = await self.cap_and_find(['去领取'], [], True)
            if len(ad_click_ocr) > 0:
                break
            self.random_sleep(1)

        if len(ad_click_ocr) == 0:
            self.logger.info(f"{self.device.serial} today's ad watched")
            self.current_task_completed = True
        else:
            self.logger.info(f'{self.device.serial} ad click find at {ad_click_ocr[0].rec}')
            self.device.click(ad_click_ocr[0].rec)
            self.random_sleep(5)
            await self.close_ad()

    async def close_ad(self):
        #SplashActivity
        #ad
        #ExcitingVideoActivity
        await self.handle_popups()
        activity = self.device.get_current_activity()
        print(activity)
        # if self.activities['ad'] in activity:
        #     self.logger.info(f"{self.device.serial}: get ad")
        #     i = 0
        #     #set as failed after 30 tries
        #     while i < 30 and not self.device.should_stop:
        #         get_award = await self.cap_and_find(["领取成功"])
        #         if len(get_award) > 0:
        #             self.logger.info(f"{self.device.serial}: get award")
        #             break
        #         else:
        #             self.random_sleep(3)
        #             i += 1
        #             self.logger.info(f"find ad award {i}")
        #
        #     get_award = await self.cap_and_find(["领取成功"])
        #     if len(get_award) > 0:
        #         self.device.click(get_award[0].rec)
        #         self.logger.info(f"{self.device.serial}: click get award")
        #         self.random_sleep(3)
        #     else:
        #         self.device.press_back()
        #         get_award = await self.cap_and_find(["领取成功"])
        #         if len(get_award) > 0:
        #             self.device.click(get_award[0].rec)
        #             self.logger.info(f"{self.device.serial}: click get award")
        #             self.random_sleep(3)
        #         else:
        #             self.logger.info(f"{self.device.serial}: ad error")
        #             await self.click_home()
        #             return
        #
        #     cumulative = await self.cap_and_find(["累计获得"])
        #     if len(cumulative) > 0:
        #         self.logger.info(f"{self.device.serial} get cumulative float")
        #         self.device.press_back()
        #         self.random_sleep(5)
        #
        #     await self.watch_more()

        if self.activities['ad'] in activity:
            self.logger.info(f"{self.device.serial} in ad")
            i = 0
            #set as failed after 25 tries
            while i < 25 and not self.device.should_stop:
                ocr_results = await self.get_ocr_results()
                get_award = filter_by_text(ocr_results,["领取成功"])
                # download = filter_by_text(ocr_results,["<"])
                if len(get_award) > 0:
                    self.logger.info(f"{self.device.serial}: get award")
                    break
                # elif len(download) > 0:
                #     self.logger.info(f"{self.device.serial}: get award download")
                #     self.device.press_back()
                else:
                    self.random_sleep(3)
                    i += 1
                    self.logger.info(f"{self.device.serial} find ad award {i}")
            self.device.press_back()
            self.logger.info(f"{self.device.serial}: click get award")
            self.random_sleep(3)

            cumulative = await self.cap_and_find(["累计获得"])
            if len(cumulative) > 0:
                self.logger.info(f"{self.device.serial} get cumulative float")
                self.device.press_back()
                self.random_sleep(2)

            await self.watch_more()

        elif self.activities['ad_stream'] in activity:
            self.logger.info(f"{self.device.serial}: get stream")
            # self.random_sleep(45)
            self.device.press_back()
            while not await self.check_in_walfare() or not await self.check_in_home():
                self.device.press_back()
                self.random_sleep(3)
            self.current_task_completed = True
        else:
            self.logger.info(f"{self.device.serial}: unknown ad activity")
            self.current_task_completed = True

    async def watch_more(self):
        # self.device.cap_save()

        ocr_results = await self.get_ocr_results()

        click_get_more = filter_by_text(ocr_results, ['点击额外'])
        download_get_more = filter_by_text(ocr_results, ['下载并'])
        watch_one_more = filter_by_text(ocr_results, ['再看一个'])

        if len(click_get_more) > 0:
            self.logger.info(f"{self.device.serial}: find click get more, reject")
            reject_click = await self.cap_and_find(["放弃奖励"])
            if len(reject_click) > 0:
                self.device.click(reject_click[0].rec)
                self.random_sleep(5)
                self.current_task_completed = True

        elif len(download_get_more) > 0:
            self.logger.info(f"{self.device.serial}: find download get more, reject")
            reject_click = await self.cap_and_find(["放弃奖励"])
            if len(reject_click) > 0:
                self.device.click(reject_click[0].rec)
                self.random_sleep(5)
                self.current_task_completed = True

        elif len(watch_one_more) > 0:
            one_more_click = await self.cap_and_find(["领取奖励"], ["领取成功"], True)
            if len(one_more_click) > 0:
                self.device.click(one_more_click[0].rec)
                self.logger.info(f"{self.device.serial}: click watch one more")
                self.random_sleep(5)
                await self.close_ad()
            else:
                reject_click = await self.cap_and_find(["放弃奖励","坚持退出"])
                if len(reject_click) > 0:
                    self.device.click(reject_click[0].rec)
                    self.logger.info(f"{self.device.serial}: find watch one more, reject")
                    self.random_sleep(5)
                    self.current_task_completed = True

        else:
            self.logger.info(f"{self.device.serial}: no one more")
            self.current_task_completed = True
            pass

    @staticmethod
    def random_sleep(seconds, scale=1.5):
        sleep_duration = random.uniform(seconds, seconds * scale)
        time.sleep(sleep_duration)