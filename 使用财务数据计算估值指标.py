# -- coding: utf-8 --

from jqdatasdk import *
import pandas as pd

auth('18138398903','6PpiKmr5dyYc') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

# 设置行列不忽略
pd.set_option('display.max_rows',10000000)
pd.set_option('display.max_columns',10000)

# 使用 Python 计算贵州茅台的最新市值数据
df1 = get_fundamentals(query(valuation),date='2022-05-26')
df1 = df1[df1['code'] == '600519.XSHG']    #找到茅台索引

df2 = df = get_price('600519.XSHG',start_date='2022-05-26',end_date='2022-05-26',frequency='daily',fields = ['open','close','high','low','volume','money'])

sum = df1['capitalization'] * df2['close'][0]
print(sum)
