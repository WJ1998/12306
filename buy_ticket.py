# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/25 0025

import re
import json
import datetime
from urllib.parse import unquote
# 自己定义的文件
from login import session
from get_train_date import GetTrainDate
from setting import *


class BuyTicket(object):
    """购票类"""
    def __init__(self, train_date, from_station, to_station):
        """
        初始化方法
        :param str train_date:
        :param str from_station:
        :param str to_station:
        """
        self.train_date = train_date
        self.from_station = from_station
        self.to_station = to_station
        # GetTrainDate类实例化的对象用来将 字符串‘2018-08-01’变成‘Wed Aug 01 2018’
        self.get_train_data = GetTrainDate(train_date)

    @staticmethod
    def buy_ticket_one():
        """
        下单的第一个请求
        :return:
        """
        # # 验证有没有登录成功
        # # 个人中心链接
        # url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        # response = session.get(url, headers=headers)
        # if response.status_code == 200:
        #     html = response.text
        #     print(html)
        # exit()
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = {
            '_json_att': ''
        }
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            print('100006:', data)

    def buy_ticket_two(self, secret_str):
        """
        下单的第二个请求
        :param secret_str:
        :return:
        """
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        today = datetime.datetime.now()
        back_train_date = str(today)[:10]
        data = {
            'back_train_date': back_train_date,
            'purpose_codes': 'ADULT',
            'query_from_station_name': self.from_station,
            'query_to_station_name': self.to_station,
            'secretStr': unquote(secret_str),
            'tour_flag': 'dc',
            'train_date': self.train_date,
            'undefined': ''
        }
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            print('100007:', data)
            if '未处理的订单' in str(data['messages']):
                print('您还有未处理的订单！！，请您先处理完未完成的订单在进行抢票！！')
                return None
            if data['status'] is True:
                return True

    @staticmethod
    def buy_ticket_three():
        """
        下单的第三个请求（这个请求比较特殊，返回值中有接下来请求的必要参数）
        :return:
        """
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {
            '_json_att': ''
        }
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            # print(html)
            result1 = re.findall("globalRepeatSubmitToken = '(.*?)';", html)[0]
            result2 = re.findall("'key_check_isChange':'(.*?)',", html)[0]
            result3 = re.findall("'leftTicketStr':'(.*?)',", html)[0]
            print('result1:', result1)
            print('result2:', result2)
            print('result3:', result3)
            return result1, result2, result3

    @staticmethod
    def buy_ticket_four(repeat_submit_token):
        """
        下单的第四个请求
        :param repeat_submit_token:
        :return:
        """
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token
        }
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            print('100008:', data)
            if data and 'data' in data.keys():
                normal_passengers = data['data']['normal_passengers'][0]
                return normal_passengers['passenger_name'], normal_passengers['passenger_id_no'], \
                    normal_passengers['passenger_type'], normal_passengers['mobile_no']

    @staticmethod
    def buy_ticket_five(repeat_submit_token, name, id_num, phone_num, category, is_adult):
        """
        下单的第五个请求
        :param repeat_submit_token:
        :param name:
        :param id_num:
        :param phone_num:
        :param category:
        :param is_adult:
        :return:
        """
        # # 验证有没有登录成功
        # # 个人中心链接
        # url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        # response = session.get(url, headers=headers)
        # if response.status_code == 200:
        #     html = response.text
        #     print(html)
        if is_adult is True:
            passenger_type = '1'
        else:
            passenger_type = '3'
        category = seat_to_int[category]
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            '_json_att': '',
            'bed_level_order_num': '000000000000000000000000000000',
            'cancel_flag': '2',
            'oldPassengerStr': '{},{},{},{}_'.format(name, passenger_type, id_num, passenger_type),
            'passengerTicketStr': '{},0,{},{},1,{},{},N'.format(category, passenger_type, name, id_num, phone_num),
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token,
            'tour_flag': 'dc',
            'whatsSelect': 1
        }
        # print(data)
        response = session.post(url, headers=headers, data=data)
        # print(response)
        if response.status_code == 200:
            html = response.text
            # print(html)
            data = json.loads(html)
            print('100009:', data)
            if data['data']['submitStatus'] is True:
                return True

    # 下单的第六个请求 category表示座位类别 比如硬座，硬卧等
    def buy_ticket_six(self, from_station_code, left_ticket_str, repeat_submit_token,
                       category, train_code, to_station_code, train_location, train_no):
        category = seat_to_int[category]
        train_data = self.get_train_data.get_week_day()
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            '_json_att': '',
            'fromStationTelecode': from_station_code,
            'leftTicket': left_ticket_str,
            'purpose_codes': '00',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token,
            'seatType': category,
            'stationTrainCode': train_code,
            'toStationTelecode': to_station_code,
            'train_date': train_data + ' 00:00:00 GMT+0800',
            'train_location': train_location,
            'train_no': train_no,
        }
        print(data)
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            print('100000010:', data)

    @staticmethod
    def buy_ticket_seven(train_location, key_check_is_change, left_ticket_str, repeat_submit_token,
                         name, id_num, phone_num, category, is_adult):
        """
        下单的第七个请求
        :param train_location:
        :param key_check_is_change:
        :param left_ticket_str:
        :param repeat_submit_token:
        :param name:
        :param id_num:
        :param phone_num:
        :param category:
        :param is_adult:
        :return:
        """
        if is_adult is True:
            passenger_type = '1'
        else:
            passenger_type = '3'
        category = seat_to_int[category]
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            '_json_att': '',
            'choose_seats': '',
            'dwAll': 'N',
            'key_check_isChange': key_check_is_change,
            'leftTicketStr': left_ticket_str,
            'oldPassengerStr': '{},{},{},{}_'.format(name, passenger_type, id_num, passenger_type),
            'passengerTicketStr': '{},0,{},{},1,{},{},N'.format(category, passenger_type, name, id_num, phone_num),
            'purpose_codes': '00',
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': repeat_submit_token,
            'roomType': '00',
            'seatDetailType': '000',
            'train_location': train_location,
            'whatsSelect': '1'
        }
        print(data)
        response = session.post(url, headers=headers, data=data)
        if response.status_code == 200:
            html = response.text
            data = json.loads(html)
            print('1000011:', data)
