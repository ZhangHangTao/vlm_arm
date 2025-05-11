# agent_go.py

print('华中科大网安学院TAI团队 2024-08-24')

from utils_asr import *             # 录音+语音识别
from utils_robot import *           # 连接机械臂
from utils_llm import *             # 大语言模型API
from utils_camera import *          # 摄像头
from utils_robot import *           # 机械臂运动
from utils_pump import *            # GPIO、吸泵
from utils_vlm_move import *        # 多模态大模型识别图像，吸泵吸取并移动物体
from utils_agent import *           # 智能体Agent编排
from utils_tts import *             # 语音合成模块
from utils_vlm_vqa import *
import threading
# print('播放欢迎词')
pump_off()
# back_zero()
#play_wav('asset/welcome.wav')
working_mode = False
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
    return "小优" in text or "小幽" in text or "同学" in text 
    
def process_command(order):
    message.append({"role":"user","content":order})
    # 智能体Agent编排动作
    #output=eval(agent_plan(message))
    output = eval(agent_plan(message).strip('```')) if agent_plan(message).startswith('```') else eval(agent_plan(message))
    print(output)
    response = output['response'] # 获取机器人想对我说的话
    tts(response)                     # 语音合成，导出wav音频文件
    play_wav('temp/tts.wav')          # 播放语音合成音频文件
    output_other=''
    for each in output['function']: # 运行智能体规划编排的每个函数
        print('开始执行动作', each)
        ret = eval(each)
        if ret != None:
            output_other = ret

    output['response']+='.'+ output_other
    message.append({"role":"assistant","content":str(output)})
    back_zero()
    
    #time.sleep(3)
    
def agent_play():
    '''
    主函数，语音控制机械臂智能体编排动作
    '''
    # 归零
    catch('吸泵', 0)
    back_zero()
    #global working_mode
    #background_thread=threading.Thread(target=background_task)
    #background_thread.start()
    # print('测试摄像头')
    #check_camera()
    
    # 输入指令
    print('请根据场馆噪声，设置声音接受阈值，数值越高，排除噪声越多（5000～15000），键入回车使用默认值')
    #QUITE_DB=input('')
    QUITE_DB=20000
    #if str.isnumeric(QUITE_DB)==False:
    	#QUITE_DB=8000
    #start_record_ok = input('输入数字录音指定时长，按k打字输入，按c输入默认指令\n')
    print("机械臂已启动，正在等待唤醒词'小优同学'...")
    
    start_record_ok = "1" # Option 1      
         
    # Option 2          
    process_command('将药放到碗里') # Option 2 
   
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
            #time.sleep(0.011)
            
            
            
    	elif start_record_ok == 'k':
            order = input('请输入指令')
            process_command(order)
        #elif start_record_ok == 'c':
            #order = '先归零，再摇头，然后把绿色方块放在篮球上'
        #else:
            #print('无指令，退出')
            #raise NameError('无指令，退出')
        
    

if __name__ == '__main__':

    while True:
        agent_play()

