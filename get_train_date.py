# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/7/16 0016

import datetime


class GetTrainDate(object):
    """获取日期"""
    def __init__(self, train_date):
        # 传入格式为 2018-01-01
        self.train_date = train_date

    def get_week_day(self):
        """
        将传入的字符串形如 ‘2018-01-01’ 这样的日期变成字符串 ‘Wed Aug 01 2018’
        :return:
        """
        year, month, day = self.train_date.split('-')
        week_day_dict = {
            0: 'Mon',
            1: 'Tue',
            2: 'Wed',
            3: 'Thu',
            4: 'Fri',
            5: 'Sat',
            6: 'Sun',
        }
        month_to_english = {
            '01': 'Jan',
            '02': 'Feb',
            '03': 'Mar',
            '04': 'Apr',
            '05': 'May',
            '06': 'Jun',
            '07': 'Jul',
            '08': 'Aug',
            '09': 'Sep',
            '10': 'Oct',
            '11': 'Nov',
            '12': 'Dec'
        }
        # 变成日期格式
        date_format = datetime.datetime.strptime(self.train_date, '%Y-%m-%d')
        number = date_format.weekday()
        return week_day_dict[number] + ' ' + month_to_english[month] + ' ' + day + ' ' + year


# def main():
#     get_train_date = GetTrainDate('2018-08-01')
#     result = get_train_date.get_week_day()
#     print(result)
#
#
# if __name__ == '__main__':
#     main()
