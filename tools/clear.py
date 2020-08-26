import os
import shutil
from config.conf import SCREENSHOT_DIR
#  TODO(LoveLinXue.com):清理截图还没实现
# 用例执行前清除OutPuts目录的异常截图图片
MAIN_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根目录
OUTPUTS_DIR = os.path.join(SCREENSHOT_DIR, 'screen_capture')  # screen_capture目录

os.chdir(SCREENSHOT_DIR)  # 切换到SCREENSHOT_DIR目录

try:
    shutil.rmtree('screen_capture')  # 清空screen_capture目录下的文件
except FileNotFoundError as e:
    print(f'reports目录不存在，详细信息如下：\n{e}')
for i in os.listdir(SCREENSHOT_DIR):
    if 'png' in i:
        os.unlink(i)

os.chdir(MAIN_DIR)  # 切换到项目根目录

if __name__ == '__main__':
    pass