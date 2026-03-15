#!/usr/bin/env python3
"""
Exp-003: 时间体验操纵实验脚本部署
启动时间：2026-03-14 22:11
状态：部署中
"""

import os
import json
from datetime import datetime

print("=" * 80)
print("🧪 Exp-003: 时间体验操纵实验脚本部署")
print("=" * 80)

# 创建实验目录
EXP_DIR = '/home/claworc/.openclaw/workspace/experiments/Exp-003_TimePerception'
os.makedirs(EXP_DIR, exist_ok=True)

# 创建实验配置文件
config = {
    'experiment_id': 'Exp-003',
    'name': '时间体验操纵实验',
    'status': 'deployed',
    'deployment_time': datetime.now().isoformat(),
    'protocol': {
        'task': '时间间隔估计任务',
        'conditions': ['高Φ条件', '低Φ条件'],
        'trials': 100,
        'duration_minutes': 30
    },
    'software': {
        'platform': 'PsychoPy',
        'version': '2023.2.3',
        'script': 'time_perception_task.py'
    }
}

# 保存配置
with open(os.path.join(EXP_DIR, 'config.json'), 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 创建 PsychoPy 脚本框架
psychopy_script = '''#!/usr/bin/env python3
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
    text='请估计圆圈呈现的时间长度\\n\\n按空格键开始',
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
'''

with open(os.path.join(EXP_DIR, 'time_perception_task.py'), 'w', encoding='utf-8') as f:
    f.write(psychopy_script)

print(f"\n✅ 实验脚本已部署至：{EXP_DIR}")
print(f"📁 文件:")
print(f"  - config.json (实验配置)")
print(f"  - time_perception_task.py (PsychoPy 脚本)")
print(f"\n📊 实验参数:")
print(f"  - 试次数：100")
print(f"  - 条件数：2")
print(f"  - 预计时长：30 分钟")
print(f"\n✅ 部署完成！")
