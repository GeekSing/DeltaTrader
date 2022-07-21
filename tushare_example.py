# -- coding: utf-8 --
'''
@author:generous
@software:pycharm
@datetime:2022/7/13 14:31
@software: PyCharm
@desc:
'''
import tushare as ts

ts.set_token('62bb065f291ac32d39c178e0801ab91521a019ab69e59ddac86efe57')

if __name__ == "__main__":
    pro = ts.pro_api()

    df = pro.daily(ts_code='000001.SZ', start_date='20220712', end_date='20220712')

    print(df)