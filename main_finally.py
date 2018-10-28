# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/28 0028

import time
# from playsound import playsound
# import urllib3
# 自己定义的文件
from login import Login
from check_remaining_ticket_finally import CheckTicket
from buy_ticket import BuyTicket

# # 禁用安全请求警告
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    """
    用来控制整个程序的流程
    :return:
    """
    # 登录 Login实例化对象
    login = Login()
    login.download_captcha_picture()
    login.login()

    # 传入格式必须按照 2018-08-01
    train_date = '2018-09-20'
    from_station = '杭州'
    to_station = '上海'
    print('本次您准备要购买的是%s，从%s到%s的火车票！！' % (train_date, from_station, to_station))

    # 余票查询 CheckTicket实例化的对象
    check_ticket = CheckTicket(train_date, from_station, to_station)
    # 买票 BuyTicket实例化的对象
    buy_ticket = BuyTicket(train_date, from_station, to_station)

    number = 0
    while True:
        # 刷票可能出异常，捕获异常
        try:
            # 查票
            secret_str, train_no, train_code, from_station_code, to_station_code, \
                train_location, category, remainder, is_adult = check_ticket.parse_page_index(number)
            time.sleep(1)
            if remainder != '无' and remainder != '':
                print('本次刷票成功！！')
                break
            else:
                print('本次刷票，显示没有票，正在重新刷票！！')
                # number == 0 时，需要输入抢票的信息，以后都不用输入
                number += 1
        except(IndexError, Exception):
            pass
    print('is_adult', is_adult)
    # 买票
    time.sleep(1)
    buy_ticket.buy_ticket_one()
    flag1 = buy_ticket.buy_ticket_two(secret_str)
    if flag1 is None:
        exit()
    # 返回下面请求的一些必要参数
    repeat_submit_token, key_check_is_change, left_ticket_str = buy_ticket.buy_ticket_three()
    # 输出其中一个
    print('repeat_submit_token:', repeat_submit_token)
    # 返回下面请求的一些必要参数
    name, id_num, passenger_type,  phone_num = buy_ticket.buy_ticket_four(repeat_submit_token)
    flag2 = buy_ticket.buy_ticket_five(repeat_submit_token, name, id_num, phone_num, category, is_adult)
    # buy_ticket_two 和 buy_ticket_five 都请求成功说明有票
    if flag1 is True and flag2 is True:
        print('下单基本成功！！')
    # # 下单的第六个请求有没有都没有关系，如果有的话就不用排队，也不一定
    buy_ticket.buy_ticket_six(from_station_code, left_ticket_str, repeat_submit_token, category, train_code,
                              to_station_code, train_location, train_no)

    # # 下单的最后一步 前面都调试好了，再下单
    # buy_ticket.buy_ticket_seven(train_location, key_check_is_change, left_ticket_str, repeat_submit_token,
    #                             name, id_num, phone_num, category, is_adult)
    # print('下单成功！！')
    #
    # # 下单成功播放音乐
    # playsound('music/test.mp3')


if __name__ == '__main__':
    main()
