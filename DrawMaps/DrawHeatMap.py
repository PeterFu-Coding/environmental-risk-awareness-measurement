# -*- encoding:utf-8 -*-

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from dataTransmission.GetDataFromdb import GetDataFromDatabase
btypes = [['生物入侵', '气候变化', '人类活动', '自然灾害']]
for btype in btypes:
    result = pd.DataFrame([],
                          index=['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省',
                                 '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省',
                                 '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '台湾省', '香港特别行政区',
                                 '澳门特别行政区'],
                          columns=range(1980,2023))
    for year in range(1980, 2023):
        data = GetDataFromDatabase(time=year, btype=btype, selected='面数据', source='学术资料')
        max = 1
        for single_data in data:
            if single_data['value'] > max:
                max = single_data['value']
        for single_data in data:
            result.loc[single_data['name'], year] = single_data['value'] / max
    result.index = ['Beijing', 'Tianjin', 'Hebei', 'Shanxi', 'Inner Mongolia', 'Liaoning', 'Jilin', 'Heilongjiang',
                    'Shanghai', 'Jiangsu', 'Zhejiang', 'Anhui', "Fujian", 'Jiangxi', 'Shandong', 'Henan', 'Hubei',
                    'Hunan', 'Guangdong', 'Guangxi', 'Hainan', 'Chongqing', 'Sichuan', 'Guizhou', 'Yunnan', 'Tibet',
                    'Shaanxi', 'Gansu', 'Qinghai', 'Ningxia', 'Xinjiang', 'Taiwan', 'Hong Kong', 'Macao']
    result = result.astype(float)
    plt.rc('font', family='Times New Roman')
    plot = sns.heatmap(result, vmin=0, vmax=1, cmap="Reds")
    plt.tight_layout()
    plt.yticks(ticks=np.arange(1, len(result.index) + 1), labels=result.index, fontproperties='Times New Roman',
               verticalalignment='bottom')
    plt.xticks(rotation=45)

    plt.tick_params(bottom=False, top=False, left=False, right=False)
    plt.xlabel("Year", fontproperties='Times New Roman')
    plt.ylabel("Province", fontproperties='Times New Roman')
    plt.show()
