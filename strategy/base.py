# -- coding: utf-8 --
"""
用来创建交易策略，生成交易信号
"""
import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe, 包含单次收益率数据
    :return results: dict, 评价指标数据
    """

    # 评估策略效果:总收益率、年化收益率、最大回撤、夏普比
    data = calculate_cum_prof(data)
    print(data)
    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]
    # 计算年化收益率 （每月开仓）
    annual_return = data['profit_pct'].mean() * 12

    # 计算近一年最大回撤
    data = caculate_max_drawdown(data,window=12)
    print(data)

    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]

    # 计算夏普比率
    sharpe, annual_sharpe = calculate_shape(data)

    # 放到dict中
    results = {'总收益率':total_return,'年化收益率':annual_return ,
              '最大回撤':max_drawdown,'夏普比率': annual_sharpe}
    # print()

    # 打印评估指标
    for key,value in results.items():
        print(key,value)

    return data

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
    :return returns: dataframe
    """
    print(data)
    returns = data.copy()
    # 投组收益率 （等权重） = 收益率之和 、 股票个数\
    returns['profit_pct'] = (signal * data.shift(-1)).T.sum() / n
    returns = calculate_cum_prof(returns)
    return returns.shift(1) # 匹配对应的交易月份

def caculate_max_drawdown(data,window=252):
    """
    计算最大回撤比
    :param data:
    :param window: int,时间窗户设置，默认为252(日k)
    :return
    """
    # 模拟持仓金额:投入的总金额 * (1+收益率)
    data['close'] = 10000 * (1+data['cum_profit'])
    data['roll_max'] = data['close'].rolling(window=window,min_periods=1).max()
    # 计算当天的回撤比 = (股值 - 峰值)/峰值 = 谷值/峰值 - 1
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
    # daily_return = data['close'].pct_change() # 演示部分
    daily_return = data['profit_pct'] # 策略应用后
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普: 每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe,sharpe_year

