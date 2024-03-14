# -*- coding: utf-8 -*-
"""
@Time ： 2023/4/3 17:16
@Auth ： Fu Yi
@ID ：2022202050049
"""
import numpy as np
import pyodbc
import pandas as pd
from dataTransmission.GetDataFromdb import GetDataFromDatabase
import matplotlib.pyplot as plt

def GetCoorFromDatabase(keyword, source):
    conn = pyodbc.connect('DRIVER={sql server};server=localhost\SQLEXPRESS;database=ResultNews;charset=cp936')
    cursor = conn.cursor()
    sql_2 =''
    temp_list = []

    for time in range(1980,2023):
        for month in range(1,13):
            if source == '新闻媒体':
                sql_2 = f"select id from News where year(nTime) = {time} and month(nTime) = {month} and nkeyword like '%{keyword}%'"
                sql_3 = 'select * from locationInfo where id in {} and confidence != 0'
            elif source == '学术资料':
                sql_2 = f"select id from Journals where year(nTime) = {time} and month(nTime) = {month} and nkeyword like '%{keyword}%'"
                sql_3 = 'select * from cnki_locationInfo where id in {} and confidence != 0'
            results = GetDataFromDatabase(time=time,btype=['生物入侵' ,'气候变化','人类活动', '自然灾害'],selected='面数据',source=source)
            sum_value = 0
            for result in results:
                sum_value += int(result['value'])
            # 选出符合时间要求的数据
            ids = []
            for row in cursor.execute(sql_2):
                ids.append(row.id)
            sql3 = sql_3.format(tuple(ids))
            if len(ids) == 1:
                sql3 = sql3.replace(',','')
            if len(ids) == 0:
                temp_list.append(np.nan)
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

                weights = geoData['weight'].tolist()
                weight = sum(weights)/sum_value
                temp_list.append(weight)
                print(str(time) + ' ' + str(month) + ' ' + str(weight))
            except Exception as e:
                print(e)
                pass
    return temp_list
news_data_list = GetCoorFromDatabase('地震','新闻媒体')
year = range(1,517)
font1 = {'family': 'Times New Roman', 'weight': 'normal', 'size': 16}
plt.figure(figsize=(20,10))
plt.plot(year,news_data_list,color='grey',marker='o',markeredgecolor='black',markersize='5')
plt.ylabel('Normalized ERV',font1)
plt.ylim(ymin=0)
plt.xlim(xmin=1,xmax=516)
plt.xlabel('Year',font1)

x_labels = range(1980,2023)
x_ticks = range(1,517,12)
plt.xticks(ticks=x_ticks,labels=x_labels,fontproperties='Times New Roman', fontsize=16,rotation=45)
plt.yticks(fontproperties='Times New Roman', fontsize=16)

plt.show()