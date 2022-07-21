# -- coding: utf-8 --
from jqdatasdk import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

auth('18138398903','6PpiKmr5dyYc') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

# 设置行列不忽略
pd.set_option('display.max_rows', 10000000)
pd.set_option('display.max_columns', 10000)

def get_data(code):
    return get_price(code,'2019-01-01','2020-12-31',frequency='daily', panel=False)

def compose_signal(data):
    data['buy_singal'] =np.where((data['buy_singal'] == 0) &
                                 (data['buy_singal'].shift(1) == 1),0,data['buy_singal'])     #当前为0，下一个为1，则0，否者不变

    data['sell_singal'] = np.where((data['sell_singal'] == -1) &
                                  (data['sell_singal'].shift(1) == 0), -1, data['sell_singal'])  # 当前为0，下一个为1，则0，否者不变

    data['singal'] =  data['buy_singal'] + data['sell_singal']

    return data

def calculate_prof_pct(data):
    """
    计算涨跌幅
    :param data:
    :return:
    """
    data= data[data['singal'] != 0]
    data['profit_pct']= (data['close'] - data['close'].shift(1)) /data['close'].shift(1)
    data=data[data['singal'] == -1]
    return data

def  calculate_cum_prof(data):
    """
    计算收益率
    :param data:
    :return:
    """
    data['cum_proid'] = pd.DataFrame(1+data['profit_pct']).cumprod() - 1
    return data

def week_period_strateg(data):
    # 新增加一列时间
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_singal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_singal'] = np.where((data['weekday'] == 0), -1, 0)

    data = compose_signal(data) #整合信号
    data = calculate_prof_pct(data) #计算涨跌幅
    data = calculate_cum_prof(data) #计算收益率
    return data

if __name__ == "__main__":
    list_code = ['000001.XSHE','000002.XSHE','000009.XSHE']
    data_frame = pd.DataFrame()
    for code in list_code:
        df = get_data(code)
        df = week_period_strateg(df)
        data_frame[str(code)+'_cum_proid'] = df['cum_proid']
        df['cum_proid'].plot() #画折线图
        plt.show()
    print(data_frame)