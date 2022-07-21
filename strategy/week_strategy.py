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
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]  # 筛选条件，signal不为0
    return data

def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data: dataframe
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1+data['profit_pct']).cumprod() - 1
    return data

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
    :param data:
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

def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # print(data)
    #exit()
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_singal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_singal'] = np.where((data['weekday'] == 0), -1, 0)

    # # 模拟重复买入: 周五再次买入
    # data['buy_singal'] = np.where((data['weekday'] == 3)  |  (data['weekday'] == 4),1,0)          #满足条件为1，不满足为0

    # 模拟重复买入: 周二再次买入
    #data['sell_singal'] = np.where((data['weekday'] == 0)  |  (data['weekday'] == 1),-1,0)          #满足条件为1，不满足为0


    data = compose_signal(data)  # 整合型号
    data = calculate_prof_pct(data) # 计算涨跌幅
    data = calculate_cum_prof(data) # 计算收益率
    # data = caculate_max_drawdown(data) # 最大回撤

    return data

if __name__ == "__main__":
    # df = week_period_strategy('000001.XSHE','daily',None,datetime.date.today())
    # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    # print(df.describe())
    # df['cum_profit'].plot()  #画曲线图
    # plt.show()

    # 查看平安银行最大回撤
    # df = st.get_single_price('000001.XSHE','daily','2006-01-01','2021-01-01')
    # df = caculate_max_drawdown(df)
    # print(df[['close','roll_max','daily_dd','max_dd']])
    # df[['daily_dd','max_dd']].plot()
    # plt.show()

    # 计算夏普比率
    df = st.get_single_price('000001.XSHE','daily','2006-01-01','2021-01-01')
    sharpe = calculate_shape(df)
    print(sharpe)