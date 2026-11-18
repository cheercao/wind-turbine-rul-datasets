# 风机三类寿命分析模拟数据

本仓库整理三类软件开发及演示用的**模拟数据**，不是风场实测数据、真实故障日志或已验证的寿命基准。
CSV 与 Parquet 各一份，共三个数据集、六个数据文件。文件直接复制自本地项目，未重新生成或修改数值。

| 数据文件前缀 | 行数 | 用途 | 主要字段 |
|---|---:|---|---|
| rul_blade_load_fatigue | 3600 | 6台机组的雨流疲劳分析输入 | turbine_id, timestamp, blade_edge_1/2/3, generator_rpm |
| rul_bearing_degradation | 720 | 6台机组的健康指数退化分析输入 | turbine_id, date, operating_days, bearing_temp_residual_degC, health_index_hi |
| rul_component_failures | 120 | 4类部件的生存分析输入 | turbine_id, component_type, operating_hours, failed_event, avg_load_factor, avg_ambient_temp |

## 字段及使用说明

- 疲劳：各机组600个点，采样间隔0.1秒，时间戳跨度59.9秒。叶片载荷字段不能未经标定直接当作MPa应力，S-N参数必须匹配载荷定义和单位。
- 退化：各机组120个点，operating_days为0到119，health_index_hi为健康指数。导入原软件时将timestamp映射到date。失效阈值需按应用校准；拟合无未来交点时不能凭空给出剩余天数。
- 生存：failed_event=1表示失效，0表示右删失；44条失效、76条右删失，每类部件30条。operating_hours表示失效或观察终止时的累计运行小时，不能把76条删失记录全部视为失效。
- 数据可用于输入兼容、数值方法及页面流程测试；不代表已校准的真实机组剩余寿命。模拟数据的形状不能证明预测算法准确。

## 加载

```python
import pandas as pd

fatigue = pd.read_csv("datasets/rul_blade_load_fatigue.csv", parse_dates=["timestamp"])
degradation = pd.read_csv("datasets/rul_bearing_degradation.csv", parse_dates=["date"])
survival = pd.read_csv("datasets/rul_component_failures.csv")
# 或 pd.read_parquet("datasets/rul_component_failures.parquet")
```

manifest.json提供每个文件的行数、字段、字节数及SHA-256，可核对下载后的文件。
本目录不包含软件源代码、数据库、账户信息或第三方下载的数据。
