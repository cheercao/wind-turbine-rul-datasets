<div align="center">

# Wind Turbine RUL Datasets
### 风电机组运行寿命与状态分析真实数据集
**Real-World Wind Turbine Operational & Remaining Useful Life (RUL) Datasets**

**雨流疲劳分析 · 健康指数(HI)退化分析 · Weibull 可靠性与生存分析**

![Data type](https://img.shields.io/badge/Data-Real--world%20Operational-2563eb)
![Formats](https://img.shields.io/badge/Formats-CSV%20%7C%20Parquet-0f766e)
![Records](https://img.shields.io/badge/Records-4%2C440-7c3aed)
![Turbines](https://img.shields.io/badge/Turbines-6%20Units-amber)
![Dataset version](https://img.shields.io/badge/Dataset-v1.0.1-334155)

面向风电机组剩余使用寿命（RUL）预测、健康状态评估、退化趋势跟踪与设备可靠性建模的真实风电运行与状态监测数据集。

[数据文件](datasets/) · [字段字典](docs/DATA_DICTIONARY.md) · [数据说明](docs/DATA_CARD.md) · [质量检查](docs/QUALITY_REPORT.md)

</div>

![风电机组三类数据概览](assets/dataset-overview.png)

## 数据一览

本仓库收录三组面向风电机组关键部件寿命预测与状态评估的核心数据集，每组均提供高效列式存储的 **Parquet** 格式与通用易读的 **CSV** 格式：

| 数据集 | 规模 | 维度 / 采样轴 | 核心应用场景与算法 | 下载文件 |
|---|---|---|---|---|
| **叶片载荷时序** (`rul_blade_load_fatigue`) | 3,600 行 · 6 台机组 (WT01–WT06) | 0.1 秒采样 (10 Hz)；每台机组 600 点时序 | 雨流计数法（Rainflow Counting）、载荷谱统计、疲劳应力分析、Palmgren-Miner 线性累积损伤度计算 | [CSV](datasets/rul_blade_load_fatigue.csv) · [Parquet](datasets/rul_blade_load_fatigue.parquet) |
| **轴承健康退化** (`rul_bearing_degradation`) | 720 行 · 6 台机组 (WT01–WT06) | 0–119 天运行历时；每台机组 120 天跟踪 | 轴承测点温度残差跟踪、健康指数（HI）长周期退化建模、指数/多项式退化曲线拟合、阈值外推与剩余天数预测 | [CSV](datasets/rul_bearing_degradation.csv) · [Parquet](datasets/rul_bearing_degradation.parquet) |
| **部件故障与寿命记录** (`rul_component_failures`) | 120 行 · 4 类风机核心部件 | 实际累计服役运行小时数；含 44 次真实故障与 76 次右删失 | 包含右删失（截尾）数据的 Weibull 可靠度分布拟合（MLE 极大似然估计）、Kaplan-Meier 生存曲线估计、故障率与可靠度建模 | [CSV 单部件版](datasets/rul_component_failures.csv) · [Parquet 四部件版](datasets/rul_component_failures.parquet) |

> **数据统计说明**：4,440 行记录按三个独立数据集统计，CSV 与 Parquet 存储格式一一对应。寿命记录数据集中：Parquet 版本涵盖四类典型关键部件（主轴承、齿轮箱轴承、发电机轴承、变桨电机，各 30 条）；CSV 版本聚焦齿轮箱轴承（120 条）。两版均包含 44 条实际失效与 76 条统计截止时的右删失（存活）记录。

---

## 快速开始

### 1. 克隆仓库与安装依赖

```bash
git clone https://github.com/cheercao/wind-turbine-rul-datasets.git
cd wind-turbine-rul-datasets
python -m pip install -r requirements.txt
python scripts/validate.py
```

### 2. 数据读取与加载示例

```python
import pandas as pd

# 1. 加载叶片高频载荷时序
fatigue_df = pd.read_parquet("datasets/rul_blade_load_fatigue.parquet")
# 或读取 CSV: pd.read_csv("datasets/rul_blade_load_fatigue.csv", parse_dates=["timestamp"])
print("叶片载荷样本 (WT01):")
print(fatigue_df[fatigue_df["turbine_id"] == "WT01"].head())

# 2. 加载轴承健康指数退化数据
degradation_df = pd.read_parquet("datasets/rul_bearing_degradation.parquet")
# 或读取 CSV: pd.read_csv("datasets/rul_bearing_degradation.csv", parse_dates=["date"])
print("\n轴承退化样本 (WT01):")
print(degradation_df[degradation_df["turbine_id"] == "WT01"].head())

# 3. 加载部件服役寿命与故障记录
life_df = pd.read_parquet("datasets/rul_component_failures.parquet")
failed_records = life_df[life_df["failed_event"] == 1]      # 44 条实际失效记录
censored_records = life_df[life_df["failed_event"] == 0]    # 76 条右删失（服役存活）记录

print(f"\n部件寿命记录统计: 失效样本数={len(failed_records)}, 删失样本数={len(censored_records)}")
```

---

## 核心算法对应与工程方法指南

### 1. 雨流计数与疲劳损伤累积（Rainflow Fatigue Analysis）
- **核心字段**：`turbine_id`, `timestamp`, `blade_edge_1/2/3`, `generator_rpm`。
- **算法流程**：
  1. 采用 ASTM E1049 标准雨流循环计数法，从叶片摆振实测载荷信号中提取循环幅值（Range / Amplitude）与均值（Mean）。
  2. 根据部件材料 S-N 疲劳曲线方程计算各级载荷下的许用循环数 $N_i$：
     $$N_i = C \cdot S_i^{-m}$$
  3. 基于 Palmgren-Miner 线性累积损伤准则计算累积损伤度 $D$：
     $$D = \sum_{i} \frac{n_i}{N_i}$$
  4. 结合实测时序长度推算风机叶片或连接结构的等效疲劳损伤与服役剩余寿命。

### 2. 健康指数（HI）退化外推（HI Degradation Modeling）
- **核心字段**：`turbine_id`, `date`, `operating_days`, `bearing_temp_residual_degC`, `health_index_hi`。
- **算法流程**：
  1. `health_index_hi` 反映机组轴承由健康正常（$\approx 1.0$）逐步向劣变退化的演化历程；`bearing_temp_residual_degC` 提供了机组温升热平衡的残差监测指标。
  2. 对每台机组（WT01–WT06）的时序健康指数采用指数衰减模型 $HI(t) = a \cdot e^{b \cdot t}$ 或多项式/高斯过程回归（GPR）进行趋势拟合。
  3. 设定设备报警或失效阈值 $HI_{th}$（如 0.2 或 0.1），外推求解交点天数 $t_{fail}$，得到剩余运行天数 $RUL = t_{fail} - t_{current}$。

### 3. Weibull 可靠度与删失生存分析（Weibull Survival Analysis）
- **核心字段**：`turbine_id`, `component_type`, `operating_hours`, `failed_event`, `avg_load_factor`, `avg_ambient_temp`。
- **算法流程**：
  1. `failed_event=1` 为发生故障停机的确切失效时间点；`failed_event=0` 为统计截止时仍安全运转的样本（右删失/截尾数据，Right Censoring）。
  2. 采用包含右删失项的极大似然估计（MLE）拟合两参数 Weibull 分布：
     $$R(t) = \exp\left(-\left(\frac{t}{\eta}\right)^\beta\right)$$
     其中 $\beta$ 为形状参数（反映早期故障、随机故障或磨损故障阶段），$\eta$ 为特征寿命（尺度参数）。
  3. 利用 Kaplan-Meier 非参数方法对比各部件（主轴承、齿轮箱轴承、发电机轴承、变桨电机）的生存函数 $S(t)$，评估不同机群工况（平均负载、环境温度）对部件寿命的影响。

---

## 仓库目录结构

```text
wind-turbine-rul-datasets/
├── datasets/                            # 核心数据文件（CSV / Parquet 双格式）
│   ├── rul_blade_load_fatigue.csv       # 叶片高频载荷时序（3,600行）
│   ├── rul_blade_load_fatigue.parquet
│   ├── rul_bearing_degradation.csv      # 轴承长周期健康退化时序（720行）
│   ├── rul_bearing_degradation.parquet
│   ├── rul_component_failures.csv       # 部件服役与故障记录（120行，单部件版）
│   └── rul_component_failures.parquet   # 部件服役与故障记录（120行，四部件版）
├── assets/
│   └── dataset-overview.png             # 三类数据集可视化图表
├── docs/
│   ├── DATA_CARD.md                     # 数据集设计背景、工程价值与详细规范
│   ├── DATA_DICTIONARY.md               # 完备字段字典、物理量单位与编码说明
│   └── QUALITY_REPORT.md                # 数据质量、完整性与校验报告
├── scripts/
│   └── validate.py                      # 数据哈希 SHA-256 与结构一致性校验脚本
├── manifest.json                        # 官方数据清单（文件哈希、字节大小、记录数）
├── requirements.txt                     # Python 依赖项
├── CHANGELOG.md                         # 版本变更记录
└── README.md
```

---

## 数据校验与复核

为确保数据在下载传输过程中的完整性，可运行内置校验脚本进行 SHA-256 与结构校验：

```bash
python scripts/validate.py
```

校验脚本会自动核验 6 个数据文件的哈希值、各字段类型、数值范围与双格式一致性。具体哈希清单请参阅 [manifest.json](manifest.json)。

---

## 引用与支持

如果您在风电机组预测性维护（PdM）、剩余寿命预测、SCADA 状态监测等科研或工程项目中使用了本数据集，欢迎引用本项目或提交 Issue / PR 进行交流。
