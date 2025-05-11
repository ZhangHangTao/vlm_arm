from pymycobot import MyCobot,utils
import time
arm=MyCobot(utils.get_port_list()[0])
for i in range(1):
    arm.set_basic_output(1,0)#打开吸泵
    time.sleep(2)
    arm.set_basic_output(1,1)#关闭吸泵
    time.sleep(2)


