# -- coding: utf-8 --
"""
用来创建交易策略，生成交易信号
"""
import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    data['buy_singal'] = np.where((data['buy_singal'] == 1)
                                   & (data['buy_singal'].shift(1) == 1),0,data['buy_singal'])  # 当前为1，下一个为1符合条件buy_singal为0，否者buy_singal为本身不变

    data['sell_singal'] = np.where((data['sell_singal'] == -1)
                                   & (data['sell_singal'].shift(1) == -1),0,data['sell_singal'])  # 当前为1，下一个为1符合条件buy_singal为0，否者buy_singal为本身不变
    data['signal'] = data['buy_singal'] + data['sell_singal']
    return data

def calculate_prof_pct(data):
    """
    计算单次收益率:开仓、平仓(开仓的全部股数)
    :param data:
    :return:
    """
    data = data[data['signal'] != 0]  # 筛选条件，signal不为0
    data['profit_pct'] = data['close'].pct_change() # 计算涨跌幅
    data = data[data['signal'] == -1]  # 筛选平仓后的数据: 单次收益
    return data

def calculate_cum_prof(data):
    """
    计算累计收益率（个股收益率）
    :param data: dataframe
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data

def caculate_portfolio_return(data, signal, n):
    """
    计算组合收益率
    :param data: dataframe
    :param signal: dataframe
    :param n: int
    :return: dataframe
    """
    # 投组收益率 （等权重） = 收益率之和 、 股票个数\
    returns = (signal * data.shift(-1)).T.sum() / n
    return returns.shift(1) # 匹配对应的交易月份

def caculate_max_drawdown(data):
    """
    计算最大回撤比
    :param data:
    :return:
    """
    # 选取时间周期 （时间窗口）
    window = 252
    # 计算时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=252,min_periods=1).max()
    # 计算当天的回撤比 = (股值 - 峰值)/峰值 = 谷值、峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window,min_periods=1).min()

    return data




#def calculate_prof_pct2(data):
    """
    计算单次收益率:开仓、平仓(开仓的全部股数)
    :param data:
    :return:
    """
    # data.loc[data[data['signal'] != 0],data['close'].ptc_change()]
    # data = data[data['signal'] == -1]  # 筛选条件，signal不为0
    #return data

def calculate_shape(data):
    """
    计算夏普比率，返回的是年华的夏普比率
    :param data: dataframe,stock
    :return:
    """
    # 公式:shape = (回报率的均值 - 无风险利率) / 回报率的标准差
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普: 每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe,sharpe_year

