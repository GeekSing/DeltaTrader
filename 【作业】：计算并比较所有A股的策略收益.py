# -- coding: utf-8 --
import data.stock as st
import strategy.ma_strategy as ma
import strategy.base as strat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from jqdatasdk import *

auth('18138398903','6PpiKmr5dyYc') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

stocks = st.get_stock_list() # 获取所有股票列表


if __name__ == "__main__":
    # 存放累计收益率
    cum_profits = pd.DataFrame()

    for stock in stocks:
        start_date = get_security_info(stock).start_date # 获取股票上市日期

        if start_date.year == 2016:
            df = st.get_single_price(stock,'daily','2016-01-01','2020-12-31') # 获取股票

            df = ma.ma_strategy(df) # 双均线策略

            cum_profits[stock] = df['cum_profit'].reset_index(drop=True)  # 存储累计收益率

            # 折线图
            df['cum_profit'].plot(label=stock)


    # 预览
    print(cum_profits)   # 收益率
    # 可视化
    # cum_profits.plot()
    plt.title("Comparison of Ma Strategy Profits")
    plt.show()


