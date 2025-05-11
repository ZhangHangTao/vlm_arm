# utils_vlm.py
# 同济子豪兄 2024-5-22
# 多模态大模型、可视化

print('导入视觉大模型模块')
import cv2
import numpy as np
from pyorbbecsdk import Config, OBSensorType, Pipeline
from PIL import Image, ImageDraw, ImageFont
import time
import os


MIN_DEPTH = 20  # 20mm
MAX_DEPTH = 1000  # 10000mm


from utils_tts import *             # 语音合成模块
# 导入中文字体，指定字号
font = ImageFont.truetype('asset/SimHei.ttf', 26)

from API_KEY import *

OUTPUT_VLM = ''

# 系统提示词
SYSTEM_PROMPT_CATCH = '''
我即将说一句给机械臂的指令，你帮我从这句话中提取出起始物体和终止物体，并从这张图中分别找到这两个物体左上角和右下角的像素坐标，你必须保证定位的精准性，输出json数据结构,从{开始, 记住一定不要输出包含```json的开头或结尾。如果你收到的指令是移动一个一样的重复物体（例如，移动纸巾到纸巾上），那么你输出两个一样的纸巾物体和坐标。

例如，如果我的指令是：请帮我把红色方块放在房子简笔画上。
你输出这样的格式：
{
 "start":"红色方块",
 "start_xyxy":[[102,505],[324,860]],
 "end":"房子简笔画",
 "end_xyxy":[[300,150],[476,310]]
}
只回复json本身即可，不要回复其它内容
我现在的指令是：
'''

SYSTEM_PROMPT_VQA = '''
告诉我图片中每个物体的名称、类别和作用。每个物体用一句话描述。

例如：
连花清瘟胶囊，药品，治疗感冒。
盘子，生活物品，盛放东西。
氯雷他定片，药品，治疗抗过敏。

我现在的指令是：
'''


# Yi-Vision调用函数
import openai
from openai import OpenAI
import base64


def qw_vision_api(PROMPT='帮我把红色方块放在钢笔上', img_path='temp/vl_now.jpg', vlm_option=0):

    '''
    零一万物大模型开放平台，yi-vision视觉语言多模态大模型API
    '''
    if vlm_option == 0:
        SYSTEM_PROMPT = SYSTEM_PROMPT_CATCH
    elif vlm_option==1:
        SYSTEM_PROMPT = SYSTEM_PROMPT_VQA


    client = OpenAI(
        api_key=QW_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
    
    # 向大模型发起请求
    completion = client.chat.completions.create(
      model="qwen-vl-max-2024-11-19",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT + PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    #OUTPUT_VLM = str(completion.choices[0].message.content.strip())
    # 解析大模型返回结果
    if vlm_option == 0:
        result = eval(completion.choices[0].message.content.strip())
        print(result)
    elif vlm_option==1:
        result=completion.choices[0].message.content.strip()
        print(result)
        tts(result)                     # 语音合成，导出wav音频文件
        play_wav('temp/tts.wav')          # 播放语音合成音频文件S
    
    return result
    
    
def yi_vision_api(PROMPT='帮我把红色方块放在钢笔上', img_path='temp/vl_now.jpg', vlm_option=0):

    '''
    零一万物大模型开放平台，yi-vision视觉语言多模态大模型API
    '''
    if vlm_option == 0:
        SYSTEM_PROMPT = SYSTEM_PROMPT_CATCH
    elif vlm_option==1:
        SYSTEM_PROMPT = SYSTEM_PROMPT_VQA


    client = OpenAI(
        api_key=YI_KEY,
        base_url="https://api.lingyiwanwu.com/v1"
    )
    
    # 编码为base64数据
    with open(img_path, 'rb') as image_file:
        image = 'data:image/jpeg;base64,' + base64.b64encode(image_file.read()).decode('utf-8')
    
    # 向大模型发起请求
    completion = client.chat.completions.create(
      model="yi-vision-solution",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": SYSTEM_PROMPT + PROMPT
            },
            {
              "type": "image_url",
              "image_url": {
                "url": image
              }
            }
          ]
        },
      ]
    )
    
    #OUTPUT_VLM = str(completion.choices[0].message.content.strip())
    # 解析大模型返回结果
    if vlm_option == 0:
        result = eval(completion.choices[0].message.content.strip())
    elif vlm_option==1:
        result=completion.choices[0].message.content.strip()
        print(result)
        tts(result)                     # 语音合成，导出wav音频文件
        play_wav('temp/tts.wav')          # 播放语音合成音频文件S
    
    return result
   

class TemporalFilter:
    def __init__(self, alpha):
        self.alpha = alpha
        self.previous_frame = None

    def process(self, frame):
        if self.previous_frame is None:
            result = frame
        else:
            result = cv2.addWeighted(frame, self.alpha, self.previous_frame, 1 - self.alpha, 0)
        self.previous_frame = result
        return result

class DepthMeasurement:
    def __init__(self):
        self.config = Config()
        self.pipeline = Pipeline()
        self.temporal_filter = TemporalFilter(alpha=0.5)
        self.setup_pipeline()

    def setup_pipeline(self):
        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            assert profile_list is not None
            depth_profile = profile_list.get_default_video_stream_profile()
            assert depth_profile is not None
            print("depth profile: ", depth_profile)
            self.config.enable_stream(depth_profile)
        except Exception as e:
            print(f"Setup pipeline error: {e}")

    def measure_depth(self, x1, y1, x2, y2):
        self.pipeline.start(self.config)
        try:
            frames = self.pipeline.wait_for_frames(500)
            if frames is None:
                return None

            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                return None

            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()
		
            x1 = max(0, min(x1, width - 1))
            y1 = max(0, min(y1, height - 1))
            x2 = max(0, min(x2, width))
            y2 = max(0, min(y2, height))
            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))
            
            #roi = depth_data[y1:y2, x1:x2]

            depth_data = depth_data.astype(np.float32) * scale
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
            depth_data = depth_data.astype(np.uint16)
            
            # Apply temporal filtering
            depth_data = self.temporal_filter.process(depth_data)
            depth_data = depth_data[y1:y2, x1:x2]

            return np.median(depth_data[depth_data > 0])



        finally:
            self.pipeline.stop()

    def get_depth_image(self):
        self.pipeline.start(self.config)
        try:
            frames = self.pipeline.wait_for_frames(100)
            if frames is None:
                return None

            depth_frame = frames.get_depth_frame()
            if depth_frame is None:
                return None

            width = depth_frame.get_width()
            height = depth_frame.get_height()
            scale = depth_frame.get_depth_scale()

            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_data = depth_data.reshape((height, width))

            depth_data = depth_data.astype(np.float32) * scale
            depth_data = np.where((depth_data > MIN_DEPTH) & (depth_data < MAX_DEPTH), depth_data, 0)
            depth_data = depth_data.astype(np.uint16)
            
            # Apply temporal filtering
            depth_data = self.temporal_filter.process(depth_data)

            depth_image = cv2.normalize(depth_data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_image = cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)

            return depth_image

        finally:
            self.pipeline.stop()



def post_processing_viz(result, img_path, check=False):
    '''
    视觉大模型输出结果后处理和可视化
    check：是否需要人工看屏幕确认可视化成功，按键继续或退出
    '''
    # 后处理
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # 缩放因子
    FACTOR = 999
    # 起点物体名称
    START_NAME = result['start']
    # 终点物体名称
    END_NAME = result['end']
    # 起点，左上角像素坐标
    START_X_MIN = int(result['start_xyxy'][0][0] * img_w / FACTOR)
    START_Y_MIN = int(result['start_xyxy'][0][1] * img_h / FACTOR)
    # 起点，右下角像素坐标
    START_X_MAX = int(result['start_xyxy'][1][0] * img_w / FACTOR)
    START_Y_MAX = int(result['start_xyxy'][1][1] * img_h / FACTOR)
    # 起点，中心点像素坐标
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # 终点，左上角像素坐标
    END_X_MIN = int(result['end_xyxy'][0][0] * img_w / FACTOR)
    END_Y_MIN = int(result['end_xyxy'][0][1] * img_h / FACTOR)
    # 终点，右下角像素坐标
    END_X_MAX = int(result['end_xyxy'][1][0] * img_w / FACTOR)
    END_Y_MAX = int(result['end_xyxy'][1][1] * img_h / FACTOR)
    # 终点，中心点像素坐标
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    START_X_MIN_DEPTH = int(START_X_MIN * 848 / 1280)
    START_Y_MIN_DEPTH = int(START_Y_MIN * 480 / 720)
    START_X_MAX_DEPTH = int(START_X_MAX * 848 / 1280)
    START_Y_MAX_DEPTH = int(START_Y_MAX * 480 / 720)
    END_X_MIN_DEPTH = int(END_X_MIN * 848 / 1280)
    END_Y_MIN_DEPTH = int(END_Y_MIN * 480 / 720)
    END_X_MAX_DEPTH = int(END_X_MAX * 848 / 1280)
    END_Y_MAX_DEPTH = int(END_Y_MAX * 480 / 720)

    # 初始化深度测量
    depth_measurer = DepthMeasurement()
    start_depth = depth_measurer.measure_depth(
    int(START_X_MIN_DEPTH + (START_X_MAX_DEPTH - START_X_MIN_DEPTH) * 0.25),
    int(START_Y_MIN_DEPTH + (START_Y_MAX_DEPTH - START_Y_MIN_DEPTH) * 0.25),
    int(START_X_MAX_DEPTH - (START_X_MAX_DEPTH - START_X_MIN_DEPTH) * 0.25),
    int(START_Y_MAX_DEPTH - (START_Y_MAX_DEPTH - START_Y_MIN_DEPTH) * 0.25)
)

    end_depth = depth_measurer.measure_depth(
    int(END_X_MIN_DEPTH + (END_X_MAX_DEPTH - END_X_MIN_DEPTH) * 0.25),
    int(END_Y_MIN_DEPTH + (END_Y_MAX_DEPTH - END_Y_MIN_DEPTH) * 0.25),
    int(END_X_MAX_DEPTH - (END_X_MAX_DEPTH - END_X_MIN_DEPTH) * 0.25),
    int(END_Y_MAX_DEPTH - (END_Y_MAX_DEPTH - END_Y_MIN_DEPTH) * 0.25)
)

    depth_image = depth_measurer.get_depth_image()
    cv2.rectangle(depth_image, (START_X_MIN_DEPTH, START_Y_MIN_DEPTH), 
                  (START_X_MAX_DEPTH, START_Y_MAX_DEPTH), [0, 0, 255], 2)
    cv2.rectangle(depth_image, (END_X_MIN_DEPTH, END_Y_MIN_DEPTH), 
                  (END_X_MAX_DEPTH, END_Y_MAX_DEPTH), [255, 0, 0], 2)
    if depth_image is not None:
        cv2.imshow("Depth Image", depth_image)
        cv2.moveWindow('Depth Image', 1800, 100) 
        cv2.waitKey(1)
    # 可视化
    # 画起点物体框
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # 画起点中心点
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # 画终点物体框
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # 画终点中心点
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # 写中文物体名称
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR 转 RGB
    img_pil = Image.fromarray(img_rgb) # array 转 pil
    draw = ImageDraw.Draw(img_pil)
    # 写起点物体中文名称
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # 文字坐标，中文字符串，字体，rgba颜色
    # 写终点物体中文名称
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # 文字坐标，中文字符串，字体，rgba颜色

    # 添加深度信息到图像
    if start_depth is not None:
        start_depth_text = f"Depth: {start_depth:.2f} mm"
        draw.text((START_X_MIN, START_Y_MAX+5), start_depth_text, font=font, fill=(255, 0, 0, 1))
    
    if end_depth is not None:
        end_depth_text = f"Depth: {end_depth:.2f} mm"
        draw.text((END_X_MIN, END_Y_MAX+5), end_depth_text, font=font, fill=(0, 0, 255, 1))

    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB转BGR
    # 保存可视化效果图
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)
    
    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)
    # 在屏幕上展示可视化效果图
    cv2.imshow('HUST_vlm', img_bgr) 
    cv2.moveWindow('HUST_vlm_start', 100, 100)
    print(START_X_CENTER)
    print(START_Y_CENTER)
    if check:
        print('    请确认可视化成功，按c键继续，按q键重新识别！')
        while(True):
            key = cv2.waitKey(10) & 0xFF
            if key == ord('c'): # 按c键继续
                break
            if key == ord('q'): # 按q键退出
                cv2.destroyAllWindows()   # 关闭所有opencv窗口
                return -1,-1,-1,-1
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass
    #start_depth, end_depth
    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER , start_depth , end_depth

