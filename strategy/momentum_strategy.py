# -- coding: utf-8 --
'''
@author:generous
@software:pycharm
@datetime:2022/7/12 11:49
@software: PyCharm
@desc:动量策略(正向)
'''
import pandas as pd
import data.stock as st
import numpy as np
import strategy.base as base
import matplotlib.pyplot as plt

def get_data(start_date, end_date, use_cols,index_symbol='000300.XSHG'):
    """
    获取股票收盘价数据，并拼接为一个df
    :param start_date: str
    :param end_date: str
    :param use_cols: list
    :param index_symbol: str
    :return data_concat: df,拼接后的数据表
    """
    # 获取股票列表代码:沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol)
    # 拼接收盘价数据
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks[0:5]:
        data = st.get_csv_price(code,start_date, end_date, use_cols)
        # 预览股票
        print("===============",code)
        # 拼接多个股票的收盘价:日期 股票A收盘价 股票B收盘价 ..
        data.columns = [code] # 设置列索引列表为code
        data_concat = pd.concat([data_concat,data],axis=1)
    # 预览股票数据
    #print(data_concat.tail()) # 尾部后5列
    #exit()
    return data_concat

def momentum(data_concat, shift_n=1, top_n=2):
    """

    :param data_concat: df
    :param shift_n: int,表示业绩统计周期(单位:月)
    :return:
    """
    # 转换时间频率: 日->月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('M').last()   # 把日转换为年
    # 计算过去三个月的N个收益率 = 期末值/期初值 - 1 = (期末-期初) / 期初
    # optional:对数收益率 = log(期末值 / 期初值)
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return.head())
    # print(shift_return.shift(-1))

    # 生成交易信号:收益率排前n的>赢家组合>买入1，排最后n个>输家>卖出>1
    buy_signal = get_top_stocks(shift_return,top_n)
    sell_singal = get_top_stocks(-1 * shift_return, top_n)
    signal = buy_signal -sell_singal
    print(signal.head())
    # 数据预览
    #print(data_month.head())
    print(shift_return)

    # 计算投资组合收益率
    returns = base.caculate_portfolio_return(shift_return, signal, top_n * 2)
    print(returns)

    # 数据预览
    # print(data_month.head())
    return returns

def get_top_stocks(data,top_n):
    """
    找到前n位极值，并转换为信号返回
    :param data: df
    :param top_n: int,表示要产生信号的个数
    :return: signals:df, 放回0~1信号数据表
    """
    # 初始化信号容器
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # print(signals)
    # 对data的每一行进行遍历，找里面的最大值，并利用bool函数标注0或1
    for index,row in data.iterrows():
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int) #ioc函数是提取数据框中的数据
    return signals

if __name__ == "__main__":
    # 测试:获取沪深300个股数据
    data = get_data('2016-01-01','2021-04-04',['date','close'])
    # 测试:动量策略
    returns = momentum(data)
    # 可视化每个月收益率
    returns.plot()
    plt.show()