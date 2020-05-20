#_*_ coding:utf-8 _*_


import sys
sys.path.append('..')

from task_table import task_table
from task_category import task_category
from task_book import task_book
from task_item import task_item
from task_download import task_download
from sql.table import Table
from utils.log import Log
from Queue import Queue
import threading





def task(t_n=2,d_n=4,is_test=False,is_timer=True,is_category=True,is_book=True,is_item=True,is_download=True):
    '''
    t_n 更新表线程数
    d_n 下载线程数
    '''


    root_log = Log(filename=u'log.log',name='root')
    root_logger = root_log.Logger
    table = Table(logger=root_logger)
    table.create_tables()

    tasks =[]



    ##获取分类信息
    if is_category:

        task_categorys = threading.Thread(target=task_category,name='Thread-task-category',kwargs=dict(logger=root_logger,is_test=is_test))
        tasks.append(task_categorys)

    ##获取各个分类下书籍信息
    if is_book:
        log = Log(filename='book.log',name=u'book')
        book_logger = log.Logger
        task_books = task_book(logger=book_logger,t_n=t_n,is_test=is_test)
        tasks = tasks + task_books

    #获取各本书籍下的章节信息
    if is_item:
        item_log = Log(filename=u'item.log',name='item')
        item_logger = item_log.Logger 
        task_items = task_item(logger=item_logger,t_n=t_n,is_test=is_test)
        tasks = tasks + task_items


    #获取未下载章节信息
    if is_download:
    
        download_log = Log(filename=u'download.log',name='download')
        download_logger = download_log.Logger 
        task_downloads = task_download(logger=download_logger,t_n=d_n)
        tasks = tasks + task_downloads

    ##实时更新table category中book_count,table book中的d_count,total,rate
    if is_timer:
        table_log = Log(filename=u'table.log',name='table')
        table_logger = table_log.Logger
        task_tables =  task_table(logger=table_logger,t_n=d_n,is_test=is_test)
        tasks = tasks + task_tables


    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

    print u'all jobs finished'


def test(is_test = True):
    t_n = 1
    d_n = 2
    task(t_n=t_n,d_n=d_n,is_test=is_test)



if __name__ =='__main__':

    test(True)