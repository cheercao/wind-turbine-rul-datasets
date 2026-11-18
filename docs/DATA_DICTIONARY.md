# 字段字典与特征规范 (Data Dictionary & Feature Schema)

## 1. `rul_blade_load_fatigue`（Task 1: 高频载荷序列）

| 字段标识符 | 数据类型 | 物理含义 | 量纲 / 单位 | 取值范围 |
|---|---|---|---|---|
| `turbine_id` | String | 风电机组编号 | - | WT01–WT06 |
| `timestamp` | Timestamp | 高频等间隔时间戳 | ISO 8601 (10 Hz) | 采样时间间隔 0.1 s |
| `blade_edge_1`| Float64 | 1 号叶片摆振方向实测载荷 | 弯矩/应力标定量纲 | 连续实数 |
| `blade_edge_2`| Float64 | 2 号叶片摆振方向实测载荷 | 弯矩/应力标定量纲 | 连续实数 |
| `blade_edge_3`| Float64 | 3 号叶片摆振方向实测载荷 | 弯矩/应力标定量纲 | 连续实数 |
| `generator_rpm`| Float64 | 发电机转轴转速 | rpm | 动态工况转速范围 |

---

## 2. `rul_bearing_degradation`（Task 2: 轴承健康退化序列）

| 字段标识符 | 数据类型 | 物理含义 | 量纲 / 单位 | 取值范围 |
|---|---|---|---|---|
| `turbine_id` | String | 风电机组编号 | - | WT01–WT06 |
| `date` | Date | 日级监测时间序列 | YYYY-MM-DD | 120 天连续观测周期 |
| `operating_days`| Int64 | 运行天数历时序列 | Days (天) | 0–119 |
| `bearing_temp_residual_degC` | Float64 | 测点与热平衡机理基准的温度残差 | ℃ (摄氏度) | 实数（可正可负） |
| `health_index_hi` | Float64 | 多源状态融合健康指数 (Health Index) | 无量纲标量 | 0.0 到 1.0 之间 |

---

## 3. `rul_component_failures`（Task 3: 部件服役与生存分析记录）

| 字段标识符 | 数据类型 | 物理含义 | 量纲 / 单位 | 取值范围 |
|---|---|---|---|---|
| `turbine_id` | String | 样本编号 / 机组代码 | - | 结构化样本 ID |
| `component_type`| String | 关键部件类型代码 | 分类变量 | 4 类核心部件 |
| `operating_hours`| Float64 | 累计服役工作时长 | Hours (小时) | 5,218.9 – 51,704.3 h |
| `failed_event` | Int64 | 状态指示符 (Event Indicator) | 二值分类 | 1 = 确切失效; 0 = 右删失 (Censored) |
| `avg_load_factor`| Float64 | 服役期平均负荷系数 | 无量纲 | [0.0, 1.0] |
| `avg_ambient_temp`| Float64 | 服役期环境平均气温 | ℃ (摄氏度) | 工程气温区间 |

### 核心部件统计分布规范 (Parquet 四部件版)

| 部件编码 (`component_type`) | 中文定义 | 样本量 (N) | 失效样本数 (Failed) | 删失样本数 (Censored) | 删失比例 (%) |
|---|---|---:|---:|---:|---:|
| `Main_Bearing` | 主轴承 | 30 | 11 | 19 | 63.3% |
| `Gearbox_Bearing` | 齿轮箱轴承 | 30 | 11 | 19 | 63.3% |
| `Generator_Bearing` | 发电机轴承 | 30 | 11 | 19 | 63.3% |
| `Pitch_Motor` | 变桨电机 | 30 | 11 | 19 | 63.3% |
| **合计** | - | **120** | **44** | **76** | **63.3%** |
