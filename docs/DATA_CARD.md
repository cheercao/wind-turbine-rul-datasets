# 数据卡片 (Data Card): WindTurbine-RUL Benchmark

## 1. 基本信息 (Dataset Metadata)

- **数据集名称**：WindTurbine-RUL: A Multitask Benchmark Dataset for Prognostics and Health Management in Wind Turbines
- **当前版本**：v1.1.0 (2026-11)
- **学科领域**：机械工程、可再生能源、预测与健康管理（PHM）、可靠性工程、时间序列机器学习。
- **开源许可**：Creative Commons Attribution 4.0 International (CC BY 4.0)。

## 2. 研究背景与基准设计原则 (Motivation & Principles)

风电机组属于典型的大型离散、多约束受载机电复合装备。相比传统工业 PHM 基准数据集（如 NASA 轴承或 C-MAPSS 航空发动机）：
1. **真实多时间尺度耦合**：风机叶片面临 10 Hz 级的高频气动交变疲劳，主轴承/齿轮箱轴承表现为日级甚至月级的缓慢磨损退化，而整机群的关键部件则表现为数万小时服役历时下的离散时间-事件过程。
2. **高比例右删失（Right Censoring）特性**：工程实测数据集中，大部分机组及核心部件在观测终止时并未发生故障。直接剔除删失样本会导致生存率严重低估，强行视为故障则会引入系统性伪标签偏差。
3. **多任务兼容性**：本基准同时面向物理退化驱动的物理模型（如 Rainflow-Miner 疲劳损伤）、数据驱动的时序退化追踪模型（如 GPR/LSTM）以及统计可靠性生存分析模型（Weibull MLE / DeepSurv）。

## 3. 子数据集技术规格与范式规范 (Subsets & Paradigms)

### Task 1: 叶片高频实测载荷时序 (`rul_blade_load_fatigue`)
- **样本单元**：6 台风电机组（WT01–WT06）。
- **观测规格**：每台机组连续采集 600 个时间点，采样周期 $\Delta t = 0.1\text{ s}$（采样率 10 Hz），总计 3,600 条记录。
- **物理通道**：包含 1 号、2 号、3 号叶片摆振方向受载信号（`blade_edge_1/2/3`）与发电机转速（`generator_rpm`）。

### Task 2: 轴承长程健康退化轨迹 (`rul_bearing_degradation`)
- **样本单元**：6 台风电机组（WT01–WT06）。
- **观测规格**：每台机组 120 天连续跟踪（`operating_days`: 0–119），总计 720 条记录。
- **物理指标**：轴承温度测点与热平衡预测基线之间的残差（`bearing_temp_residual_degC`）以及多指标融合健康状态量（`health_index_hi`，满足 $0 < HI \le 1.0$）。

### Task 3: 关键部件服役寿命与删失记录 (`rul_component_failures`)
- **样本单元**：120 个风电核心部件服役观测样本。
- **涵盖部件**：主轴承（Main_Bearing, n=30）、齿轮箱轴承（Gearbox_Bearing, n=30）、发电机轴承（Generator_Bearing, n=30）、变桨电机（Pitch_Motor, n=30）。
- **事件分布**：44 次实际故障失效事件（$\delta=1$），76 次右删失记录（$\delta=0$），整体删失率达 63.3%。
- **协变量**：累计运行小时数（`operating_hours`）、服役期平均负载系数（`avg_load_factor`）与平均环境温度（`avg_ambient_temp`）。

## 4. 推荐基准评测协议 (Benchmark Evaluation Protocols)

- **时序与损伤评估**：推荐使用对齐后的统一输入接口，评估模型在等效疲劳循环数及损伤度度量上的泛化性能（MAE、RMSE）。
- **FHT 阈值外推**：退化曲线外推需以到达统一预设阈值（如 $HI_{\text{th}} = 0.2$）的预测天数误差作为核心指标。
- **生存分析评估**：必须采用支持右删失的评估指标（如 C-index、Integrated Brier Score），验证模型在不同协变量下的风险排序与时变生存概率预测能力。
