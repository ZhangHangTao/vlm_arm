from utils_robot import *
from utils_asr import *
from utils_vlm import *

import time

def vlm_vqa(PROMPT='请数一数图中中几个方块', input_way='keyboard'):
    # 机械臂归零
    print('机械臂归零')
    #mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    time.sleep(3)
    print('第二步，给出的指令是：', PROMPT)
    top_view_shot(check=False)
    img_path = 'temp/vl_now.jpg'
    result = yi_vision_api(PROMPT, img_path='temp/vl_now.jpg', vlm_option=1)
    print('    多模态大模型调用成功！')
    # print(result)
    GPIO.cleanup()            # 释放GPIO pin channel
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    return result

