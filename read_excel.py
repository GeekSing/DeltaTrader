# -- coding: utf-8 --
'''
@author:generous
@software:pycharm
@datetime:2022/7/13 9:20
@software: PyCharm
@desc:
'''
 #引入Excel库的xlrd
import xlrd

from xlrd import xldate_as_tuple

import datetime


#导入需要读取Excel表格的路径

data = xlrd.open_workbook(r'test.xlsx')

table = data.sheets()[0]



#将excel表格内容导入到tables列表中

def import_excel(excel):

  # 提取每一列
  for rown in range(excel.nrows):
        print(excel.row_values(rowx=rown,start_colx=0, end_colx=None))

if __name__ == '__main__':

  #将excel表格的内容导入到列表中

  import_excel(table)

