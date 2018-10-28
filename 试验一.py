# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/26 0026

data = {'3': '1330', 'A1': '¥75.0', '1': '750', 'A4': '¥205.0', 'A3': '¥133.0', '4': '2050', 'OT': [], 'WZ': '¥75.0', 'train_no': '5a0000K30820'}
print(data)
mark_to_seat = {
    'A9': '商务特等座',
    'M': '一等座',
    'O': '二等座',
    'A4': '软卧',
    'A3': '硬卧',
    'A1': '硬座',
    'WZ': '无座'
}

seat_to_price = {}
for key in data.keys():
    if key in mark_to_seat.keys():
        seat_to_price[mark_to_seat[key]] = data[key]
print(seat_to_price)
