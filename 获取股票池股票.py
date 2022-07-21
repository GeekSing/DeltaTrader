# -- coding: utf-8 --
'''
@author:generous
@software:pycharm
@datetime:2022/7/13 13:05
@software: PyCharm
@desc:获取股票池股票代码
'''
import data.stock as st

def get_data(index_symbol='000002.XSHG'):

    # 获取股票列表代码:沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol)

    print(stocks)
    print(len(stocks))
    # 获取股票数据
    # for code in stocks:
    #     data = st.get_csv_price(code,'2019-01-01','2021-04-04')
    #     # 预览股票
    #     print("===============",code)
    #     print(data.tail())


def momentum():
    return 0

if __name__ == "__main__":
    # 测试:获取沪深300个股数据
    get_data()