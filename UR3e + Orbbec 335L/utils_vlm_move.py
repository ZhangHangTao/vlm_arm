# utils_vlm_move.py
# 同济子豪兄 2024-5-22
# 输入指令，多模态大模型识别图像，吸泵吸取并移动物体

# print('神行太保：能看懂“图像”、听懂“人话”的机械臂')

from utils_robot import *
from utils_asr import *
from utils_vlm import *

import time





def calculate_arm_height(camera_depth, camera_depth_max=414.5, arm_z_max=237.24):
    """
    将相机的深度信息转换为机械臂的 Z 坐标。
    :param camera_depth: 相机检测的深度值
    :param camera_depth_max: 相机检测的最大深度（例如 414.5）
    :param arm_z_max: 机械臂的最大 Z 坐标（例如 237.24）
    :return: 机械臂的 Z 坐标
    """
    return (1 - camera_depth / camera_depth_max) * arm_z_max

   






def vlm_move(PROMPT='帮我把绿色方块放在小猪佩奇上', input_way='keyboard'):
    '''
    多模态大模型识别图像，吸泵吸取并移动物体
    input_way：speech语音输入，keyboard键盘输入
    '''

    print('多模态大模型识别图像，吸泵吸取并移动物体')
    
    # 机械臂归零
    print('机械臂归零')
    #mc.send_angles([0, 0, 0, 0, 0, 0], 50)
    time.sleep(3)
    
    ## 第一步：完成手眼标定
    print('第一步：完成手眼标定')
    
    ## 第二步：发出指令
    # PROMPT_BACKUP = '帮我把绿色方块放在小猪佩奇上' # 默认指令
    
    # if input_way == 'keyboard':
    #     PROMPT = input('第二步：输入指令')
    #     if PROMPT == '':
    #         PROMPT = PROMPT_BACKUP
    # elif input_way == 'speech':
    #     record() # 录音
    #     PROMPT = speech_recognition() # 语音识别
    print('第二步，给出的指令是：', PROMPT)
    
    ## 第三步：拍摄俯视图
    print('第三步：拍摄俯视图')
    top_view_shot(check=False)
    
    ## 第四步：将图片输入给多模态视觉大模型
    print('第四步：将图片输入给多模态视觉大模型')
    img_path = 'temp/vl_now.jpg'
    
    n = 1
    while n < 5:
        result = qw_vision_api(PROMPT, img_path='temp/vl_now.jpg', vlm_option=0)
        print(result)
        try:
            print('    尝试第 {} 次访问多模态大模型'.format(n))
            result = qw_vision_api(PROMPT, img_path='temp/vl_now.jpg', vlm_option=0)
            print('    多模态大模型调用成功！')
            #print(result)
            print('第五步：视觉大模型输出结果后处理和可视化')
            START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER, START_Z_CAMERA, END_Z_CAMERA = post_processing_viz(result, img_path, check=True)
            if START_X_CENTER==-1 or not (20 <= START_Z_CAMERA <= 420 and 20 <= END_Z_CAMERA <= 420): 
            	capture_and_save_image()
            	n = 1
    	        continue
            else:
    	        break
        except Exception as e:
            capture_and_save_image()
            print('    多模态大模型返回数据结构错误，再尝试一次', e)
            n += 1
    	
    ## 第五步：视觉大模型输出结果后处理和可视化
    
    
    ## 第六步：手眼标定转换为机械臂坐标
    print('第六步：手眼标定，将像素坐标转换为机械臂坐标')
    # 起点，机械臂坐标


    START_X_MC, START_Y_MC = eye2hand(START_X_CENTER, START_Y_CENTER)
    # 终点，机械臂坐标
    END_X_MC, END_Y_MC = eye2hand(END_X_CENTER, END_Y_CENTER)
    
    ## 第七步：吸泵吸取移动物体
    print('第七步：吸泵吸取移动物体')
    start_height = calculate_arm_height(START_Z_CAMERA)
    end_height = calculate_arm_height(END_Z_CAMERA)
    pump_move(
        XY_START=[START_X_MC, START_Y_MC],
        HEIGHT_START=start_height,
        XY_END=[END_X_MC, END_Y_MC],
        HEIGHT_END=end_height, 
    )
    ## 第八步：收尾
    print('第八步：任务完成')
    #GPIO.cleanup()            # 释放GPIO pin channel
    cv2.destroyAllWindows()   # 关闭所有opencv窗口
    # exit()


