# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/28 0028

import requests
from setting import *

session = requests.session()


# 通过别人写好的接口识别验证码
def identify_captcha_picture():
    url = 'http://littlebigluo.qicp.net:47720/'
    files = {
        'file': ('captcha_picture.jpg', open('captcha_picture.jpg', 'rb'), 'image/jpeg')
    }
    response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        html = response.text
        print(html)


def main():
    identify_captcha_picture()


if __name__ == '__main__':
    main()
