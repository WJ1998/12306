# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/25 0025

import json
from urllib.parse import urlencode
# 自己定义的文件
from login import session
from setting import *


class CheckTicket(object):
    """余票监控类"""
    def __init__(self):
        self.station_to_code = get_station()

    # 获取索引页信息，获取每辆车的信息
    @staticmethod
    def _get_page_index(train_date, from_station, to_station):
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?'
        data = {
            'leftTicketDTO.train_date': train_date,
            'leftTicketDTO.from_station': from_station,
            'leftTicketDTO.to_station': to_station,
            'purpose_codes': 'ADULT'
        }
        url = url + urlencode(data)
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            if data and 'data' in data.keys():
                for item in data['data']['result']:
                    yield item

    # 解析索引页信息
    def parse_page_index(self, train_date, from_station, to_station, category):
        from_station = self.station_to_code[from_station]
        to_station = self.station_to_code[to_station]
        # 用来保存所有有票的车辆
        all_train_own_ticket = []
        index = 0
        for item in self._get_page_index(train_date, from_station, to_station):
            result_list = str(item).split('|')
            # data_to_int 为setting中的字典
            remainder = result_list[data_to_int[category]]
            try:
                if remainder == '有':
                    print('序号：%d, 该车次有票，车次：%s，发车时间：%s，到达时间：%s，历时：%s，%s有余票'
                          % (index, result_list[3], result_list[8], result_list[9], result_list[10], category))
                elif int(remainder) > 0:
                    print('序号：%d, 该车次有票，车次：%s，发车时间：%s，到达时间：%s，历时：%s，%s余票：%d'
                          % (index, result_list[3], result_list[8], result_list[9], result_list[10],
                             category, int(remainder)))
                # print('100005:', result_list)
                # return result_list[0], result_list[15]
            except(ValueError, Exception):
                pass
            else:
                index += 1
                all_train_own_ticket.append(result_list)
        order = int(input('您想购买那一辆车的车票，输入前面的序号：'))
        print('10005:', all_train_own_ticket[order])
        return all_train_own_ticket[order][0], all_train_own_ticket[order][15]

# def main():
#     train_date = '2018-07-22'
#     from_station = '杭州'
#     to_station = '上海'
#     category = '硬座'
#     check_ticket = CheckTicket()
#     secret_str, train_location = check_ticket.parse_page_index(train_date, from_station, to_station, category)
#     print(secret_str)
#     print(train_location)
#
#
# if __name__ == '__main__':
#     main()
