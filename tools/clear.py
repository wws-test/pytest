﻿import os
import shutil
from config.conf import SCREENSHOT_DIR, BASE_DIR
from tools.logger import Log

os.chdir(SCREENSHOT_DIR)  # 切换到SCREENSHOT_DIR目录

log = Log().logger
def picclear():
    # try:
    #     shutil.rmtree('allure-results')  # 清空screen_capture目录下的文件,整个文件夹都删了，不可取
    # except FileNotFoundError as e:
    #     print(f'screen_capture目录不存在，详细信息如下：\n{e}')
    for i in os.listdir(SCREENSHOT_DIR):
        if i.endswith(".png"):
            # print(os.listdir(SCREENSHOT_DIR))
            os.remove(os.path.join(SCREENSHOT_DIR, i))
            log.info("删除文件夹")
            if not os.path.exists(SCREENSHOT_DIR):
                os.makedirs("screen_capture")
                log.info("重新创建文件夹")


os.chdir(BASE_DIR)  # 切换到项目根目录

if __name__ == '__main__':
    picclear()
