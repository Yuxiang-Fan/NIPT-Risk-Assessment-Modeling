# NIPT-Risk-Assessment-Modeling (CUMCM 2025)

This repository contains the mathematical models and source code developed for the **2025 National Undergraduate Mathematical Contest in Modeling (CUMCM / 高教社杯全国大学生数学建模竞赛)**. 

The project addresses the challenges of **Non-Invasive Prenatal Testing (NIPT)** by modeling fetal DNA fractions and optimizing test timing based on maternal physiological indicators.

## 📖 Project Context & Objectives
Non-Invasive Prenatal Testing (NIPT) is a critical tool for detecting chromosomal abnormalities. However, its accuracy is significantly affected by the **Fetal Fraction (FF)**, which is influenced by factors such as maternal BMI and gestational age. 

Developed within the competition's 72-hour timeframe, this project implements a multi-stage framework to:
1. **Concentration Prediction**: Model the Y-chromosome concentration in male fetuses.
2. **Window Optimization**: Identify optimal detection windows for different maternal BMI groups.
3. **Threshold Calculation**: Determine population-wide detection thresholds considering measurement uncertainty.
4. **Risk Assessment**: Develop a classifier for female fetal abnormalities where direct Y-concentration data is unavailable.

## 🛠️ Methodology & Implementation

The solution is divided into modular solvers corresponding to the core problems defined in the contest:

* **Data Engineering (`src/preprocessing.py`)**: Implements Variance Inflation Factor (VIF) to manage multicollinearity, Shapiro-Wilk tests for normality, and Box-Cox transformations for distribution adjustment.
* **Statistical Modeling (`src/solver_p1.py`)**: Combines Linear Mixed Models (LMM) for effect quantification with an ensemble framework (XGBoost/Random Forest) for fetal fraction prediction.
* **Stochastic Simulation (`src/solver_p2.py`)**: Uses Logistic Growth modeling and Monte Carlo simulations (100 runs) to estimate target concentration timing under measurement noise ($\sigma=0.005$).
* **Optimization (`src/solver_p3.py`)**: Employs a grid-search inversion on a gestational age mesh to identify the 95% population success threshold.
* **Neural Network Classifier (`src/solver_p4.py`)**: A Multi-Layer Perceptron (MLP) architecture (8→300→150→1) for risk assessment, utilizing SHAP (SHapley Additive exPlanations) to analyze feature attribution.

## 📁 Repository Structure

```text
NIPT-Risk-Modeling/
├── src/                     # Core solvers and preprocessing scripts
├── notebooks/               # Preliminary EDA and model validation logs
├── requirements.txt         # Dependencies (PyTorch, XGBoost, SHAP, etc.)
└── README.md                # Project documentation
```

---

# NIPT 风险评估建模 (2025 CUMCM)

本仓库包含了为 **2025 年全国大学生数学建模竞赛（CUMCM / 高教社杯）** 开发的数学模型和源代码。

该项目通过对胎儿 DNA 比例进行建模，并根据母体生理指标优化检测时机，解决了**无创产前检测（NIPT）**中的关键挑战。

## 📖 项目背景与目标
无创产前检测（NIPT）是检测染色体异常的重要工具。然而，其准确性受**胎儿浓度（Fetal Fraction, FF）**的显著影响，而该指标又受孕妇 BMI 和孕周等因素的影响。

本项目在竞赛规定的 72 小时内完成，实现了一个多阶段框架，旨在：
1. **浓度预测**：对男胎的 Y 染色体浓度进行建模。
2. **窗口优化**：针对不同 BMI 组别识别最佳检测窗口。
3. **阈值计算**：考虑测量不确定性，确定全人群的检测成功阈值。
4. **风险评估**：在缺乏直接 Y 染色体浓度数据的情况下，开发针对女胎异常的分类器。

## 🛠️ 研究方法与实现

解决方案按照竞赛定义的核心问题划分为多个模块化求解器：

* **数据工程 (`src/preprocessing.py`)**：实现方差膨胀因子（VIF）以处理多重共线性，使用 Shapiro-Wilk 检验进行正态性检测，并利用 Box-Cox 变换进行分布调整。
* **统计建模 (`src/solver_p1.py`)**：结合线性混合模型（LMM）进行效应量化，并利用集成学习框架（XGBoost/随机森林）进行胎儿浓度预测。
* **随机模拟 (`src/solver_p2.py`)**：使用 Logistic 生长建模和蒙特卡洛模拟（100 次运行），在测量噪声（$\sigma=0.005$）环境下估计目标浓度的达标时间。
* **数值优化 (`src/solver_p3.py`)**：在孕周网格上采用网格搜索反演，以确定 95% 人群达标的成功阈值。
* **神经网络分类器 (`src/solver_p4.py`)**：采用多层感知机（MLP）架构（8→300→150→1）进行风险评估，并利用 SHAP（SHapley Additive exPlanations）分析特征归因。

## 📁 仓库结构

```text
NIPT-Risk-Modeling/
├── src/                     # 核心求解器与预处理脚本
├── notebooks/               # 初步 EDA 与模型验证记录
├── requirements.txt         # 依赖项 (PyTorch, XGBoost, SHAP 等)
└── README.md                # 项目文档
```
