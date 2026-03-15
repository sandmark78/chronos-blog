#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间体验操纵实验任务
基于 PsychoPy 实现
"""

from psychopy import visual, core, event, data
import random

# 实验参数
N_TRIALS = 100
DURATIONS = [1.0, 2.0, 3.0, 4.0, 5.0]  # 秒

# 创建窗口
win = visual.Window([800, 600], color='black', fullscr=False)
fixation = visual.TextStim(win, text='+', height=0.1)
stimulus = visual.TextStim(win, text='O', height=0.2)

# 指导语
instructions = visual.TextStim(
    win, 
    text='请估计圆圈呈现的时间长度\n\n按空格键开始',
    height=0.05
)

# 练习 trials
instructions.draw()
win.flip()
event.waitKeys(keypresses=['space'])

# 正式实验
for trial in range(N_TRIALS):
    duration = random.choice(DURATIONS)
    
    # 呈现刺激
    fixation.draw()
    win.flip()
    core.wait(1.0)  # 固定点 1 秒
    
    stimulus.draw()
    win.flip()
    core.wait(duration)  # 刺激呈现
    
    # 被试反应
    response = event.waitKeys(keypresses=['1', '2', '3', '4', '5'])
    
    # 记录数据
    # TODO: 保存到数据文件

win.close()
core.quit()
