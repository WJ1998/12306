# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/7/16 0016

import datetime


def get_week_day(date):
    week_day_dict = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    day = date.weekday()
    return week_day_dict[day]


def main():
    today = datetime.datetime.now()
    print(today)
    print(str(today)[:10])
    print(type(str(today)[:10]))
    result = get_week_day(today)
    print(result)

    date = '2018-08-01'
    data_data_time = datetime.datetime.strptime(date, '%Y-%m-%d')
    print(data_data_time)
    print(get_week_day(data_data_time))


if __name__ == '__main__':
    main()
