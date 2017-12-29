'''
(first real) code by yeti

this script downloads all the stock price history data from
tushare.org, and store data in csv format in the \data\
folder, with stock id number as filename.

ver 0.1
'''

import tushare as ts
import os
import datetime
import pandas as pd


def stock_id_gen():
    with open('股票代码.txt') as fh:
        stock_list = []
        i = 0
        for line in fh:
            id_start_loc = line.find('(') + 1
            stock_id = line[id_start_loc:(id_start_loc + 6)]
            # slice the stock_id
            if stock_id.startswith('00') or stock_id.startswith('300') or stock_id.startswith('60'):
                # checks if meets above criteria then append stock_list
                stock_list.append(stock_id)
        stock_list.sort()
    return stock_list


def save_path_gen(stock_id):
    # returns path string, stock id as filename
    file_path = os.getcwd() + '\\data\\' + stock_id + '.csv'
    return file_path


def join_date(y, d):
    return str(y) + d


def year_splitter(start_date, end_date):
    # returns a list of [start,end] lists for the download_data() function
    start_to_end = []
    start_year = int(start_date.split('-')[0])
    start_day = start_date[4:]
    # start_day string format: -mm-dd
    end_year = int(end_date.split('-')[0])
    end_day = end_date[4:]
    while True:
        if end_year - start_year > 2:
            slice = [join_date((end_year - 2), end_day), join_date(end_year, end_day)]
            end_year = end_year - 2
            start_to_end.append(slice)
        else:
            slice = [join_date(start_year, start_day), join_date(end_year, end_day)]
            start_to_end.append(slice)
            break
    return start_to_end


def download_data(stock_id, start_to_end):
    # downloads stock_id to \data\ as stock_id.csv
    df = None
    print('trying to download', stock_id)
    try:
        for period in start_to_end:
            data = ts.get_k_data(stock_id, period[0], period[1])
            df = pd.concat([df, data])
        df.set_index('date').sort_index().to_csv(save_path_gen(stock_id))
        print(stock_id, 'download finished!')
    except:
        print(stock_id, 'doesn\'t exist!')
        pass


def get_today_date():
    # return today's date in yyyy-mm-dd format
    today = datetime.datetime.now()
    today_date = '%s-%s-%s' % (today.year, today.month, today.day)
    return today_date


def down_them_all(start_date='2005-01-01', end_date=get_today_date()):
    # literally down them all
    stock_id_list = stock_id_gen()
    start_to_end = year_splitter(start_date, end_date)
    progress = 0
    total = len(stock_id_list)
    for stock_id in stock_id_list:
        download_data(stock_id, start_to_end)
        progress += 1
        print('progress:', str(int(progress * 100 / total)) + '%')
    print('all done! files are in \\data\\ folder')


down_them_all()
