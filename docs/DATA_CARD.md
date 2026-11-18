# 数据说明文档 (Data Card): WindTurbine-RUL Benchmark

## 1. 基本信息 (Dataset Metadata)

- **数据集名称**：WindTurbine-RUL: A Multitask Benchmark Dataset for Prognostics and Health Management in Wind Turbines
- **当前版本**：v1.1.0 (2026-11)
- **技术领域**：机械工程、风力发电、预测与健康管理（PHM）、可靠性工程、时序数据分析。
- **开源许可**：Creative Commons Attribution 4.0 International (CC BY 4.0)。

## 2. 工程背景与设计目标 (Motivation & Objectives)

大型风电机组属于典型的大型离散、多约束受载机电设备。相比实验室环境下的单一加速退化测试：
1. **真实多时间尺度特征**：风机叶片承受 10 Hz 级的高频气动交变疲劳载荷，主轴承与齿轮箱轴承表现为长周期日级温升与平缓退化，整机群部件则对应数万小时服役历时下的离散时间-事件过程。
2. **高比例右删失（Right Censoring）**：在实际服役数据中，绝大部分在役部件至统计截止时并未发生故障。直接剔除未失效样本会导致寿命严重低估，强行标记为故障则会引入系统性伪标签偏差。
3. **多任务覆盖**：涵盖物理驱动的疲劳损伤模型（Rainflow-Miner）、数据驱动的状态退化追踪模型（GPR/LSTM）以及统计可靠性生存分析模型（Weibull MLE / DeepSurv）。

## 3. 子数据集技术规格 (Subsets & Specifications)

### Task 1: 叶片高频实测载荷时序 (`rul_blade_load_fatigue`)
- **机组规模**：6 台风电机组（WT01–WT06）。
- **采样规格**：每台机组连续记录 600 个时间点，采样周期 $\Delta t = 0.1\text{ s}$（采样率 10 Hz），总计 3,600 条记录。
- **测点通道**：1 号、2 号、3 号叶片摆振方向载荷信号（`blade_edge_1/2/3`）与发电机转速（`generator_rpm`）。

### Task 2: 轴承长程健康退化轨迹 (`rul_bearing_degradation`)
- **机组规模**：6 台风电机组（WT01–WT06）。
- **观测规格**：每台机组 120 天连续跟踪（`operating_days`: 0–119），总计 720 条记录。
- **状态指标**：轴承温度测点残差（`bearing_temp_residual_degC`）与综合健康状态指数（`health_index_hi`，满足 $0 < HI \le 1.0$）。

### Task 3: 关键部件服役寿命与删失记录 (`rul_component_failures`)
- **样本规模**：120 个风电核心部件服役观测样本。
- **涵盖部件**：主轴承（`Main_Bearing`, n=30）、齿轮箱轴承（`Gearbox_Bearing`, n=30）、发电机轴承（`Generator_Bearing`, n=30）、变桨电机（`Pitch_Motor`, n=30）。
- **事件分布**：44 次故障失效事件（$\delta=1$），76 次右删失记录（$\delta=0$），整体删失率达 63.3%。
- **工况协变量**：累计运行小时数（`operating_hours`）、平均负载系数（`avg_load_factor`）与环境温度（`avg_ambient_temp`）。

## 4. 推荐评测方法 (Evaluation Protocols)

- **时序与损伤评估**：评估模型在等效疲劳循环数及损伤度度量上的误差（MAE、RMSE）。
- **退化与阈值外推**：退化曲线外推需以到达统一预设阈值（如 $HI_{\text{th}} = 0.2$）的预测天数误差作为核心指标。
- **生存分析评估**：采用支持右删失的评估指标（如 C-index、Integrated Brier Score），验证模型在不同工况下的风险排序与时变生存概率预测能力。
