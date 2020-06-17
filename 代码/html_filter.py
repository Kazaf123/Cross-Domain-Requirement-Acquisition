# -*- coding: utf-8 -*-
"""
@author:Yihui Wang
@software:PyCharm
@file:SimpleFeatureExtraction.py
@time:2019/1/15 8:59

  ━━━━━━神兽出没━━━━━━
  　　　┏┓　　　┏┓
  　　┏┛┻━━━┛┻┓
  　　┃　　　　　　　┃
  　　┃　　　━　　　┃
  　　┃　┳┛　┗┳　┃
  　　┃　　　　　　　┃
  　　┃　　　┻　　　┃
  　　┃　　　　　　　┃
  　　┗━┓　　　┏━┛Code is far away from bug with the animal protecting
  　　　　┃　　　┃    神兽护体,永无bug
  　　　　┃　　　┃
  　　　　┃　　　┗━━━┓
  　　　　┃　　　　　　　┣┓
  　　　　┃　　　　　　　┏┛
  　　　　┗┓┓┏━┳┓┏┛
  　　　　　┃┫┫　┃┫┫
  　　　　　┗┻┛　┗┻┛

  ━━━━━━感觉萌萌哒━━━━━━

"""
import re


def filters(paragraph):
    d1 = filter_emoji(paragraph)  # 去除描述文本中的emoji符号
    d2 = filter_url(d1)  # 去除描述文本中的url
    d3 = filter_char(d2)
    d4 = filter_html_tag(d3)
    return d4


def filter_html_tag(paragraph):
    rule = "<[^>]*>"
    my_re = re.compile(rule, re.S)
    paragraph1 = my_re.sub(". ", paragraph)
    return paragraph1


def filter_url(paragraph):
    my_re = re.compile(r'[a-zA-z]+://[^\s]*', re.S)
    my_re_1 = re.compile(r'www+\.[^\s]*', re.S)
    my_re_2 = re.compile(r'[a-zA-Z0-9_-]+@+[a-zA-Z0-9_-]+\.com', re.S)
    paragraph1 = my_re.sub("", paragraph)
    paragraph2 = my_re_1.sub("", paragraph1)
    paragraph3 = my_re_2.sub("", paragraph2)
    return paragraph3


def filter_char(paragraph):
    paragraph = paragraph.replace(u'\u2019', "'")
    my_re = re.compile(u'['u'\u0628'u'\u0629'u'\u062c'u'\u0631'u'\u0635'u'\u0639'u'\u0642'u'\u0643'u'\u0644'u'\u0645'
                       u'\u0646'u'\u0647'u'\u0648'u'\u064a'                                 
                       u'\u1ecd'
                       u'\u2000-\u206F'  # 一般标点符号
                       u'\xae'
                       u'\xb7'
                       u'\u0300-\u036F'  # 组合音标加符号
                       u'\u0600-\u06FF'  # 基本拉丁文
                       u'\u0100-\u017F'
                       u'\u2100-\u214F'  # 似字母符号
                       u'\u2190-\u21FF'  # 箭头符号
                       u'\u2200-\u22FF'  # 数学运算符号
                       u'\u2400-\u243F'  # 控制图像
                       u'\u25A0-\u25FF'  # 几何符号
                       u'\u2d00-\u2dff'
                       u'\u3000-\u303F'  # 中日符号和标点
                       u'\u2460-\u24FF'
                       u'\u30A0-\u30FF'  # 片假名
                       u'\xa0-\xaf'
                       u'\xe0-\xef'
                       u'\xe9'
                       u'\xb1'
                       u'\xf0-\xff'
                       u'\xf6\xba'
                       u'\u3010'u'\u3011'
                       u'\uf0fc'u'\uff01'
                       u'\u7f8e\u989c\u76f8\u673a'
                       u'\uff00-\uffef'#半角及全角字符
                       u'\ufe0f]+',
                       re.UNICODE)
    return my_re.sub('. ', paragraph)  # 替换字符串中的拉丁文


def filter_emoji(paragraph):
    # print "###############emoji"
    # 过滤字符串中的emoji字符，将其转换为[emoji]
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u2B55]+',
                          re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
                          u'\ud83c[\udf00-\udfff]|'
                          u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                          u'[\u2600-\u2B55])+',
                          re.UNICODE)
    return myre.sub('. ', paragraph)  # 替换字符串中的Emoji

