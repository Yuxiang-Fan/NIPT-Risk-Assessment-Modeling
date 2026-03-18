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
