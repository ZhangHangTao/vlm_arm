from pymycobot.mycobot320 import MyCobot320
import time
mc = MyCobot320("COM5", 115200)

start = time.time()
# 让机械臂到达指定位置
mc.send_angles([-1.49, 115, -145, 30, -33.42, 137.9], 80)
# 判断其是否到达指定位置
while not mc.is_in_position([-1.49, 115, -145, 30, -33.42, 137.9], 0):
    # 让机械臂恢复运动
    mc.resume()
    # 让机械臂移动0.5s
    time.sleep(0.5)
    # 暂停机械臂移动
    mc.pause()
    # 判断移动是否超时
    if time.time() - start > 3:
        break
# 设置开始时间
start = time.time()
# 让运动持续30秒
while time.time() - start < 30:
    # 让机械臂快速到达该位置
    mc.send_angles([-1.49, 115, -145, 30, -33.42, 137.9], 80)
    # 将灯的颜色为[0,0,50]
    mc.set_color(0, 0, 50)
    time.sleep(0.7)
    # 让机械臂快速到达该位置
    mc.send_angles([-1.49, 55, -145, 80, 33.42, 137.9], 80)
    # 将灯的颜色为[0,50,0]
    mc.set_color(0, 50, 0)
    time.sleep(0.7)