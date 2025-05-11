# utils_robot.py
# 启动并连接机械臂，导入各种工具包

print('导入机械臂连接模块')
import socket
import cv2
import numpy as np
import time
from utils_pump import *
import os
from pyorbbecsdk import *
from utils import frame_to_bgr_image
p = 3.1415926535


class UR:
    def __init__(self, host, port=30003):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((self.host, self.port))
        print("Connected to robot")

    def disconnect(self):
        if self.socket:
            self.socket.close()
            print("Disconnected from robot")

    def send_command(self, command):
        if self.socket:
            self.socket.send((command + "\n").encode())
            print(f"Sent command: {command}")

    def catch_on(self):
        command = f"set_tool_digital_out(0,True)"
        self.send_command(command)
        
    def catch_off(self):
        command = f"set_tool_digital_out(0,False)"
        self.send_command(command)
        
    def pump_on(self):
        command = f"set_standard_digital_out(5,True)"
        self.send_command(command)
        
    def pump_off(self):
        command = f"set_standard_digital_out(5,False)"
        self.send_command(command)
        time.sleep(0.2)
        
        command = f"set_standard_digital_out(5,True)"
        self.send_command(command)
        time.sleep(0.01)
        
        command = f"set_standard_digital_out(5,False)"
        self.send_command(command)
        time.sleep(0.2)
        

        
    def movej(self, q, a=0.3, v=0.3, t=0, r=0):
        command = f"movej({q}, a={a}, v={v}, t={t}, r={r})"
        self.send_command(command)

    def movel(self, pose, a=0.05, v=0.05):
        command = f"movel([{pose[0]},{pose[1]},{pose[2]},{pose[3]},{pose[4]},{pose[5]}], a={a}, v={v})"
        self.send_command(command)

    def move_to_z(self, new_z):
        """只改变z轴坐标，保持x, y, rx, ry, rz不变"""
        command = (
            "def move_to_z():\n"
            "  pose = get_actual_tcp_pose()\n"
            f"  pose[2] = {new_z}\n"
            "  movel(pose, a=0.05, v=0.05)\n"
            "end\n"
        )
        self.send_command(command)

    def move_to_xyz(self, new_x, new_y, new_z):
        """只改变x和y轴坐标，保持z, rx, ry, rz不变"""
        command = (
            "def move_to_xyz():\n"
            "  pose = get_actual_tcp_pose()\n"
            f"  pose[0] = {new_x}\n"
            f"  pose[1] = {new_y}\n"
            f"  pose[2] = {new_z}\n"
            "  movel(pose, a=0.1, v=0.1)\n"
            "end\n"
        )
        self.send_command(command)

    def stop(self):
        command = "stopj(2)"
        self.send_command(command)


robot = UR("192.168.1.112")
robot.connect()

#import RPi.GPIO as GPIO
# 初始化GPIO
#GPIO.setwarnings(False)   # 不打印 warning 信息
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(20, GPIO.OUT)
#GPIO.setup(21, GPIO.OUT)
#GPIO.output(20, 1)        # 关闭吸泵电磁阀

def back_zero():
    '''
    机械臂归零
    '''
    print('机械臂归零')
    robot.movej([-135/180*p, -90/180*p, 60/180*p, -150/180*p, 90/180*p, 0], a=1, v=2)
    time.sleep(0.3)

def relax_arms():
    print('放松机械臂关节')
    #mc.release_all_servos()

def head_shake():
    print('shake')
    # 左右摆头
    #mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    #robot.movej([-135/180*p, -90/180*p, 60/180*p, -160/180*p, 90/180*p, 0], a=1.5, v=1.5)
    robot.movej([90/180*p, -88.53/180*p, -54.14/180*p, -90/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(6)    
    for count in range(1):
    	robot.movej([60/180*p, -88.53/180*p, -30/180*p, -90/180*p, 90/180*p, 0/180*p], a=1.5, v=1)
    	time.sleep(2)
    	robot.movej([120/180*p, -88.53/180*p, -30/180*p, -90/180*p, 90/180*p, 0/180*p], a=1.5, v=1)
    	time.sleep(2)
    	robot.movej([60/180*p, -88.53/180*p, -30/180*p, -90/180*p, 90/180*p, 0/180*p], a=1.5, v=1)
    	time.sleep(2)
    	robot.movej([120/180*p, -88.53/180*p, -30/180*p, -90/180*p, 90/180*p, 0/180*p], a=1.5, v=1)
    	time.sleep(2) 
    # mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
  
    #mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    robot.movej([86.59/180*p, -122.63/180*p, 69.27/180*p, -159.78/180*p, 90/180*p, 0], a=1.5, v=1.5)
    #time.sleep(2)

def head_dance():
    #print('dance')
    # 跳舞
    #mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    robot.movej([90/180*p, -110/180*p, -30/180*p, -80/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(6)
            
    for count in range(2):
    	robot.movej([60/180*p, -110/180*p, -60/180*p, -100/180*p, 120/180*p, 30/180*p], a=1.5, v=1)
    	time.sleep(1.8)    
    	robot.movej([120/180*p, -88.53/180*p, -30/180*p, -80/180*p, 90/180*p, -30/180*p], a=1.5, v=1)
    	time.sleep(1.8)    
    	robot.movej([60/180*p, -110/180*p, -0/180*p, -60/180*p, 60/180*p, 30/180*p], a=1.5, v=1)
    	time.sleep(1.8)
    	robot.movej([110/180*p, -90/180*p, -30/180*p, -90/180*p, 100/180*p, -30/180*p], a=1.5, v=1)
    	time.sleep(1.8)    
    	
        
        
def welcome():
    #print('dance')
    # 跳舞

    robot.movej([60/180*p, -110/180*p, -60/180*p, -100/180*p, 120/180*p, 30/180*p], a=1.5, v=1)
    time.sleep(3)    
    robot.movej([120/180*p, -88.53/180*p, -30/180*p, -80/180*p, 90/180*p, -30/180*p], a=1.5, v=1)
    time.sleep(3)    
    robot.movej([60/180*p, -110/180*p, -0/180*p, -60/180*p, 60/180*p, 30/180*p], a=1.5, v=1)
    time.sleep(3)
    robot.movej([110/180*p, -90/180*p, -30/180*p, -90/180*p, 100/180*p, -30/180*p], a=1.5, v=1)
    time.sleep(3) 
    	        
        #mc.send_angles([(-0.17),(-94.3),118.91,(-39.9),59.32,(-0.52)],80)        
        #time.sleep(1.2)
        #mc.send_angles([67.85,(-3.42),(-116.98),106.52,23.11,(-0.52)],80)
        #time.sleep(1.7)              


def head_nod():
    print('nod')
    # 点头
    #mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)
    robot.movej([90/180*p, -110/180*p, -30/180*p, -80/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(6)    
    robot.movej([90/180*p, -110/180*p, -30/180*p, -110/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(1.5)    
    robot.movej([90/180*p, -110/180*p, -30/180*p, -80/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(1.5)    
    robot.movej([90/180*p, -110/180*p, -30/180*p, -110/180*p, 90/180*p, 0/180*p], a=1.5, v=1.5)
    time.sleep(1.5)    
    robot.movej([-135/180*p, -90/180*p, 60/180*p, -150/180*p, 90/180*p, 0], a=1.5, v=1.5)
     
    #for count in range(2):
        #mc.send_angle(4, 13, 70)
        #time.sleep(0.5)
        #mc.send_angle(4, -20, 70)
        #time.sleep(1)
        #mc.send_angle(4,13,70)
        #time.sleep(0.5)
    #mc.send_angles([0.87,(-50.44),47.28,0.35,(-0.43),(-0.26)],70)

def move_to_coords(X=150, Y=-130, HEIGHT=200):
    print('移动至指定坐标：X {} Y {}'.format(X, Y))
    robot.move_to_xyz(X/1000, Y/1000, HEIGHT/1000)


def move_z(Z=150):
    print('移动至指定坐标：Z {}'.format(Z))
    robot.move_to_z(Z/1000)

def catch(t='吸泵',z=1):
    if t=='吸泵':
        if z==0:
            robot.pump_off()
        elif z==1:
            robot.pump_on()
    elif t=='抓夹':
        if z==0:
            robot.catch_off()
        elif z==1:
            robot.catch_on()

    else:
        print('请检查抓架命令')
 
    
def single_joint_move(joint_index, angle):
    print('关节 {} 旋转至 {} 度'.format(joint_index, angle))
    #mc.send_angle(joint_index, angle, 40)
    #time.sleep(2)

def move_to_top_view():
    #robot.movej([-258.82/180*p, -75.32/180*p, -57.42/180*p, -134.59/180*p, 90/180*p, 56.5/180*p], a=2, v=3)
    robot.movej([90/180*p, -88.53/180*p, -54.14/180*p, -127.2/180*p, 90/180*p, 0/180*p], a=2, v=3)
    time.sleep(4)




def save_one_color_frame(frame: ColorFrame, filename="temp/vl_now.jpg"):
    if frame is None:
        print("No frame to save.")
        return
    image = frame_to_bgr_image(frame)
    if image is None:
        print("Failed to convert frame to image.")
        return
    cv2.imwrite(filename, image)
    print(f"Image saved as {filename}")

def capture_and_save_image(filename="temp/vl_now.jpg", timeout=800):
    pipeline = Pipeline()
    config = Config()

    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
        if profile_list is not None:
            color_profile: VideoStreamProfile = profile_list.get_default_video_stream_profile()
            config.enable_stream(color_profile)
    except OBError as e:
        print(f"Error getting stream profile list: {e}")
        return None

    pipeline.start(config)
    
    try:
        frames = pipeline.wait_for_frames(timeout)
        if frames is not None:
            color_frame = frames.get_color_frame()
            if color_frame is not None:
                save_one_color_frame(color_frame, filename)
                return frame_to_bgr_image(color_frame)
        else:
            print("No frames received.")
            return None
    except Exception as e:
        print(f"An error occurred while capturing the frame: {e}")
        return None
    finally:
        pipeline.stop()

def top_view_shot(check=False):
    '''
    拍摄一张图片并保存
    check：是否需要人工看屏幕确认拍照成功，再在键盘上按q键确认继续
    '''
    print('    移动至俯视姿态')
    move_to_top_view()

    # 使用Orbbec SDK替代OpenCV的摄像头捕获
    #time.sleep(0.3)  # 等待摄像头稳定
    img_bgr = capture_and_save_image()
    if img_bgr is not None:
        # 屏幕上展示图像
        cv2.destroyAllWindows()  # 关
        cv2.imshow('HUST_vlm', img_bgr)
        
        if check:
            print('请确认拍照成功，按c键继续，按q键退出')
            while(True):
                key = cv2.waitKey(10) & 0xFF
                if key == ord('c'):  # 按c键继catch('吸泵', 0)续
                    break
                if key == ord('q'):  # 按q键退出
                    cv2.destroyAllWindows()   # 关闭所有opencv窗口
                    raise NameError('按q退出')
        else:
            if cv2.waitKey(10) & 0xFF == None:
                pass
    else:
        print("Failed to capture image.")

    # 关闭所有OpenCV

    cv2.destroyAllWindows()




def linear_interpolate(x, x_points, y_points):
    '''
    手动实现线性插值和外推
    x: 输入值（可能超出范围）
    x_points: 自变量已知点的列表（两个点）
    y_points: 因变量已知点的列表（两个点）
    '''
    x0, x1 = x_points
    y0, y1 = y_points

    # 计算斜率
    slope = (y1 - y0) / (x1 - x0)
    
    # 线性插值或外推
    return y0 + slope * (x - x0)


def eye2hand(X_im=160, Y_im=120):
    '''
    输入目标点在图像中的像素坐标，转换为机械臂坐标，支持插值和外推
    '''
    # 整理两个标定点的坐标
    cali_1_im = [502, 312]                      # 左下角，第一个标定点的像素坐标，要手动填！
    cali_1_mc = [19.38, 416.17]                 # 左下角，第一个标定点的机械臂坐标，要手动填！
    cali_2_im = [858, 121]                      # 右上角，第二个标定点的像素坐标
    cali_2_mc = [260.4, 529.78]                 # 右上角，第二个标定点的机械臂坐标，要手动填！
    
    X_cali_im = [cali_1_im[0], cali_2_im[0]]    # 像素坐标
    X_cali_mc = [cali_1_mc[0], cali_2_mc[0]]    # 机械臂坐标
    Y_cali_im = [cali_2_im[1], cali_1_im[1]]    # 像素坐标，先小后大
    Y_cali_mc = [cali_2_mc[1], cali_1_mc[1]]    # 机械臂坐标，先大后小

    # 使用线性插值函数进行X和Y的插值或外推
    X_mc = linear_interpolate(X_im, X_cali_im, X_cali_mc)
    Y_mc = linear_interpolate(Y_im, Y_cali_im, Y_cali_mc)

    return X_mc, Y_mc





#用抓夹抓
def pump_move(XY_START=[230,-50], HEIGHT_START=65, XY_END=[100,220], HEIGHT_END=100, HEIGHT_SAFE=120):
    catch('吸泵',0)



    move_to_coords(XY_START[0],XY_START[1],HEIGHT_SAFE)
    time.sleep(6)

    
    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    print(HEIGHT_START)
    #mc.send_coords([XY_START[0], XY_START[1], HEIGHT_START, 0, 180, 90], 15, 0)
    move_z(HEIGHT_START+3)
    time.sleep(4)
    catch('吸泵',1)
    time.sleep(1)
    # 升起物体
    #print('    升起物体')
    move_z(HEIGHT_SAFE-150)
    #mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(5)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    #print(XY_END[0])
    #print(XY_END[1])
    move_to_coords(XY_END[0],XY_END[1],HEIGHT_SAFE)
    #mc.send_coords([XY_END[0], XY_END[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(5)

    # 向下放下物体
    print('    向下放下物体')
    #mc.send_coords([XY_END[0], XY_END[1], HEIGHT_END, 0, 180, 90], 20, 0)
    #move_z(HEIGHT_END)
    time.sleep(4)
    catch('吸泵',0)
    time.sleep(1)
    
    

    

# 吸泵吸取并移动物体
def pump_move_ZJ(XY_START=[230,-50], HEIGHT_START=65, XY_END=[100,220], HEIGHT_END=100, HEIGHT_SAFE=120):
    catch('抓夹',1)
    #catch('吸泵', 0)
    '''
    用吸泵，将物体从起点吸取移动至终点

    mc：机械臂实例
    XY_START：起点机械臂坐标
    HEIGHT_START：起点高度 90
    XY_END：终点机械臂坐标
    HEIGHT_END：终点高度
    HEIGHT_SAFE：搬运途中安全高度
    '''

    # 初始化GPIO
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(20, GPIO.OUT)
    #GPIO.setup(21, GPIO.OUT)

    # 设置运动模式为插补
    #mc.set_fresh_mode(0)
    
    # # 机械臂归零
    # print('    机械臂归零')
    # mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    # time.sleep(4)
    
    # 吸泵移动至物体上方
    print('    吸泵移动至物体上方')

    #time.sleep(3)
    #print(XY_START[0])
    #print(XY_START[1])
    move_to_coords(XY_START[0],XY_START[1],HEIGHT_SAFE)
    time.sleep(6)
    #mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 20, 0)
    #time.sleep(3)

    
    # 吸泵向下吸取物体
    print('    吸泵向下吸取物体')
    print(HEIGHT_START)
    #mc.send_coords([XY_START[0], XY_START[1], HEIGHT_START, 0, 180, 90], 15, 0)
    move_z(HEIGHT_START-76)
    #move_z(HEIGHT_START)
    time.sleep(7)
    catch('抓夹', 0)
    time.sleep(1)
    # 升起物体
    #print('    升起物体')
    move_z(HEIGHT_SAFE)
    #mc.send_coords([XY_START[0], XY_START[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(5)

    # 搬运物体至目标上方
    print('    搬运物体至目标上方')
    #print(XY_END[0])
    #print(XY_END[1])
    move_to_coords(XY_END[0],XY_END[1],HEIGHT_SAFE)
    #mc.send_coords([XY_END[0], XY_END[1], HEIGHT_SAFE, 0, 180, 90], 15, 0)
    time.sleep(5)

    # 向下放下物体
    print('    向下放下物体')
    #mc.send_coords([XY_END[0], XY_END[1], HEIGHT_END, 0, 180, 90], 20, 0)
    move_z(HEIGHT_END+50)
    time.sleep(4)
    catch('抓夹', 1)
    time.sleep(1)
    # 关闭吸泵
    #pump_off()

    # 机械臂归零
    #back_zero()


