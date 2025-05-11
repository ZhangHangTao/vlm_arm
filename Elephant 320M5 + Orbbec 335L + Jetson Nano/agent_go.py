# agent_go.py

# 导入常用函数
from utils_asr import *             # 录音+语音识别
from utils_robot import *           # 连接机械臂
from utils_llm import *             # 大语言模型API
from utils_led import *             # 控制LED灯颜色
from utils_camera import *          # 摄像头
from utils_robot import *           # 机械臂运动
from utils_pump import *            # GPIO、吸泵
from utils_vlm_move import *        # 多模态大模型识别图像，吸泵吸取并移动物体
from utils_vlm_vqa import *
from utils_agent import *           # 智能体Agent编排
from utils_tts import *             # 语音合成模块
working_mode = False
pump_off(mc)
message=[]
message.append({"role":"system","content":AGENT_SYS_PROMPT})

def background_task():
    while 1:
        while not working_mode:
        #tts('我是大语言模型赋能的小优同学，我什么都知道哦! 还能抓取任意东西，快来和我聊天吧！')                     # 语音合成，导出wav音频文件
            #play_wav('temp/welcome.wav')
            #welcome()
            time.sleep(1)
def detect_wake_word(text):
    return "大象" in text
def process_command(order):
    message.append({"role": "user", "content": order})
    # 智能体Agent编排动作
    # output=eval(agent_plan(message))
    output = eval(agent_plan(message).strip('```')) if agent_plan(message).startswith('```') else eval(
        agent_plan(message))
    print(output)
    response = output['response']  # 获取机器人想对我说的话
    tts(response)  # 语音合成，导出generwav音频文件
    play_wav('temp/tts.wav')  # 播放语音合成音频文件
    output_other = ''
    for each in output['function']:  # 运行智能体规划编排的每个函数
        print('开始执行动作', each)
        ret = eval(each)
        if ret != None:
            output_other = ret

    output['response'] += '.' + output_other
    message.append({"role": "assistant", "content": str(output)})
    back_zero()

    # time.sleep(3)


def agent_play():
    '''
    主函数，语音控制机械臂智能体编排动作
    '''
    back_zero()
    global working_mode

    QUITE_DB = 20000
    print("机械臂已启动，正在等待唤醒词'大象同学'...")

    start_record_ok = "1"  # Option 1

    # Option 2
    process_command('将积木移动到碗里')  # Option 2

    while True:
        if str.isnumeric(start_record_ok):
            working_mode = record_auto(working_mode, int(QUITE_DB))
            text = speech_recognition()

            if working_mode:
                if text.strip():  # 如果识别到非空文本
                    process_command(text)
            else:
                if detect_wake_word(text):
                    back_zero()
                    play_wav('temp/tts_welcome.wav')  # 播放语音合成音频文件
                    working_mode = True
            time.sleep(0.011)



        elif start_record_ok == 'k':
            order = input('请输入指令')
            process_command(order)



if __name__ == '__main__':

    while True:
        agent_play()


