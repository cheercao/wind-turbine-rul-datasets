# 字段字典

## 1. rul_blade_load_fatigue

| 字段 | 类型 | 含义 / 单位 |
|---|---|---|
| turbine_id | 字符串 | 模拟机组ID，WT01–WT06 |
| timestamp | 时间 | 模拟采样时刻，间隔0.1秒；原文件无时区 |
| blade_edge_1 | 数值 | 叶片1摆振方向模拟载荷；原文件未附可核实的物理单位元数据 |
| blade_edge_2 | 数值 | 叶片2同类模拟载荷 |
| blade_edge_3 | 数值 | 叶片3同类模拟载荷 |
| generator_rpm | 数值 | 原样例转速字段，名称标记rpm；未提供真实设备标定 |

不要把载荷直接重命名为stress_mpa并当作MPa。S-N参数和载荷定义、幅值/范围约定必须一致。
每机组600行，首末时间戳跨度59.9秒；采样点数×间隔为60秒，两种计时口径应区别。

## 2. rul_bearing_degradation

| 字段 | 类型 | 含义 / 单位 |
|---|---|---|
| turbine_id | 字符串 | 模拟机组ID，WT01–WT06 |
| date | 日期 | 模拟观测日期，无时区 |
| operating_days | 整数 | 运行时间轴，天，0–119 |
| bearing_temp_residual_degC | 数值 | 模拟轴承温度残差，摄氏度；残差可为负 |
| health_index_hi | 数值 | 无量纲健康指数，文件中0<HI≤1 |

每机组120行。HI阈值不是原始数据中已确认的真实故障标签。

## 3. rul_component_failures

| 字段 | 类型 | 含义 / 单位 |
|---|---|---|
| turbine_id | 字符串 | 样例记录ID，不等同于已确认的现场风机数量 |
| component_type | 字符串 | 部件类型，见下表 |
| operating_hours | 数值 | 失效或观察终止时累计运行小时，正值 |
| failed_event | 整数 | 1=发生失效；0=观察结束仍未失效（右删失） |
| avg_load_factor | 数值 | 模拟平均负载系数，无量纲 |
| avg_ambient_temp | 数值 | 模拟平均环境温度；字段未附独立单位元数据 |

| 编码 | 中文含义 | 行数 |
|---|---|---:|
| Main_Bearing | 主轴承 | 30 |
| Gearbox_Bearing | 齿轮箱轴承 | 30 |
| Generator_Bearing | 发电机轴承 | 30 |
| Pitch_Motor | 变桨电机 | 30 |

上表部件计数适用于Parquet版。CSV版120条全部为Gearbox_Bearing，运行小时范围5218.9–35000；Parquet版范围5826.1–51704.3。两版均44条失效、76条右删失，记录数相同但数据不同，不能按ID关联。

为存活样本记录的operating_hours表示至少已存活这么久，不能当作精确失效时间。
