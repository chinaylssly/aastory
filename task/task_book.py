#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from book import Book
from task_tool import Task_Tool
from sql.table import Table
from utils.log import Log
from utils.tools import putty
import json


'''
书本信息抓取模块
'''





def core_execute_book(book,category,logger,table,is_test=False):
    ##获取分类下某一页的book信息，以及下一页url,is_test控制是否是测试环境
    '''
    params: book ->class Book的实例
    params: table ->class Table 的实例
    params: is_test ->控制是否测试环境
    书籍信息抓取的核心函数
    '''

    book_data = book.get_link()
    for each in book_data:
        book_url = each.get('url')
        id = each.get('id')
        title = each.get('title')
        book_name = putty(title)

        if is_test:
            message = json.dumps(dict(id=id,url=book_url,book=book_name,category=category),ensure_ascii=False)
            logger.debug(message)
        else:
            table.insert_table_book(id=id,url=book_url,book=book_name,category=category)

    next_url = book.get_next()
    return next_url


def execute_book(table,queue,logger,is_test=False):
    '''
    params: table -> class Table的实例
    params: queue -> book task queue
    params: logger -> Log().Logger
    书本信息抓取
    '''

 
    data = queue.get(block=True,timeout=30)
    category = data.get('category')
    category_url = data.get('url')

    book = Book(url=category_url,logger=logger)
    next_url = core_execute_book(book=book,category=category,logger=logger,table=table,is_test=is_test)
    while next_url:
        ##处理下一页
        book = Book(url=next_url,logger=logger)
        next_url =core_execute_book(book=book,category=category,logger=logger,table=table,is_test=is_test)





    

def task_book(logger,t_n=4,g_sleep=180,g_times=20,e_sleep=10,e_times=30,is_filter=True,is_test=False):
    ##多线程任务函数
    
    task_tool =Task_Tool(logger=logger,is_filter=is_filter)
    generate_func_name = u'check_table_category'
    g_kw = {}
    e_kw = dict(queue=task_tool.queue,logger=logger,is_test=is_test)

    tasks = task_tool.thread_tasks(generate_func_name=generate_func_name,execute_func=execute_book,g_kw=g_kw,e_kw=e_kw,
                                    t_n=t_n,g_sleep=g_sleep,g_times=g_times,e_sleep=e_sleep,e_times=e_times)
    return tasks




def test_task_book(is_test=True):

    log = Log(filename='book.log',name=u'book')
    logger = log.Logger
    tasks = task_book(logger=logger,is_test=is_test)
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()

if __name__ == '__main__':


    test_task_book()









