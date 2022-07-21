# -- coding: utf-8 --
import time

import pandas as pd
from jqdatasdk import *

auth('18138398903','6PpiKmr5dyYc') #账号是申请时所填写的手机号；密码为聚宽官网登录密码



# 转换周期: 日K转换为月K
# df = get_price('000001.XSHE', start_date='2021-01-01',end_date='2021-01-29',
#                frequency='daily',panel=False)# 获取日K
#
#
# #添加一行
# df['month'] = df.index.month
#
#
#
# df_month = pd.DataFrame()
#
# df_month['open'] = df['open'].resample('M').first()
# df_month['close'] = df['close'].resample('M').last()
# df_month['high'] = df['high'].resample('M').max()
# df_month['low'] = df['low'].resample('M').min()
#
# print(df_month)

# 转换周期: 日K转换为月K
df = get_price('000001.XSHE', start_date='2020-01-01',end_date='2020-12-31',
               frequency='daily',panel=False)# 获取日K

df['month'] = df.index.month

df_month = pd.DataFrame()


df_month['volume'] = df['volume'].resample('M').sum()
df_month['money'] = df['money'].resample('M').sum()

print(df_month)

