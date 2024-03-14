import pyodbc
import pandas as pd


def GetDataFromDatabase(time, btype, selected,source):
    conn = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=Your database;charset=cp936')
    cursor = conn.cursor()
    conn2 = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=Your database;charset=cp936')
    cursor2 = conn2.cursor()

    points_dict = {}
    province = {
        "河北省": 0,
        "山西省": 0,
        "辽宁省": 0,
        "吉林省": 0,
        "黑龙江省": 0,
        "江苏省": 0,
        "浙江省": 0,
        "安徽省": 0,
        "福建省": 0,
        "江西省": 0,
        "山东省": 0,
        "湖北省": 0,
        "湖南省": 0,
        "广东省": 0,
        "海南省": 0,
        "四川省": 0,
        "贵州省": 0,
        "云南省": 0,
        "陕西省": 0,
        "甘肃省": 0,
        "青海省": 0,
        "内蒙古自治区": 0,
        "广西壮族自治区": 0,
        "宁夏回族自治区": 0,
        "新疆维吾尔自治区": 0,
        "北京市": 0,
        "天津市": 0,
        "重庆市": 0,
        "上海市": 0,
        "西藏自治区": 0,
        "台湾省": 0,
        "香港特别行政区": 0,
        "澳门特别行政区": 0,
        "河南省": 0
    }
    province_list = []
    colors = {
        '生物入侵':'#00ff00',
        '气候变化':'#03FED2',
        # '气候变化':'#0000ff',
        '人类活动':'yellow',
        '自然灾害':'red',
    }
    if source == '新闻媒体':
        sql_1 = "select keyword from keyword where class1 = '{0}' or class2 = '{0}'"
        sql_2 = "select id,nkeyword from News where year(nTime) = %d"
        sql_3 = 'select * from locationInfo where id in {} and confidence != 0'
    elif source == '学术资料':
        sql_1 = "select keyword from keyword where class1 = '{0}' or class2 = '{0}'"
        sql_2 = "select id,nkeyword from Journals where year(nTime) = %d"
        sql_3 = 'select * from cnki_locationInfo where id in {} and confidence != 0'

    # btype此刻传递的是一个数组
    for s_type in btype:
        points_info = []
        sql1 = sql_1.format(s_type)
        keywords = []
        for row in cursor2.execute(sql1):
            keywords.append(row.keyword)

        # 选出符合时间要求的数据
        ids = []
        ntime = int(time)
        sql2 = sql_2 % ntime
        for row in cursor.execute(sql2):
            keyword_info = row.nkeyword
            row_keyword, row_weights = keyword_info.split('|')
            row_keyword_list = row_keyword.split(',')
            row_weights = row_weights.split(',')
            for i in range(len(row_keyword_list)):
                if row_keyword_list[i] in keywords:
                    ids.append(row.id)
        sql3 = sql_3.format(tuple(ids))
        if len(ids) == 1:
            sql3 = sql3.replace(',','')
        if len(ids) == 0:
            continue

        if selected == '面数据':
            try:
                for data in cursor.execute(sql3):
                    if data.province_info == '' or data.province_weight == '':
                        continue
                    province_info = data.province_info.split("|")
                    province_weight = data.province_weight.split("|")
                    for i in range(len(province_info)):
                        province[province_info[i]] += float(province_weight[i])
            except Exception as e:
                print(e)
                pass

        elif selected == '点数据':
            try:
                temp_geoData = pd.DataFrame([], columns=['name', 'coor', 'weight'])
                geoData = pd.DataFrame([], columns=['name', 'coor', 'weight'])
                for data in cursor.execute(sql3):
                    if data.province_point != '':
                        temp_province_point= data.province_point.split('|')
                        province_point_info = temp_province_point[0].split(',')
                        province_point_weight = temp_province_point[1].split(',')
                        for j in range(len(province_point_info)):
                            province[province_point_info[j]] += float(province_point_weight[j])

                    if data.points_name == '' or data.points_coor == '' or data.points_weight == '':
                        continue
                    else:
                        temp_names = data.points_name.split('|')
                        temp_coor = data.points_coor.split('|')
                        temp_weights = data.points_weight.split('|')
                        for i in range(len(temp_names)):
                            temp_geoData.loc[len(temp_geoData)] = [temp_names[i], temp_coor[i], float(temp_weights[i])]

                for name in set(temp_geoData['name']):
                    geoData.loc[len(geoData)] = [name, temp_geoData[temp_geoData['name'] == name]['coor'].iloc[0],
                                                 sum(temp_geoData[temp_geoData['name'] == name]['weight'])]

                names = geoData['name'].tolist()
                geos = geoData['coor'].tolist()
                weights = geoData['weight'].tolist()

                for i in range(len(names)):
                    geo = [float(geo) for geo in geos[i].lstrip('(').rstrip(')').split(',')]
                    points_info.append({'name': names[i], 'geometry': geo,
                                         'value': float(weights[i]), 'color':colors[s_type]})
                points_dict[s_type] = points_info
            except:
                pass

    if selected == '面数据':
        for i in province:
            province_list.append({'name': i, 'value': province[i]})
        return province_list
    elif selected == '点数据':
        result_max = province[max(province, key=lambda x: province[x])]
        for key in province:
            if result_max == 0:
                break
            province[key] = province[key]/result_max
        result_dict = {'点数据':points_dict,'背景数据':province}
        return result_dict
