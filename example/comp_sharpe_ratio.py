# -- coding: utf-8 --
import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt

# 获取3只股票的数据
codes = ['002594.XSHE','300750.XSHE','601012.XSHG']

# 容器:存放夏普
sharpes = []

code_sex = []
# 计算每只股票的夏普比率
for code in codes:
    data = st.get_single_price(code,'daily','2018-10-01','2021-01-01')
    print(data.head())

    # 计算每只股票邪恶夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_shape(data)

    # 计算每只股票的股价
    close = data['close']

    sharpes.append([code,annual_sharpe])   # 存放 [[c1,s1],[c2,s2]..]
    # 画出折线图 用在循环里面可以画出多个图像
    plt.plot(data.index,data['close'],label=code)
    plt.xticks(rotation=30)


    print(sharpes)# 存放股价
    print(code_sex)# 存放股价

# 画图
plt.legend()


# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes,columns=['code','sharpe']).set_index('code')

# 可视化3只股票
code_sex = pd.DataFrame(code_sex,columns=['code','close']).set_index('code')

sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()

