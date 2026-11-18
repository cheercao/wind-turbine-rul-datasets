# 版本演进记录 (CHANGELOG)

## 数据版本 v1.1.0 (2026-11-18)

- **基准学术化重构 (Benchmark Formalization)**：采用学术基准数据集规范全面重塑 `README.md` 与技术卡片，提出覆盖雨流疲劳、健康退化外推与截尾生存分析的三大标准基准任务（Tasks 1–3）。
- **形式化数学建模与评价协议**：引入严谨的数学表征公式（ASTM E1049 雨流谱、Palmgren-Miner 损伤累积、FHT 首达时间预测、包含右删失项的 Weibull 极大似然估计与 Kaplan-Meier 经验估计），并明确基线评测指标（RMSE, C-index, IBS 等）。
- **学术可视化升级**：更新 `assets/dataset-overview.png` 预览图表为论文三联图标准排版风格。
- **引用与开源协议规范**：补充标准 BibTeX 论文引用规范及 CC BY 4.0 协议说明。

## 数据版本 v1.0.0 (2026-11-18)

- 收录整理叶片高频载荷、轴承健康退化与关键部件寿命记录三组核心数据，提供 CSV / Parquet 双格式共六个数据文件。
- 建立数据清单 `manifest.json`、字段字典、数据卡片及质量校验报告。
- 仓库由 `DATA` 正式命名为 `wind-turbine-rul-datasets`。
