from dataTransmission.GetDataFromdb import GetDataFromDatabase
import matplotlib.pyplot as plt
import pandas as pd

# 新闻媒体和学术资料
btypes = [['生物入侵'], ['气候变化'], ['人类活动'], ['自然灾害']]
sum_result = {}
results = []

for btype in btypes:
    result = pd.DataFrame([],
                          index=['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省',
                                 '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省',
                                 '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '台湾省', '香港特别行政区',
                                 '澳门特别行政区'],
                          columns=range(1980, 2023))
    for year in range(1980, 2023):
        data = GetDataFromDatabase(time=year, btype=btype, selected='面数据', source='学术资料')
        for single_data in data:
            result.loc[single_data['name'], year] = single_data['value']
    sum_result[btype[0]] = result.sum().tolist()
x = range(1980, 2023)
for i in range(43):
    results.append(sum_result['生物入侵'][i] + sum_result['气候变化'][i] + sum_result['人类活动'][i] + sum_result['自然灾害'][i])

sw = []
cc = []
ac = []
nd = []

for a, b, c, d, e in zip(sum_result['生物入侵'], sum_result['气候变化'], sum_result['人类活动'], sum_result['自然灾害'], results):
    if e != 0:
        if a != 0:
            sw.append(a / e)
        else:
            sw.append(None)
        if b != 0:
            cc.append(b / e)
        else:
            cc.append(None)
        if c != 0:
            ac.append(c / e)
        else:
            ac.append(None)
        if d != 0:
            nd.append(d / e)
        else:
            nd.append(None)
    else:
        sw.append(None)
        cc.append(None)
        ac.append(None)
        nd.append(None)

plt.figure()
plt.plot(x, sw, c='brown',
         label='Biological Invasion')
plt.plot(x, cc, c='red', label='Climate Change')
plt.plot(x, ac, c='green',
         label='Anthropogenic Activity')
plt.plot(x, nd, c='blue',
         label='Natural Disaster')

font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 12}
font2  = {'family': 'Times New Roman', 'weight': 'normal', 'size': 9.5}
plt.xticks(x[::5], fontproperties='Times New Roman', fontsize=12)
plt.yticks(fontproperties='Times New Roman', fontsize=12)
plt.ylim(0,1.0)
plt.legend(loc=1, prop=font2)

plt.xlabel(u'Year', font1)
plt.ylabel(u'Normalized ERV', font1)

plt.show()
