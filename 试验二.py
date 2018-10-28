# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wanjie time:2018/6/30 0030

import io
from PIL import Image

img = Image.open('captcha_picture.jpg')
roiImg = img.crop((5, 41, 71, 107))

imgByteArr = io.BytesIO()
roiImg.save(imgByteArr, format='PNG')
imgByteArr = imgByteArr.getvalue()
print(imgByteArr)
