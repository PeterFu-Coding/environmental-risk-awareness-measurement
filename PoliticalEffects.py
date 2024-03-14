import pyodbc
import json
import numpy as np
provinces = ['河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省',
             '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '四川省', '贵州省',
             '云南省', '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区']
cities = {
    "河北省":"石家庄市",
    "山西省":"太原市",
    "辽宁省":"沈阳市",
    "吉林省":"长春市",
    "黑龙江省":"哈尔滨市",
    "江苏省":"南京市",
    "浙江省":"杭州市",
    "安徽省":"合肥市",
    "福建省":"福州市",
    "江西省":"南昌市",
    "山东省":"济南市",
    "湖北省":"武汉市",
    "湖南省":"长沙市",
    "广东省":"广州市",
    "海南省":"海口市",
    "四川省":"成都市",
    "贵州省":"贵阳市",
    "云南省":"昆明市",
    "陕西省":"西安市",
    "甘肃省":"兰州市",
    "青海省":"西宁市",
    "内蒙古自治区":"呼和浩特市",
    "广西壮族自治区":"南宁市",
    "宁夏回族自治区":"银川市",
    "新疆维吾尔自治区":"乌鲁木齐市",
    "西藏自治区": "拉萨市",
    "河南省": "郑州市"
}
result = {}
results = []
conn = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=Your database;charset=cp936')
cursor = conn.cursor()

for province in provinces:
    # 每个省份的总值
    sum_pro_weight = 0
    # 每个城市的总值
    sum_city_weight = 0
    province_sql = f"select province_info,province_weight from LocationInfo where province_info like '%{province}%'"
    for row in cursor.execute(province_sql):
        result_province_list = row.province_info.split('|')
        result_province_weight = row.province_weight.split('|')
        sum_pro_weight += float(result_province_weight[result_province_list.index(province)])
    city_sql = f"select points_name,points_weight from LocationInfo where points_name like '%{cities[province]}%'"
    for row2 in cursor.execute(city_sql):
        result_city_list = row2.points_name.split('|')
        result_city_weight = row2.points_weight.split('|')
        for i in range(len(result_city_list)):
            if cities[province] in result_city_list[i]:
                sum_city_weight += float(result_city_weight[i])
    result[province] = [sum_pro_weight,sum_city_weight,sum_city_weight/sum_pro_weight]
    results.append(sum_city_weight/sum_pro_weight)

with open('PoliticalEffects.json','w',encoding='utf-8') as fp:
    json.dump(result, fp, indent=2,ensure_ascii=False)
print(np.mean(results))
print(np.std(results))
