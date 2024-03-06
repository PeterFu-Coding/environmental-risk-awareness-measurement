# encoding: utf-8
import json


def clear_locations(locations):
    fp = open('bbd_world_country.json', 'r', encoding='utf-8')
    foreign_countries = json.dumps(json.load(fp), indent=2, ensure_ascii=False)
    # 除了国外的地名，还有中国的一些关于范围的地名，我们一并剔除
    others = ['联合国', '全球', '世界', '东盟', '白宫', '亚洲',
              '欧洲', '欧盟', '南极洲', '非洲', '南美', '北美',
              '南极', '北极', '北冰洋', '太平洋', '印度洋', '大西洋',
              '大洋洲', '北美洲', '南美洲', '美洲', '华中', '华东',
              '华南', '华北', '西北', '青藏', '江汉', '关中', '东亚',
              '西亚', '南亚', '北亚', '中东', '中亚', '北加州', '加州',
              '不列颠', '哥伦比亚省', '副热带地区', '江南', '江淮', '多国',
              '中国', '关西', '西欧','东欧', '南欧', '北欧', '西非', '东非',
              '北非', '亚太', '珠峰', '中非', '中国海', '金山银山', '陕北',
              '藏南', '青藏高原', '黄淮海', '长江', '黄河', '东海', '南海',
              '黄海','渤海', '欧美']

    location_list = []
    for loc in locations:
        if loc not in others:
            if loc not in foreign_countries:
                location_list.append(loc)
    return location_list
