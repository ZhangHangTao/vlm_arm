# utils_pump.py

import time


def pump_on(arm):
    '''
    开启吸泵
    '''
    print('    开启吸泵')
    arm.set_basic_output(1, 0)  # OUT1输出打开

def pump_off(arm):
    '''
    开启吸泵
    '''
    print('    关闭吸泵')
    arm.set_basic_output(1,1)