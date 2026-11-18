<div align="center">

# WindTurbine-RUL: A Multitask Benchmark Dataset for Prognostics and Health Management in Wind Turbines
### 面向风电机组健康预测与寿命管理的基准数据集 (WindTurbine-RUL Benchmark)

**Rainflow Fatigue Quantification · Health Indicator Degradation Modeling · Right-Censored Survival Analysis**

[![Benchmark](https://img.shields.io/badge/Benchmark-PHM%20%26%20RUL-2563eb?style=flat-square)](datasets/)
[![Tasks](https://img.shields.io/badge/Tasks-Fatigue%20%7C%20Degradation%20%7C%20Survival-0f766e?style=flat-square)](docs/DATA_CARD.md)
[![Formats](https://img.shields.io/badge/Formats-CSV%20%7C%20Parquet-7c3aed?style=flat-square)](manifest.json)
[![Turbines](https://img.shields.io/badge/Turbines-6%20Units%20(WT01--WT06)-amber?style=flat-square)](docs/DATA_DICTIONARY.md)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-slate?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Release-v1.1.0-334155?style=flat-square)](CHANGELOG.md)

[Dataset Files](datasets/) • [Task Formulations](#基准任务与数学表征-benchmark-tasks--mathematical-formulations) • [Data Dictionary](docs/DATA_DICTIONARY.md) • [Data Card](docs/DATA_CARD.md) • [Validation](docs/QUALITY_REPORT.md) • [Citation](#引用-citation)

</div>

---

## 摘要 (Abstract)

大型风电机组（Wind Turbine Generators, WTGs）长期服役于非平稳湍流风况与交变载荷环境下，关键结构件与机电传动链退化机理复杂，剩余使用寿命（Remaining Useful Life, RUL）的高精度预测与可靠性评估是风电装备预测与健康管理（Prognostics and Health Management, PHM）领域的核心挑战。现有公开基准多局限于实验室稳态加速退化试验，难以兼顾空气动力-结构高频受载、长周期热力学退化以及多部件伴随高比例截尾（Right Censoring）的多时间尺度物理特性。

**WindTurbine-RUL** 构建了面向风电机组 PHM 与可靠性分析的多任务公开基准数据集，系统覆盖三类核心分析范式：
1. **Task 1: 高频气动-结构载荷雨流疲劳损伤累积 (High-Frequency Aerodynamic-Structural Load Fatigue Damage)**；
2. **Task 2: 长程轴承温度残差与健康指数退化轨迹建模 (Multivariate Bearing HI Degradation Modeling)**；
3. **Task 3: 考虑右删失的多部件时变可靠度与生存分析 (Right-Censored Component Survival & Reliability Analysis)**。

所有子集均提供高效列式存储的 **Parquet** 格式与通用 **CSV** 格式，并配备形式化数学建模、标准评测协议及自动化校验套件，旨在为风电智能运维、时间序列建模与可靠性工程研究提供高保真的开放评测基准。

---

![WindTurbine-RUL 基准概览](assets/dataset-overview.png)
<p align="center"><em>Figure 1. 数据集概览：(a) 叶片摆振受载时序 (10 Hz)；(b) 轴承长周期健康指数退化曲线；(c) 4 类关键部件服役寿命与故障/删失分布。</em></p>

---

## 基准任务与数学表征 (Benchmark Tasks & Mathematical Formulations)

### Task 1: 载荷循环提取与累积疲劳损伤量化 (Rainflow Fatigue Analysis)

- **物理背景**：风电机组叶片在旋转过程中承受显著的周期性气动载荷与随机湍流扰动，产生微观塑性变形与疲劳裂纹累积。
- **输入时序规格**：多通道连续时序张量定义为 $\mathbf{X} \in \mathbb{R}^{T \times C}$，采样频率 10 Hz，时序长度 $T = 600$（单次连续观测时长 60 s），涵盖 6 台机组（WT01–WT06）。测点包含三通道叶片摆振实测载荷（`blade_edge_1/2/3`）与发电机转速（`generator_rpm`）。

#### 数学建模与计算流程

**1. 载荷循环提取与雨流离散化**

依据 ASTM E1049-85 标准雨流计数算法（Rainflow Counting Algorithm），将连续随机载荷历程离散化为载荷谱集合：

$$
\mathcal{C} = \{ (S_{a,i}, S_{m,i}, n_i) \}_{i=1}^M
$$

| 参数符号 | 物理含义 | 说明 |
|---|---|---|
| $S_{a,i}$ | 循环应力幅值 | 雨流计数提取的各级交变载荷幅值 |
| $S_{m,i}$ | 平均应力 | 各级循环均值（用于平均应力修正） |
| $n_i$ | 循环频次 | 当前时序历程中统计的载荷周次 |

**2. Palmgren-Miner 线性累积疲劳损伤**

结合材料 S-N 双对数幂律本构方程：

$$
N_i \cdot S_{a,i}^m = C
$$

依 Palmgren-Miner 准则计算无量纲累积疲劳损伤度 $D$：

$$
D = \sum_{i=1}^M \frac{n_i}{N_i}
$$

基于实测时序的损伤累积率，进一步评估部件在特征工况下的疲劳耗损速率与折合服役年限。

---

### Task 2: 长程健康指数退化轨迹建模与阈值外推 (HI Degradation & First Hitting Time)

- **物理背景**：主轴承与齿轮箱高速轴承在持续交变摩擦与温升冲击下发生微磨损、剥落或点蚀，状态监测表现为热平衡温度残差偏移与融合健康指数衰退。
- **输入序列定义**：长历时多变量离散观测时序集合定义为：

$$
\mathcal{D}_k = \{ (t_\tau, y_\tau, \mathbf{z}_\tau) \}_{\tau=0}^k
$$

包含 6 台机组（WT01–WT06）连续 120 天跟踪监测（运行天数 $t \in [0, 119]$）：
- `bearing_temp_residual_degC`：测点温度与热平衡基准的残差标量 $\mathbf{z}$；
- `health_index_hi`：多维融合健康状态指数 $y \in (0, 1.0]$。

#### 数学建模与计算流程

**1. 非线性状态退化动力学建模**

建立非线性状态退化回归方程：

$$
y(t) = g(t; \boldsymbol{\theta}) + \epsilon(t), \quad \epsilon(t) \sim \mathcal{N}(0, \sigma^2)
$$

典型模型包括指数衰减模型 $g(t) = a \cdot \exp(b \cdot t)$、多项式轨迹或高斯过程回归（Gaussian Process Regression, GPR）。

**2. 首达阈值时间（First Hitting Time, FHT）预测**

设失效预警阈值为 $HI_{\text{th}}$，剩余寿命预测形式化为首达阈值时间求解：

$$
T_{\text{fail}} = \inf \left[ t > t_k \mid g(t; \boldsymbol{\theta}) \le HI_{\text{th}} \right]
$$

$$
\text{RUL}(t_k) = T_{\text{fail}} - t_k
$$

---

### Task 3: 考虑右删失的多部件时变可靠度与生存分析 (Right-Censored Survival Analysis)

- **物理背景**：在风电场实际工程统计中，绝大多数在役部件至统计截止时仍处于健康服役状态，直接丢弃未失效样本或将其强行视作故障将导致极大的生存概率高估或寿命低估偏差。
- **输入样本集定义**：共计 120 个关键部件服役观测样本，数学表征定义为：

$$
\mathcal{S} = \{ (t_j, \delta_j, \mathbf{x}_j) \}_{j=1}^N \quad (N = 120)
$$

涵盖 4 类核心部件（`Main_Bearing`、`Gearbox_Bearing`、`Generator_Bearing`、`Pitch_Motor`）。各分量定义如下：

| 变量符号 | 对应数据字段 | 物理含义与取值范围 |
|---|---|---|
| $t_j$ | `operating_hours` | 观测服役时长（累计运行小时数，$t_j > 0$） |
| $\delta_j$ | `failed_event` | 事件状态指示符：$\delta = 1$ 为确切故障停机，$\delta = 0$ 为右删失截尾 |
| $\mathbf{x}_j$ | `avg_load_factor`, `avg_ambient_temp` | 工况协变量向量（包含平均负载系数与平均环境温度） |

#### 数学建模与计算流程

**1. 参数化 Weibull 似然估计（处理右删失数据）**

两参数 Weibull 分布可靠度函数 $R(t)$ 与概率密度函数 $f(t)$ 分别为：

$$
R(t; \beta, \eta) = \exp\left( -\left(\frac{t}{\eta}\right)^\beta \right)
$$

$$
f(t; \beta, \eta) = \frac{\beta}{\eta}\left(\frac{t}{\eta}\right)^{\beta - 1}\exp\left( -\left(\frac{t}{\eta}\right)^\beta \right)
$$

构建包含右删失项的对数似然函数并求解极大似然估计（MLE）：

$$
\ln \mathcal{L}(\beta, \eta) = \sum_{j=1}^N \left[ \delta_j \ln f(t_j; \beta, \eta) + (1 - \delta_j) \ln R(t_j; \beta, \eta) \right]
$$

**2. 非参数 Kaplan-Meier 经验基准**

按失效发生时刻升序重排，计算乘积限生存估计量：

$$
\hat{S}(t) = \prod_{t_j \le t} \left( 1 - \frac{d_j}{n_j} \right)
$$

| 统计分量 | 物理含义说明 |
|---|---|
| $d_j$ | 在时刻 $t_j$ 发生的确切故障失效事件数 |
| $n_j$ | 在时刻 $t_j$ 处仍处于风险暴露（At-Risk）的有效在役样本总数 |

---

## 基准数据集架构 (Benchmark Architecture)

| 子数据集 (Subset) | 任务定位 (Task) | 机组 / 样本规模 | 时间尺度与采样率 | 特征维度 | 格式与下载 |
|---|---|---|---|---|---|
| **`rul_blade_load_fatigue`** | Task 1: 雨流疲劳分析 | 6 台机组 (WT01–WT06)；共 3,600 观测点 | 10 Hz 高频连续采样；各机组 600 点 (60 s) | 6 维 (`turbine_id`, `timestamp`, `blade_edge_1/2/3`, `generator_rpm`) | [Parquet](datasets/rul_blade_load_fatigue.parquet) · [CSV](datasets/rul_blade_load_fatigue.csv) |
| **`rul_bearing_degradation`**| Task 2: 健康退化建模 | 6 台机组 (WT01–WT06)；共 720 观测点 | 日级追踪历时；各机组 120 天时序 | 5 维 (`turbine_id`, `date`, `operating_days`, `bearing_temp_residual_degC`, `health_index_hi`) | [Parquet](datasets/rul_bearing_degradation.parquet) · [CSV](datasets/rul_bearing_degradation.csv) |
| **`rul_component_failures`** | Task 3: 删失生存分析 | 4 类关键部件；共 120 条服役记录 | 累计服役小时 (5,218–51,704 h)；含 63.3% 删失率 | 6 维 (`turbine_id`, `component_type`, `operating_hours`, `failed_event`, `avg_load_factor`, `avg_ambient_temp`) | [Parquet (四部件)](datasets/rul_component_failures.parquet) · [CSV (单部件)](datasets/rul_component_failures.csv) |

### Task 3 关键部件统计分布 (Component Breakdown)

| 部件编码 (`component_type`) | 中文名称 | 样本量 ($N$) | 失效事件 ($\delta=1$) | 右删失事件 ($\delta=0$) | 删失率 ($c\%$) | 服役小时极差 (Min–Max h) |
|---|---|---:|---:|---:|---:|---|
| `Main_Bearing` | 主轴承 | 30 | 11 | 19 | 63.3% | 7,120.4 – 51,704.3 |
| `Gearbox_Bearing` | 齿轮箱轴承 | 30 | 11 | 19 | 63.3% | 5,826.1 – 48,932.0 |
| `Generator_Bearing` | 发电机轴承 | 30 | 11 | 19 | 63.3% | 6,340.8 – 47,819.5 |
| `Pitch_Motor` | 变桨电机 | 30 | 11 | 19 | 63.3% | 6,012.7 – 46,250.0 |
| **总计 / 整体宏观统计** | **4 类核心部件** | **120** | **44** | **76** | **63.3%** | **5,826.1 – 51,704.3** |

---

## 快速使用与基准复现 (Quick-Start & Baselines)

### 1. 环境准备与完整性校验

```bash
git clone https://github.com/cheercao/wind-turbine-rul-datasets.git
cd wind-turbine-rul-datasets
pip install -r requirements.txt

# 运行自动化质量与哈希一致性检验脚本
python scripts/validate.py
```

### 2. 标准加载与数据流水线 (Python API)

```python
import pandas as pd
import numpy as np

# -------------------------------------------------------------
# 1. 加载 Task 1 高频载荷序列并提取时序
# -------------------------------------------------------------
fatigue_df = pd.read_parquet("datasets/rul_blade_load_fatigue.parquet")
wt01_loads = fatigue_df[fatigue_df["turbine_id"] == "WT01"]
print(f"[Task 1] WT01 载荷采样点数: {len(wt01_loads)}, 采样频率: 10 Hz")

# -------------------------------------------------------------
# 2. 加载 Task 2 轴承退化时序并拟合指数衰退
# -------------------------------------------------------------
degradation_df = pd.read_parquet("datasets/rul_bearing_degradation.parquet")
wt01_deg = degradation_df[degradation_df["turbine_id"] == "WT01"]
# 对 log(HI) 进行线性拟合: ln(HI) = ln(a) + b * t
poly_fit = np.polyfit(wt01_deg["operating_days"], np.log(wt01_deg["health_index_hi"]), 1)
print(f"[Task 2] WT01 退化率速率参数 b: {poly_fit[0]:.6f}")

# -------------------------------------------------------------
# 3. 加载 Task 3 删失生存数据并统计失效/删失比率
# -------------------------------------------------------------
survival_df = pd.read_parquet("datasets/rul_component_failures.parquet")
n_failed = (survival_df["failed_event"] == 1).sum()
n_censored = (survival_df["failed_event"] == 0).sum()
print(f"[Task 3] 样本总数: {len(survival_df)}, 失效事件: {n_failed}, 右删失: {n_censored} (删失率: {n_censored/len(survival_df):.1%})")
```

---

## 推荐评测协议与性能指标 (Evaluation Protocols & Metrics)

为确保不同研究工作在该基准上具有严格可比性，推荐遵循以下基准测试协议：

1. **Task 1: 雨流疲劳损伤累积**
   - **推荐基线**：ASTM E1049-85 雨流计数法 + Goodman 应力修正 + 典型风机叶片复合材料 S-N 曲线 ($m=10, C=10^{35}$)。
   - **评价指标**：等效循环数 $N_{\text{eq}}$、累积损伤度 $D$、损伤相对误差 (Relative Damage Error)。
2. **Task 2: 退化轨迹与 RUL 预测**
   - **推荐基线**：指数外推模型 (Exponential FHT)、高斯过程回归 (GPR)、双向长短期记忆网络 (BiLSTM)、时间卷积网络 (TCN)。
   - **评价指标**：均方根误差 (RMSE)、平均绝对误差 (MAE)、对称平均绝对百分比误差 (SMAPE)、预测决定系数 ($R^2$)。
3. **Task 3: 考虑右删失的可靠度与生存分析**
   - **推荐基线**：双参数极大似然 Weibull 回归、Kaplan-Meier 乘积限估计、Cox 比例风险模型 (Cox-PH)、深度生存网络 (DeepSurv)。
   - **评价指标**：一致性指数 (Concordance Index, C-index)、积分 Brier 分数 (Integrated Brier Score, IBS)、负对数似然损失 (Negative Log-Likelihood, NLL)。

---

## 仓库拓扑结构 (Repository Topology)

```text
wind-turbine-rul-datasets/
├── datasets/                            # 核心基准数据（Parquet 与 CSV 双格式存储）
│   ├── rul_blade_load_fatigue.csv       # Task 1: 气动-结构叶片载荷高频时序
│   ├── rul_blade_load_fatigue.parquet
│   ├── rul_bearing_degradation.csv      # Task 2: 轴承长程温度残差与健康退化时序
│   ├── rul_bearing_degradation.parquet
│   ├── rul_component_failures.csv       # Task 3: 关键部件服役记录 (单部件版)
│   └── rul_component_failures.parquet   # Task 3: 关键部件服役记录 (四部件综合版)
├── assets/
│   └── dataset-overview.png             # 数据集总览图 (Fig. 1)
├── docs/
│   ├── DATA_CARD.md                     # 数据卡片 (背景、机理范式、物理量标定)
│   ├── DATA_DICTIONARY.md               # 字段字典、张量形状与物理量纲表
│   └── QUALITY_REPORT.md                # 完整性校验与统计分布验证报告
├── scripts/
│   └── validate.py                      # 独立 SHA-256 哈希与数值一致性自动化测试脚本
├── manifest.json                        # 官方校验指纹元数据 (SHA-256, Bytes, Dimensions)
├── requirements.txt                     # 评测基线 Python 依赖清单
├── CHANGELOG.md                         # 版本演进记录
└── README.md                            # 基准项目说明文档
```

---

## 引用 (Citation)

如果您在研究或项目中使用了本项目数据集，可参考以下 BibTeX 格式引用：

```bibtex
@article{windturbine_rul_benchmark_2026,
  title={WindTurbine-RUL: A Multitask Benchmark Dataset for Prognostics and Health Management in Wind Turbines},
  author={Cao, et al.},
  journal={GitHub Repository},
  year={2026},
  url={https://github.com/cheercao/wind-turbine-rul-datasets}
}
```

---

## 许可证 (License)

本项目基于 [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) 许可协议发布。在保留原始出处说明的前提下，可自由使用、分发与二次衍生。
