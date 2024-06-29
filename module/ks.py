import time
import threading
import asyncio
from .image_processor import ImageProcessor
from .utils import *

class Ks:
    def __init__(self, device, config):
        self.device = device
        self.config = config
        self.logger = self.device.logger
        self.run_duration = self.config.get('runDuration', 1) * 60  # 将运行时间从分钟转换为秒
        self.enableAd = self.config.get('watchAd', False)
        self.enableBox = self.config.get('openBox', False)
        # self.enableShopping = self.config.get('goShopping', False)
        self.likeRate = self.config.get('likeRate', 15)
        self.collectRate = self.config.get('collectRate', 10)
        self.followRate = self.config.get('followRate', 5)
        self.processor = ImageProcessor()
        self.packageName = "com.kuaishou.nebula"
        self.packageDir = './bin/package/ks.apk'
        self.stop_timer = None
        # self.home = [60.0, 2172.0, 162.0, 2229.0]
        # self.welfare = [676.0, 2161.0, 840.0, 2235.0]
        self.like = [934, 1176, 1056, 1322]
        self.follow = [952, 1068, 1024, 1114]
        self.collect = [936, 1558, 1036, 1706]
        self.mission = ["openBox", "watchAd", "watchVideo"]#, "goShopping"
        self.current_task_completed = True
        self.standard_width = 1080
        self.standard_height = 2388
        self.scale_width = 1
        self.scale_height = 1

        self.activities = {
            'main': 'HomeActivity',
            'ad': 'AwardVideoPlayActivity',
            'ad_stream': 'ShortSeriesActivity',
            'stream':'LiveSlideActivity'
        }

        # self.stop_announcement_thread = False
        # self.announcement_task = asyncio.create_task(self.handle_announcements())

    # async def close_annoucement(self):
    #     image = self.device.screen_cap()
    #     ocr_results = self.processor.ocr_text(image)
    #
    #     young_float = filter_by_text(ocr_results, ['青少年模式'])
    #     friend_float = filter_by_text(ocr_results, ['朋友推荐'])
    #     guess_you_like_float = filter_by_text(ocr_results, ['猜你喜欢'])
    #     renew = filter_by_text(ocr_results, ['版本更新'])
    #     check_in = filter_by_text(ocr_results, ['立即签到'])
    #     redpack_float = filter_by_text(ocr_results, ['拆红包'])
    #     invite_float = filter_by_text(ocr_results, ['新用户必得'])
    #     click_replay_float = filter_by_text(ocr_results, ['点击重播'])
    #
    #     if len(young_float) > 0:
    #         self.logger.info(f"{self.device.serial} find young float")
    #         young_click = await self.cap_and_find(['知道了'])
    #         self.device.click(young_click[0].rec)
    #
    #     elif len(friend_float) > 0:
    #         self.logger.info(f"{self.device.serial} find friend float")
    #         self.device.press_back()
    #
    #     elif len(guess_you_like_float) > 0:
    #         self.logger.info(f"{self.device.serial} find guess you like float")
    #         self.device.press_back()
    #
    #     elif len(renew) > 0:
    #         self.logger.info(f"{self.device.serial} find renew float")
    #         self.device.press_back()
    #
    #     elif len(check_in) > 0:
    #         self.logger.info(f"{self.device.serial} find checkin float")
    #         self.device.click(check_in[0].rec)
    #         self.random_sleep(2)
    #         await self.click_home()
    #         self.random_sleep(1)
    #         await self.click_welfare()
    #
    #     elif len(redpack_float) > 0:
    #         self.logger.info(f"{self.device.serial} find redpack float")
    #         self.device.press_back()
    #
    #     elif len(invite_float) > 0:
    #         self.logger.info(f"{self.device.serial} find invite float")
    #         self.device.press_back()
    #
    #     elif len(click_replay_float) > 0:
    #         self.logger.info(f"{self.device.serial} find click replay float")
    #         self.device.press_back()
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
            'renew': ['版本更新'],
            'new_user': ["新用户"],
            'young': ['青少年模式'],
            'guess': ['猜你喜欢'],
            'redpack': ['拆红包'],
            'review': ['点击重播'],
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

        guess_popups = filter_by_text(ocr_results, ['猜你喜欢'])
        if len(guess_popups) > 0:
            self.logger.info(f"{self.device.serial} find guess popups")
            self.device.press_back()
            return

        renew_popups = filter_by_text(ocr_results, ['版本更新'])
        if len(renew_popups) > 0:
            self.logger.info(f"{self.device.serial} find renew popups")
            self.device.press_back()
            # click = filter_by_text(ocr_results, ['以后再说'])
            # self.device.click(click[0].rec)
            return

        new_user_popups = filter_by_text(ocr_results, ['新用户'])
        if len(new_user_popups) > 0:
            self.logger.info(f"{self.device.serial} find new user popups")
            self.device.press_back()
            return

        young_popups = filter_by_text(ocr_results, ['青少年模式'])
        if len(young_popups) > 0:
            self.logger.info(f"{self.device.serial} find young popups")
            click = filter_by_text(ocr_results, ['知道了'])
            self.device.click(click[0].rec)
            return

        redpack_popups = filter_by_text(ocr_results, ['拆红包'])
        if len(redpack_popups) > 0:
            self.logger.info(f"{self.device.serial} find redpack popups")
            self.device.press_back()
            return

        review_popups = filter_by_text(ocr_results, ['点击重播'])
        if len(review_popups) > 0:
            self.logger.info(f"{self.device.serial} find review popups")
            self.device.press_back()
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

    #
    # async def init_loc(self):
    #     self.logger.info(f"Init Button Loc")
    #
    #     image = self.device.screen_cap()
    #     ocr_results = self.processor.ocr_text(image)
    #
    #     home_ocr = filter_by_text(ocr_results, ['首页'])
    #     welfare_ocr = filter_by_text(ocr_results, ['去赚钱'])
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
        #     self.logger.info(f"{self.device.serial} did not install Ks.")
        #     self.on_stop()
        #     return
            # if not os.path.exists(self.packageDir):
            #     self.logger.error(f"{self.device.serial} Package path {self.packageDir} does not exist.")
            #     return
            # self.logger.info(f"{self.device.serial} Installing Ks from {self.packageDir}...")
            # self.device.install_app(self.packageDir)
            # self.logger.info(f"{self.device.serial} installed Ks.")

        self.logger.info(f"{self.device.serial} started the Ks task.")
        self.device.close_app(self.packageName)
        self.logger.info(f"{self.device.serial} close {self.packageName}")
        self.random_sleep(2)
        self.device.launch_app(self.packageName)
        self.logger.info(f"{self.device.serial} launch {self.packageName}")

    def on_stop(self):
        try:
            self.logger.info(f"{self.device.serial} stopped the Ks task.")
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
        elif len(filter_by_text(ocr_results, ['金币', '现金'], [])) >= 2:
            self.logger.info(f"{self.device.serial} check in walfare True")
            return True
        else:
            self.logger.info(f"{self.device.serial} check in walfare False")
            return False

    
    async def check_in_home(self):
        # in_home = bool(len(await self.cap_and_find(['关注', '直播间'])))
        # self.logger.info(f"{self.device.serial} check in home {in_home}")
        # return in_home
        ocr_results = await self.get_ocr_results()
        activity = self.device.get_current_activity()
        if not self.activities['main'] in activity :
            self.logger.info(f"{self.device.serial} check in home False")
            return False
        elif len(filter_by_text(ocr_results, ['同城', '生活', '关注'])) >= 3:
            self.logger.info(f"{self.device.serial} check in home True")
            return True
        else:
            self.logger.info(f"{self.device.serial} check in home False")
            return False

    
    async def click_home(self):
        # self.logger.info(f"{self.device.serial} to home")
        # self.device.click(self.home)
        # self.random_sleep(1)
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
        # self.logger.info(f"{self.device.serial} to welfare")
        # self.device.click(self.welfare)
        # self.random_sleep(1)
        await self.click_home()
        self.random_sleep(1)

        ocr_results = await self.get_ocr_results()
        click = filter_by_text(ocr_results, ['去赚钱'])
        if len(click) > 0:
            self.device.click(click[0].rec)
            await self.handle_popups()
        else:
            self.logger.info(f"{self.device.serial} click welfare False")

    
    async def video_like(self):
        if within_percentage(self.likeRate):
            self.logger.info("click like")
            # self.device.click(self.like)
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
                #     stream = await self.cap_and_find(['直播'])
                #     if len(stream) > 0:
                #         self.logger.info(f"{self.device.serial} current in stream")
                #         self.device.swipe_direction('up')
                #     else:
                #         break

                # await self.init_loc()
                # self.random_sleep(2)
                # self.logger.info(f"{self.device.serial}: init done")
                # self.random_sleep(3)

                # self.logger.info(f"{self.device.serial}: close possible float")
                # for i in range(2):
                #     await self.click_home()
                #     self.random_sleep(2)
                #     await self.click_welfare()
                #     self.random_sleep(2)
                # self.logger.info(f"{self.device.serial}: close possible float done")

                self.logger.info(f"{self.device.serial}: start mission")
                while not self.device.should_stop:
                    if self.current_task_completed:
                        await self.do_mission()
                    self.random_sleep(5)
                self.on_stop()
        except Exception as e:
            self.logger.error(f"Exception in run method: {e}")
            self.on_stop()
        # while not self.device.should_stop:
        #     self.calculate_scale_factors()
        #     self.logger.info(f"{self.device.serial} Source Width: {self.device.width}, Height: {self.device.height}")
        #     self.logger.info(f"{self.device.serial} Scale factors - Width: {self.scale_width}, Height: {self.scale_height}")
        #     # if self.device.width != 1080 or self.device.height != 2388:
        #     #     self.logger.info(f"{self.device.serial}: Wrong width or height")
        #     #     self.on_stop()
        #     #     return
        #     self.on_start()
        #     self.stop_timer = threading.Timer(self.run_duration, self.on_stop)
        #     self.stop_timer.setDaemon(False)
        #     self.stop_timer.start()
        #     self.logger.info(f"{self.device.serial} start stop timer, active after {self.run_duration} seconds")
        #     self.random_sleep(5)
        #
        #     while not await self.check_in_home() and not self.device.should_stop:
        #         self.random_sleep(2)
        #
        #
        #     for i in range(5):
        #         stream = await self.cap_and_find(['直播'])
        #         if len(stream) > 0:
        #             self.logger.info(f"{self.device.serial} current in stream")
        #             await self.click_home()
        #         else:
        #             break
        #
        #     await self.init_loc()
        #     self.random_sleep(2)
        #     self.logger.info(f"{self.device.serial}: init done")
        #     self.random_sleep(3)
        #
        #
        #     self.logger.info(f"{self.device.serial}: close possible float")
        #     for i in range(2):
        #         await self.click_home()
        #         self.random_sleep(2)
        #         await self.click_welfare()
        #         self.random_sleep(2)
        #     self.logger.info(f"{self.device.serial}: close possible float done")
        #
        #     self.logger.info(f"{self.device.serial}: start mission")
        #     while not self.device.should_stop:
        #         if self.current_task_completed:
        #             await self.do_mission()
        #         self.random_sleep(5)
        #     self.on_stop()

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
        elif mission == "goShopping":
            self.logger.info("Go Shopping")
            await self.go_shopping()

    async def open_box(self):
        if not self.enableBox:
            self.logger.info(f"{self.device.serial} set open box false")

        if not await self.check_in_walfare():
            await self.click_welfare()

        self.random_sleep(3)

        ocr_results = await self.get_ocr_results()
        box_ocr = filter_by_text(ocr_results,['点就领'])
        if len(box_ocr) == 0:
            self.logger.info(f"{self.device.serial} box cannot open now")
            self.current_task_completed = True
            return

        self.logger.info(f"{self.device.serial} find box loc {box_ocr[0].rec}")
        self.device.click(box_ocr[0].rec)
        self.random_sleep(2)

        watch_ocr = await self.cap_and_find(['看内容'])
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
            stream = await self.cap_and_find(['直播中', '上滑继续'])
            # product_recommend = await self.cap_and_find('上滑继续')

            if len(stream) > 0:
                self.logger.info(f"{self.device.serial} current in stream or product recommend")
                self.device.swipe_direction('up')

            # elif len(product_recommend) > 0:
            #     self.logger.info(f"{self.device.serial} current in product recommend")
            #     self.click_home()
            else:
                break

        click_to_double = await self.cap_and_find(["点击翻倍"])
        if len(click_to_double) > 0:
            self.device.click(click_to_double[0].rec)
            self.logger(f"{self.device.serial} click to double")

        self.random_sleep(random.uniform(7, 19))
        await self.video_like()
        await self.video_follow()
        await self.video_collect()
        #swipe after watch
        self.device.swipe_direction('up')
        self.current_task_completed = True
        self.logger.info(f"{self.device.serial} video watch done")

    async def go_shopping(self):
        if not await self.check_in_walfare():
            await self.click_welfare()
            self.random_sleep(3)
        #swipe to top
        await self.click_welfare()
        self.random_sleep(3)
        # for i in range(5):
        #     self.device.swipe_direction('down')
        #     self.random_sleep(2)
        #swipe 5 times to find watch ad
        for i in range(5):
            self.device.swipe_direction('up')
            shopping_ocr = await self.cap_and_find(['逛街领金币'])
            if len(shopping_ocr) > 0:
                self.logger.info(f'{self.device.serial} shopping find at {shopping_ocr[0].rec}')
                break
        shopping_click_ocr =[]
        for i in range(3):
            shopping_click_ocr = await self.cap_and_find(['去逛街'], True)
            if len(shopping_click_ocr) > 0:
                break
            self.random_sleep(2)
        if len(shopping_click_ocr) == 0:
            self.logger.info(f"{self.device.serial} today's shopping done")
            self.current_task_completed = True
        else:
            self.logger.info(f'{self.device.serial} shopping click find at {shopping_click_ocr[0].rec}')
            self.device.click(shopping_click_ocr[0].rec)
            self.random_sleep(5)
            await self.close_ad()

    async def watch_ad(self):
        if not self.enableAd:
            self.logger.info(f"{self.device.serial} set watch ad false")

        if not await self.check_in_walfare():
            await self.click_welfare()
            self.random_sleep(3)

        #swipe to top
        for i in range(5):
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
            ad_click_ocr = await self.cap_and_find(['领福利'], [], True)
            if len(ad_click_ocr) > 0:
                break
            self.random_sleep(1)

        if len(ad_click_ocr) == 0:
            self.logger.info(f"{self.device.serial} today's ad watched")
            self.current_task_completed = True
        else:
            self.logger.info(f'{self.device.serial} ad click find at {ad_click_ocr[0].rec}')
            self.device.click(ad_click_ocr[0].rec)
            self.random_sleep(3)
            await self.close_ad()

    async def close_ad(self):
        await self.handle_popups()
        activity  = self.device.get_current_activity()
        print(activity)
        if self.activities['ad'] in activity:
            self.logger.info(f"{self.device.serial} in ad")
            i = 0
            #set as failed after 25 tries
            while i < 25 and not self.device.should_stop:
                ocr_results = await self.get_ocr_results()
                get_award = filter_by_text(ocr_results,["已成功领取"])
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
            await self.watch_more()

        elif self.activities['ad_stream'] in activity:
            self.logger.info(f"{self.device.serial} in stream")
            # self.random_sleep(35)
            self.device.press_back()
            while not await self.check_in_walfare() or not await self.check_in_home():
                self.device.press_back()
                self.random_sleep(3)
            # await self.watch_more()
            self.current_task_completed = True
        else:
            self.logger.info(f"{self.device.serial}: unknown ad activity")
            self.current_task_completed = True

    async def watch_more(self):
        # self.device.cap_save()

        ocr_results = await self.get_ocr_results()

        click_get_more = filter_by_text(ocr_results, ['点击额外'])
        download_get_more = filter_by_text(ocr_results, ['下载并'])
        open_get_more = filter_by_text(ocr_results, ['打开并'])
        watch_one_more = filter_by_text(ocr_results, ['再看一个'])
        exit_stream = filter_by_text(ocr_results, ['退出直播间'])

        if len(click_get_more) > 0:
            self.logger.info(f"{self.device.serial}: find click get more, agree")
            agree_click = await self.cap_and_find(["去完成任务"])
            if len(agree_click) > 0:
                self.device.click(agree_click[0].rec)
                self.random_sleep(2)
                click = await self.cap_and_find(["点击额外"])
                if len(click) > 0:
                    self.device.click(click[0].rec)
                    await self.app_back()
                    self.random_sleep(3)
                    self.device.press_back()
                    self.current_task_completed = True
                else:
                    self.logger.info(f"{self.device.serial}: click get more stuck")
                    reject_click = await self.cap_and_find(["放弃奖励"])
                    if len(reject_click) > 0:
                        self.device.click(reject_click[0].rec)
                        self.random_sleep(3)
                        self.current_task_completed = True

        elif len(download_get_more) > 0:
            self.logger.info(f"{self.device.serial}: find download get more, reject")
            reject_click = await self.cap_and_find(["放弃奖励"])
            if len(reject_click) > 0:
                self.device.click(reject_click[0].rec)
                self.random_sleep(3)
                self.current_task_completed = True

        elif len(open_get_more) > 0:
            self.logger.info(f"{self.device.serial}: find open get more, reject")
            reject_click = await self.cap_and_find(["放弃奖励"])
            if len(reject_click) > 0:
                self.device.click(reject_click[0].rec)
                self.random_sleep(3)
                self.current_task_completed = True

        elif len(watch_one_more) > 0:
            one_more_click = await self.cap_and_find(["领取奖励"], ["成功领取"], True)
            if len(one_more_click) > 0:
                self.device.click(one_more_click[0].rec)
                self.logger.info(f"{self.device.serial}: click watch one more")
                self.random_sleep(3)
                await self.close_ad()
            else:
                reject_click = await self.cap_and_find(["放弃奖励","坚持退出"])
                if len(reject_click) > 0:
                    self.device.click(reject_click[0].rec)
                    self.logger.info(f"{self.device.serial}: find watch one more, reject")
                    self.random_sleep(3)
                    self.current_task_completed = True

        elif len(exit_stream) > 0:
            self.logger.info(f"{self.device.serial}: find exit stream, click")
            self.device.click(exit_stream[0].rec)
            self.random_sleep(3)
            self.current_task_completed = True

        else:
            self.logger.info(f"{self.device.serial}: no one more")
            self.current_task_completed = True
            pass

    @staticmethod
    def random_sleep(seconds, scale=1.5):
        sleep_duration = random.uniform(seconds, seconds * scale)
        time.sleep(sleep_duration)