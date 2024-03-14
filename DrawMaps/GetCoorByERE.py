# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/3 17:16
@Auth ： Fu Yi
@ID ：2022202050049
"""
import pyodbc
import pandas as pd
from dataTransmission.GetDataFromdb import GetDataFromDatabase

def GetCoorFromDatabase(keyword, source):
    conn = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=ResultNews;charset=cp936')
    cursor = conn.cursor()

    coor_file = open(f'{keyword}_coor_{source}.txt','w',encoding='utf-8')
    sql_2 =''

    for time in range(1980,2023):
        if source == '新闻媒体':
            sql_2 = f"select id from News where year(nTime) = {time} and nkeyword like '%{keyword}%'"
            sql_3 = 'select * from locationInfo where id in {} and confidence != 0'
        elif source == '学术资料':
            sql_2 = f"select id from Journals where year(nTime) = {time} and nkeyword like '%{keyword}%'"
            sql_3 = 'select * from cnki_locationInfo where id in {} and confidence != 0'
        results = GetDataFromDatabase(time=time,btype=['生物入侵' ,'气候变化','人类活动', '自然灾害'],selected='面数据',source=source)
        sum_value = 0
        for result in results:
            sum_value += int(result['value'])
        sum_value = sum_value/10000
        # 选出符合时间要求的数据
        ids = []
        for row in cursor.execute(sql_2):
            ids.append(row.id)
        print(str(time)+' '+str(len(ids)))
        sql3 = sql_3.format(tuple(ids))
        if len(ids) == 1:
            sql3 = sql3.replace(',','')
        if len(ids) == 0:
            continue

        try:
            temp_geoData = pd.DataFrame([], columns=['name', 'coor', 'weight'])
            geoData = pd.DataFrame([], columns=['name', 'coor', 'weight'])
            for data in cursor.execute(sql3):
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
                if weights[i] >= 1:
                    coor_file.write(names[i]+' '+str(time)+' '+str(geo[0])+' '+str(geo[1])+' '+str(weights[i]/sum_value)+'\n')
        except Exception as e:
            print(e)
            pass

GetCoorFromDatabase('大风','学术资料')