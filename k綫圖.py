# -- coding: utf-8 --
'''
@author:generous
@software:pycharm
@datetime:2022/7/12 22:47
@software: PyCharm
@desc:
'''
import datetime
import time
import pandas as pd
from jqdatasdk import *
import os
import data.stock as st
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # 查询当日剩余可调用数据条数
    count = get_query_count()
    print(count['spare'] )
    dt = st.get_single_price('000001.XSHE',start_date='2022-07-15',end_date='2022-07-16',time_freq='1m')
    print(dt)

    # 画折线图
    dt['close'].plot()
    plt.show()



