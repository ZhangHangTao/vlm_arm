# 机械臂+大模型+多模态=人机协作具身智能体

三套代码已经全部更新完毕
1. NVIDIA jetson Nano + 奥比中光相机 + Ur3e协作机械臂 (见UR3e + Orbbec 335L文件夹)
2. NVIDIA jetson Nano + 奥比中光相机 + 大象机械臂320 M5 (见Elephant 320M5 + Orbbec 335L文件夹)
3. 树莓派 + 摄像头法兰 + 大象机械臂280pi (见Elephant 280pi文件夹)



## 相关视频

机械臂接入GPT4o大模型，秒变多模态AI贾维斯：https://www.bilibili.com/video/BV18w4m1U7Fi

听得懂人话、看得懂图像、指哪打哪的机械臂是怎么炼成的：https://www.bilibili.com/video/BV1Cn4y1R7V2

首发实测！百度文心大模型4.0 Turbo接入机械臂智能体：https://www.bilibili.com/video/BV16M4m1m7Z1

我的抓药机械臂做了一个违背祖宗的决定：https://www.bilibili.com/video/BV1yr421K7Qs

耗时六个月，我造出了《三体》中机器人刺杀罗辑的KILLER病毒：https://www.bilibili.com/video/BV1Wm42137kR

## 原理

![原理图1-压缩](https://github.com/user-attachments/assets/82dea292-59fb-4c0d-b5df-91b346267e6c)

目标：听人话、看图像、找坐标、排动作、定格式

智能体Agent大语言模型：GPT, DeepSeek-R1,Yi-Large、Claude 3 Opus、文心大模型4.0 Turbo

多模态视觉理解大模型：GPT4v、GPT4o、Yi-Vision、Claude 3 Opus、智谱CogVLM2-Grounding、通义千问Qwen-VL-Max

## 机械臂及配件

机械臂：大象机器人Mycobot 320 M5

开发板：树莓派4B Ubuntu 20.04

配件：摄像头法兰、吸泵


## 注意事项

复现教程：https://njapov1vnz.feishu.cn/docx/Qosedmc5NoYK7IxVoMBcD47jn9b?from=from_copylink

开机教程：https://njapov1vnz.feishu.cn/docx/SJQXdIWfUo85HjxXyEBc0Wpfnqc?from=from_copylink

- 需要安装Python 3.12及所需工具包
- 需要把API_KEY.py中的KEY换成你自己的KEY
- 需要确认麦克风ID和扬声器设备
- 需要确认摄像头和语音正常
