#!/usr/bin/python3
# __*__ coding:utf-8 __*__

import os
import pandas as pd
from lib.utility.path import DATA_PATH
from lib.zone.city import *
from lib.utility.date import *
from lib.spider.base_spider import SPIDER_NAME

pd.set_option('expand_frame_repr', False)

if __name__ == '__main__':
    city = get_city()
    # 准备日期信息，爬到的数据存放到日期相关文件夹下
    date = get_date_string()
    # 获得 csv 文件路径
    # date = "20180331"   # 指定采集数据的日期
    # city = "sh"         # 指定采集数据的城市
    city_ch = get_chinese_city(city)
    csv_dir = "{0}/{1}/zufang/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date)

    files = list()
    if not os.path.exists(csv_dir):
        print("{0} does not exist.".format(csv_dir))
        print("Please run 'python xiaoqu.py' firstly.")
        print("Bye.")
        exit(0)
    else:
        print('OK, start to process ' + get_chinese_city(city))
    for csv in os.listdir(csv_dir):
        data_csv = csv_dir + "/" + csv
        # print(data_csv)
        files.append(data_csv)

    all_df = pd.DataFrame()
    for file in files:
        print(file)
        df = pd.read_csv(file, names=['time', 'district', 'area', 'xiaoqu', 'layout', 'size', 'price', 'url'])
        all_df = all_df.append(df, ignore_index=True)

    all_df["min_price"] = all_df['price'].map(lambda price :  price if isinstance(price, int) or isinstance(price, float) or '-' not in price else price[:price.index('-')])
    all_df["max_price"] = all_df['price'].map(lambda price :  price if isinstance(price, int) or isinstance(price, float) or '-' not in price else price[price.index('-') + 1:])

    all_df = all_df[['district', 'area', 'xiaoqu', 'layout', 'size', 'min_price', 'max_price', 'price', 'url']]

    save_csv_path = "{0}/{1}/zufang/{2}/{3}".format(DATA_PATH, SPIDER_NAME, city, date + ".csv")
    all_df.to_csv(save_csv_path, index=False)