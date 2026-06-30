# 导入 pandas 用于数据处理和分析
import pandas as pd
# 导入 numpy 用于处理数组和矩阵
import numpy as np
# 导入 matplotlib 用于创建静态、动态和交互式的图形
import matplotlib.pyplot as plt
# 导入 seaborn，它是建立在 matplotlib 之上的一个数据可视化库
import seaborn as sns
# 导入 scipy.stats 用于统计编程
from scipy import stats
from dgl.data.utils import load_graphs



graph, split_dict = load_graphs('../data/processed/elliptic_of_amnet.dgldata')
graph = graph[0]
feat  = pd.DataFrame(graph.ndata['feat'].numpy())
feat.columns = ['f' + str(col) for col in feat.columns]
feat.nunique()



feat['y'] = graph.ndata['label']
feat_q = feat.copy()
for col in feat.columns.difference(['y']):
    print(col)
    feat_q[col] = pd.cut(feat[col], bins=10, labels=False)

    
#plt.rcParams['font.sans-serif'] = ['Times New Roman']

df = feat_q
for col in df.columns[:-1]:  # 这里使用 df.columns[:-1] 来排除最后一列 'y'
    # 对每一列进行分组，并计算 y 的平均值
    df_grouped = df.groupby(col)['y'].mean().reset_index()
    # 创建折线图
    plt.figure(figsize=(10, 3))  # 创建新的图形
    plt.plot(df_grouped[col], df_grouped['y'], marker='o',c='orange')
    plt.xlabel('Bucket')
    plt.ylabel('Average of y')
    plt.savefig(f'{col}_distribution.png', 
                dpi=300,
                bbox_inches='tight',  # 去除图片周围的空白部分
                pad_inches=0.1)  # 设置边距
    
    plt.close()