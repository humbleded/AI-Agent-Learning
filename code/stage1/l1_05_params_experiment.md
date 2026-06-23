# L1-05 参数实验与成本意识

> 跑完 `l1_05_params_experiment.py` 后，把真实输出贴进来，并回答下面的问答。

## 实验设置

- 问题（同一个，全程固定不变）：给我的橘猫起 5 个有创意的名字，并各用一句话说明寓意。
- 模型：`deepseek-v4-pro`（非思考模式）
- 变量：`temperature = 0.0 / 1.3 / 1.5`
- 脚本：`code/stage1/l1_05_params_experiment.py`

## 三组输出对比（贴真实结果）

### temperature = 0.0

- 回答：
  ```
  （粘贴模型回答）
  ```
- token 用量：prompt = ___ ／ completion = ___ ／ total = ___

### temperature = 1.3

- 回答：
  ```
  （粘贴模型回答）
  ```
- token 用量：prompt = ___ ／ completion = ___ ／ total = ___

### temperature = 1.5

- 回答：
  ```
  （粘贴模型回答）
  ```
- token 用量：prompt = ___ ／ completion = ___ ／ total = ___

## 差异观察

- 低温 vs 高温，名字的「保守 / 发散」程度差别：
- （可选）多跑两次同一温度，看哪个温度「每次都一样 / 每次都不同」：

## 参数选择（结合本次任务）

- 给猫起名这种「创意任务」该选哪个温度？为什么？
- 如果换成「算数学题 / 写代码」，又该选哪个？为什么？

## 成本意识（L1-05 三问）

1. temperature 变高通常意味着什么？
   - 
2. 哪类任务适合低随机性？
   - 
3. token 成本由哪些部分构成？
   - 
