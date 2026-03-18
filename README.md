# NIPT-Risk-Assessment-Modeling

This repository contains the source code and methodology developed for the **2025 National Undergraduate Mathematical Contest in Modeling (CUMCM / 高教社杯全国大学生数学建模竞赛)**. 

Our project focuses on enhancing the accuracy and reliability of **Non-Invasive Prenatal Testing (NIPT)** by modeling fetal chromosome fraction and optimizing the timing of tests based on maternal physiological indicators.

## 🏆 Project Context
* **Contest:** 2025 CUMCM (National Undergraduate Mathematical Contest in Modeling)
* **Team:** Students from **Tongji University**
* **Theme:** Statistical Analysis and Machine Learning in Prenatal Diagnostics

## 📖 Overview
Non-Invasive Prenatal Testing (NIPT) is crucial for detecting fetal chromosomal abnormalities. However, test efficacy is heavily influenced by the **Fetal Fraction (FF)**, which correlates with maternal BMI, gestational age, and other biological factors. 

This project implements a multi-stage modeling framework to:
1.  Predict the Y-chromosome concentration in male fetuses.
2.  Map the optimal detection windows for different maternal BMI groups.
3.  Inverse-calculate the population-wide detection threshold under measurement uncertainty.
4.  Develop a robust classifier for female fetal abnormalities where Y-concentration data is unavailable.

## 🛠️ Project Structure
The code is organized into modular solvers corresponding to the core challenges addressed during the competition:

- `src/preprocessing.py`: **Data Engineering Pipeline**. Implements VIF (Variance Inflation Factor) to control multicollinearity, Shapiro-Wilk tests for normality, and Box-Cox transformations for distribution correction.
- `src/solver_p1.py`: **Regression Analysis**. Utilizes Linear Mixed Models (LMM) to quantify individual effects and a Stepped Ensemble Framework (XGBoost/Random Forest) to predict fetal fraction.
- `src/solver_p2.py`: **Stochastic Simulation**. Employs Logistic Growth modeling and 100-run Monte Carlo simulations to estimate target concentration timing under measurement noise ($\sigma=0.005$).
- `src/solver_p3.py`: **Optimization & Bayesian Inversion**. Features a grid-search inversion on a gestational age mesh to identify the 95% population success threshold.
- `src/solver_p4.py`: **Deep Learning Classifier**. A Multi-Layer Perceptron (MLP) architecture (8→300→150→1) for female fetal risk assessment, integrated with SHAP for feature attribution and model interpretability.

## 🚀 Key Methodologies
- **Uncertainty Quantificaton**: We didn't just provide point estimates; we used Monte Carlo methods to provide "buffer zones" for clinical safety.
- **Interpretability**: Used SHAP (SHapley Additive exPlanations) to ensure the neural network decisions align with clinical observations.
- **Robustness**: Validation was performed using 5-Fold Cross-Validation and Permutation Tests ($p=0.0099$) to ensure the results were statistically significant and not due to random noise.

## 📈 Results (Contest Summary)
While developed within the intensive 72-hour window of the competition, our MLP-based classifier achieved:
- **AUC**: 0.9688
- **Recall**: 0.9204
- **F1-Score**: 0.9286


## 📄 License
This project is open-source under the [MIT License](LICENSE). 
The data provided for the contest is proprietary to the CUMCM Organizing Committee.

---
*Developed with ❤️ by Yuxiang Fan and teammates at Tongji University.*
