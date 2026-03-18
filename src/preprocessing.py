import pandas as pd
import numpy as np
from scipy.stats import shapiro, boxcox, spearmanr, pearsonr, pointbiserialr
from statsmodels.stats.outliers_influence import variance_inflation_factor
import warnings

warnings.filterwarnings('ignore')

class NIPTDataPreprocessor:
    def __init__(self, file_path):
        """
        初始化数据预处理类
        支持 .csv 和 .xlsx 格式
        """
        print(f"正在加载数据: {file_path}")
        if file_path.endswith('.xlsx'):
            self.df = pd.read_excel(file_path)
        else:
            self.df = pd.read_csv(file_path)
        self.original_shape = self.df.shape
            
    def clean_and_encode(self):
        """
        4.1. 数据清洗与编码
        - 筛除与研究目的无关或隐私敏感变量：末次月经、检测日期、染色体非整倍体信息
        - 序数型与二值型变量整数编码
        """
        drop_cols = ['末次月经', '检测日期', '染色体非整倍体信息']
        cols_to_drop = [col for col in drop_cols if col in self.df.columns]
        if cols_to_drop:
            self.df.drop(columns=cols_to_drop, inplace=True)
            
        # 假设存在二值型性别或分类标签，进行简单的类别编码 (根据实际列名调整)
        for col in self.df.select_dtypes(include=['object', 'category']).columns:
            self.df[col] = self.df[col].astype('category').cat.codes
            
        print(f"[数据清洗] 已移除敏感/无关变量，当前数据维度: {self.df.shape}")
        return self.df

    def check_multicollinearity(self, threshold=5.0):
        """
        4.1.1 多重共线性控制
        计算所有连续变量的方差膨胀因子 (VIF)。VIF > 5 视为严重共线性。
        """
        # 筛选出数值型变量进行 VIF 检验
        num_df = self.df.select_dtypes(include=[np.number]).dropna()
        vif_data = pd.DataFrame()
        vif_data["Feature"] = num_df.columns
        vif_data["VIF"] = [variance_inflation_factor(num_df.values, i) for i in range(num_df.shape[1])]
        
        # 依据论文：身高、体重、BMI 存在严重共线性
        high_vif = vif_data[vif_data["VIF"] > threshold]
        if not high_vif.empty:
            print(f"\n[多重共线性警告] 以下变量 VIF > {threshold}，存在严重共线性:")
            print(high_vif.to_string(index=False))
            
        return vif_data

    def handle_outliers(self, columns):
        """
        4.1.3 异常值处理
        采用三标准差原则。注：论文提到需考虑临床意义，若非测量错误则予以保留。
        为便于工程化，这里提供清洗逻辑，并返回异常值的索引供人工/临床二次确认。
        """
        outlier_indices = set()
        for col in columns:
            if col in self.df.columns:
                mean = self.df[col].mean()
                std = self.df[col].std()
                lower_bound = mean - 3 * std
                upper_bound = mean + 3 * std
                
                # 定位异常值
                outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
                outlier_indices.update(outliers.index.tolist())
                
        print(f"\n[异常值检测] 基于三标准差原则，共发现 {len(outlier_indices)} 条可能存在的异常记录。")
        # 如果需要直接删除，可解开下方注释
        # self.df.drop(index=list(outlier_indices), inplace=True)
        return list(outlier_indices)

    def normality_and_transform(self, continuous_cols):
        """
        4.1.2 分布修正
        对连续变量进行 Shapiro-Wilk 正态性检验。
        若 p < 0.05，则尝试 Log 变换与 Box-Cox 变换，并再次检验。
        """
        results = []
        for col in continuous_cols:
            if col not in self.df.columns:
                continue
                
            data = self.df[col].dropna()
            if len(data) < 3: 
                continue
                
            # 原始数据检验
            stat, p_raw = shapiro(data)
            is_normal_raw = p_raw >= 0.05
            
            # Box-Cox 变换 (需确保数据为正)
            p_bc = np.nan
            is_normal_bc = False
            if (data > 0).all():
                try:
                    data_bc, _ = boxcox(data)
                    _, p_bc = shapiro(data_bc)
                    is_normal_bc = p_bc >= 0.05
                    self.df[f'{col}_BoxCox'] = boxcox(self.df[col])[0]
                except Exception:
                    pass
            
            # 记录检验结果
            results.append({
                'Feature': col,
                'Raw_p_value': p_raw,
                'Raw_Normal': is_normal_raw,
                'BoxCox_p_value': p_bc,
                'BoxCox_Normal': is_normal_bc
            })
            
        report_df = pd.DataFrame(results)
        print("\n[分布修正] Shapiro-Wilk 检验与变换结果 (根据论文，18号/21号染色体Z值Box-Cox后应符合正态分布):")
        print(report_df.to_string(index=False))
        return report_df

    def correlation_analysis(self, target_col='Y染色体浓度'):
        """
        4.1.5 特征相关性分析
        - 偏态连续变量: Spearman 秩相关 (阈值 r > 0.3)
        - 正态变量: Pearson 相关 (阈值 p < 0.05, r > 0.2)
        - 二值变量: 点二列相关 (Point-Biserial)
        """
        if target_col not in self.df.columns:
            print(f"[错误] 目标变量 {target_col} 不存在于数据集中。")
            return None

        spearman_res = {}
        pearson_res = {}
        
        target_data = self.df[target_col]
        
        for col in self.df.columns:
            if col == target_col or not pd.api.types.is_numeric_dtype(self.df[col]):
                continue
                
            col_data = self.df[col]
            # 剔除包含 NaN 的行
            valid_idx = target_data.notna() & col_data.notna()
            t_valid = target_data[valid_idx]
            c_valid = col_data[valid_idx]
            
            if len(t_valid) < 2: continue
            
            # Spearman 相关
            s_corr, s_p = spearmanr(c_valid, t_valid)
            spearman_res[col] = {'r': s_corr, 'p_value': s_p}
            
            # Pearson 相关
            p_corr, p_p = pearsonr(c_valid, t_valid)
            pearson_res[col] = {'r': p_corr, 'p_value': p_p}
            
        print(f"\n[相关性分析] 针对目标变量 '{target_col}':")
        # 筛选出满足论文阈值的显著相关变量
        significant_spearman = {k: v for k, v in spearman_res.items() if abs(v['r']) > 0.3}
        print(f"满足 Spearman r > 0.3 的变量数量: {len(significant_spearman)}")
        
        return spearman_res, pearson_res

    def get_processed_data(self):
        """返回处理完毕的数据框"""
        return self.df


if __name__ == "__main__":
    # ---------------- 模块测试与执行入口 ----------------
    # 假设本地数据文件名为 data.csv
    file_path = "data.csv" 
    
    import os
    if not os.path.exists(file_path):
        # 如果没有真实数据，生成一份满足格式的随机假数据用于测试脚本流通性
        print(f"未找到 {file_path}，正在生成测试数据...")
        np.random.seed(42)
        dummy_data = pd.DataFrame({
            '孕妇代码': range(1, 101),
            '孕周': np.random.normal(16, 2, 100),
            'BMI': np.random.normal(24, 3, 100),
            '身高': np.random.normal(160, 5, 100), # 故意制造共线性变量
            '体重': np.random.normal(60, 10, 100),
            'X染色体浓度': np.random.lognormal(mean=0, sigma=0.5, size=100),
            'Y染色体浓度': np.random.lognormal(mean=-3, sigma=1, size=100),
            '检测抽血次数': np.random.randint(1, 4, 100),
            '参考基因组比对比例': np.random.uniform(0.8, 0.99, 100),
            '18号染色体Z值': np.random.normal(1, 0.5, 100),
            '21号染色体Z值': np.random.normal(1, 0.5, 100)
        })
        dummy_data['体重'] = dummy_data['BMI'] * (dummy_data['身高']/100)**2 # 强共线性
        dummy_data.to_csv(file_path, index=False)
        print("测试数据生成完毕。\n" + "-"*40)

    # 1. 实例化预处理对象
    preprocessor = NIPTDataPreprocessor(file_path)
    
    # 2. 数据清洗与编码
    df = preprocessor.clean_and_encode()
    
    # 3. 异常值处理 (选取核心连续变量)
    continuous_vars = ['孕周', 'BMI', 'X染色体浓度', 'Y染色体浓度']
    outliers = preprocessor.handle_outliers(continuous_vars)
    
    # 4. 多重共线性诊断
    vif_report = preprocessor.check_multicollinearity(threshold=5.0)
    
    # 5. 分布修正检验 (Shapiro-Wilk & Box-Cox)
    normality_report = preprocessor.normality_and_transform(
        continuous_vars + ['18号染色体Z值', '21号染色体Z值']
    )
    
    # 6. 特征相关性分析
    s_corr, p_corr = preprocessor.correlation_analysis(target_col='Y染色体浓度')
    
    # 7. 导出处理好的数据
    final_df = preprocessor.get_processed_data()
    print(f"\n预处理流程全部完成。可用于下游建模的最终数据维度: {final_df.shape}")