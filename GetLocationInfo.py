import json
from delete_locations import clear_locations
from LAC import LAC
from LocationInfoGrasper import location_bd, location_gd
from LocationInfoGrasper import get_d_name
import pandas as pd
from redis import Redis
from Stack import Stack


def Get_key_location(text) -> object:
    """‘
    获取文章中核心的地理实体，并返回地理实体所在的坐标。
    :param text: String,包含地理信息的新闻
    :return: 返回文章核心地理信息，包括’entire‘地理实体名称，‘weight'未归一化的地理信息权重，’longitude‘地理经度，'latitude'地理纬度
    pro_pd代表着省信息，包括省名和权重信息，confidence代表置信度
    """

    redis_conn = Redis(host='your host', port='port')

    print('-----1、开始获取-----')
    # LAC最优，用于GIR
    lac = LAC(mode='lac')
    lac.load_customization('corpus.txt', sep=None)
    words = lac.run(text)
    # locations = [words[0][i] for i in range(len(words[0])) if words[1][i] == 'LOC']
    locations_pd = pd.DataFrame([], columns=['loc', 'count', 'weight'])
    ### 此处为根据modifiers的数量为地名的confidence进行修正
    loc_stack = Stack()
    result_stack = []
    for i in range(len(words[0])):
        if words[1][i] == 'LOC':
            loc_stack.push(words[0][i])
        else:
            if loc_stack.size() != 0:
                result_stack.append([loc_stack.pop(), 1, (5 / 3) ** loc_stack.size()])
                while not loc_stack.isEmpty():
                    result_stack.append([loc_stack.pop(), 0, 0])
            # 由于顺序被打乱，导致小地方提取不出来，因此把顺序重新颠倒过来
            while result_stack:
                locations_pd.loc[len(locations_pd)] = result_stack.pop()

    print('-----地名信息提取结束-----')
    # 每个行政级别赋予一定的权重
    fp = open('administrative_weight.json', 'r', encoding='utf-8')
    pro_weight = json.load(fp)
    fp.close()

    ## 清除国外的地名
    locations = clear_locations(locations_pd['loc'])

    ## 省名的规范化
    fp = open('province_name_modification.json', 'r', encoding='utf-8')
    full_province = json.load(fp)
    fp.close()

    # 地点信息,weight代表每个地名出现的次数
    location_info = pd.DataFrame([], columns=['province', 'city', 'area', 'location', 'place_weight', 'count_weight'])
    location_set = sorted(set(locations), key=locations.index)
    for loc in location_set:
        print('【' + loc + '】' + '地名信息获取中……')
        if redis_conn.hexists("locations", loc) == 0:
            try:
                _loc = full_province[loc]
            except:
                _loc = loc
                pass
            try:
                result = get_d_name(_loc)
                if result['total'] != 0:
                    # 级别越高赋的值越低，初始化为4，即默认为乡级行政区及以下
                    score = 4
                    index = 0
                    count = 0
                    records = result['records']
                    for info in records:
                        try:
                            # count 表示最大行政级别的编号-1
                            count += 1
                            new_score = pro_weight[info['place_type']]
                            # 选取行政级别最高的结果作为最终的结果，例如“吉林”一词会选取“吉林省”作为最终结果,而非吉林市
                            if new_score < score:
                                score = new_score
                                index = count - 1
                        except:
                            continue
                    place_weight = 0.6 ** score * max(locations_pd[locations_pd['loc'] == loc]['weight'])
                    # 对较为模糊的地名进行准确地判断
                    if score == 4 and len(records) > 1:
                        if result['total'] < 150:
                            _index = 0
                            city = set()
                            province = set()
                            for i in range(len(location_info)):
                                # 优先选择有地级市级的
                                if location_info.iloc[i, 1] is not None:
                                    city.add(location_info.iloc[i, 1])
                            # 省级放在这边重复了一次，时间相对较长
                            for i in range(len(location_info)):
                                # 其次选择省级的
                                if location_info.iloc[i, 0] is not None:
                                    province.add(location_info.iloc[i, 0])
                            for info in records:
                                if info['city_name'] in city:
                                    break
                                _index += 1
                            if index == len(records):
                                index = 0
                                for i in range(len(records)):
                                    if records[i]['province_name'] in province:
                                        break
                                    index += 1
                            if _index == len(records):
                                continue
                            index = _index
                        else:
                            continue
                    info = result['records'][index]
                    if info['province_name'] == '中华人民共和国民政部':
                        continue
                    location_info.loc[len(location_info)] = [info['province_name'], info['city_name'],
                                                             info['area_name'],
                                                             loc,
                                                             place_weight,
                                                             sum(locations_pd[locations_pd['loc'] == loc]['count'])]
                    # 存着省时间
                    if score < 4:
                        infos = str(info['province_name']) + '|' + str(info['city_name']) + '|' + str(
                            info['area_name']) + '|' + str(loc) + '|' + str(place_weight)
                        redis_conn.hset('locations', loc, infos)
            except:
                pass
        else:
            location_info_list = redis_conn.hget('locations', loc).decode('UTF-8').split('|')
            location_info.loc[len(location_info)] = [location_info_list[0], location_info_list[1],
                                                     location_info_list[2],
                                                     location_info_list[3],
                                                     float(location_info_list[4]) * max(
                                                         locations_pd[locations_pd['loc'] == loc]['weight']),
                                                     sum(locations_pd[locations_pd['loc'] == loc]['count'])]
    # 对重复的地名进行整合
    # 将地名拼接在一起
    # 完整的地名
    location_info.fillna('', inplace=True)
    location_info.replace(to_replace='None', value='', inplace=True)
    location_info['entire'] = location_info['province'] + location_info['city'] + location_info['area']
    for i in range(len(location_info)):
        # 判断loc中是否为省级、地级、县级名称，否则添加至最末，避免地名中的重复
        if str(location_info.iloc[i, 3]) not in str(location_info.iloc[i, 6]):
            location_info.iloc[i, 6] = str(location_info.iloc[i, 6]) + str(location_info.iloc[i, 3])
    # 新建一个表装非重复的数据
    non_dul_location_info = pd.DataFrame([], columns=['province', 'entire', 'count_weight', 'place_weight'])
    for loc in set(location_info['entire']):
        non_dul_location_info.loc[len(non_dul_location_info)] = [
            location_info[location_info['entire'] == loc]['province'].iloc[0],
            loc,
            sum(location_info[location_info['entire'] == loc]['count_weight']),
            max(location_info[location_info['entire'] == loc]['place_weight'])]

    # 避免有些count_weight为0的影响程序的进程
    non_dul_location_info.drop(non_dul_location_info[non_dul_location_info['count_weight'] == 0].index, axis=0, inplace=True)
    non_dul_location_info['count_weight'] = non_dul_location_info['count_weight'] / sum(
        non_dul_location_info['count_weight'])
    non_dul_location_info['weight'] = non_dul_location_info['place_weight'] * non_dul_location_info['count_weight']
    # 对每个点位的权重进行归一化
    non_dul_location_info['weight'] = non_dul_location_info['weight'] / sum(non_dul_location_info['weight'])


    print('-----2、地名信息表完成！-----')

    # 省份信息表，供选择出最多的省份
    pro_pd = pd.DataFrame([], columns=['weight', 'pro_name'])
    # 计算每个省份对应的权重总和
    for pro in set(non_dul_location_info['province']):
        sum_weight = sum(non_dul_location_info[non_dul_location_info['province'] == pro]['weight'])
        pro_pd.loc[len(pro_pd)] = [sum_weight, pro]
    print('-----3、省份信息表完成！-----')

    # 降序排列
    pro_pd.sort_values(by='weight', ascending=False, inplace=True)
    # 排序之后需要重置索引
    pro_pd.reset_index(drop=True, inplace=True)
    # 设置某个阈值，说明文章地点的置信度，同时筛掉一部分的错误点
    confidence = 0
    index = 0
    for i in range(len(pro_pd)):
        confidence = confidence + pro_pd.iloc[i, 0]
        if confidence >= 0.8:
            # index包括此处的省份信息，便于后续的提取
            index = i
            break

    # 将获取的省份选择出来
    main_pro = pro_pd.iloc[0:index + 1, 1].tolist()
    # 这个地方不可以直接使用in，会造成模糊，应该使用isin，not in则使用~
    non_dul_location_info = non_dul_location_info.loc[non_dul_location_info['province'].isin(main_pro)]
    pro_pd = pro_pd.iloc[0:index + 1, :]

    locations_coor = pd.DataFrame([], columns=['entire', 'weight', 'longitude', 'latitude'])
    # 地名去重
    for loc in set(non_dul_location_info['entire']):
        locations_coor.loc[len(locations_coor)] = [loc, sum(
            non_dul_location_info[non_dul_location_info['entire'] == loc]['weight']),
                                                          None, None]

    print('-----4、主要地名信息提取完成！-----')

    # 获取地理坐标信息
    fp1 = open('province_to_capital.json', 'r', encoding='utf-8')
    pro_trans = json.load(fp1)
    fp1.close()
    pro_trans.update(pro_trans)

    for i in range(len(locations_coor)):
        address = locations_coor.iloc[i, 0]
        # 获取点数据，直接用省名获取并不合适，所以将省名移除，最低层次为地级市级
        try:
            address = pro_trans[address]
            continue
        except:
            pass
        # 获取经纬度
        coor = location_bd(address=address)
        # 百度encoding中，若是出错则会定位至此
        if coor == [116.413384, 39.910925]:
            coor = location_gd(address=address)
        if coor is None:
            locations_coor.drop(index=i)
            continue
        # 获取经度
        locations_coor.iloc[i, 2] = coor[0]
        # 获取纬度
        locations_coor.iloc[i, 3] = coor[1]
    locations_coor.dropna(how='any', axis=0, inplace=True)

    print('-----5、文章地理坐标信息已提取完成！-----')

    return locations_coor, pro_pd, confidence
