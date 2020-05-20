#_*_ coding:utf-8 _*_

import sys
sys.path.append('..')

from item import Item
from task_tool import Task_Tool
import json
from sql.table import Table
from utils.log import Log
from utils.tools import putty

'''
章节信息抓取模块
'''



def core_execute_item(item,book,category,book_id,logger,table,is_test=False):
    ##
    '''
    params: item ->class Item的实例
    params: table ->class Table 的实例
    params: is_test ->控制是否测试环境
    章节内容抓取核心函数
    '''
    is_finish = item.get_xingzhi()
    item_data = item.get_item()
    for each in item_data:
        item_url = each.get('url')
        id = each.get('id')
        title = each.get('title')

        item_name = putty(title)

        if is_test:
            message = json.dumps(dict(id=id,url=item_url,item=item_name,book=book,category=category,book_id=book_id,is_finish=is_finish),ensure_ascii=False)
            logger.debug(message)
        else:
            table.insert_table_item(id=id,url=item_url,item=item_name,book=book,category=category,book_id=book_id,is_finish=is_finish)
            table.update_table_book_is_finish(id=book_id,is_finish=is_finish)



def execute_item(table,queue,logger,is_test=False):
    '''
    params: table -> class Table的实例
    params: queue -> book task queue
    params: logger -> Log().Logger
    章节抓取函数
    '''

 
    data = queue.get(block=True,timeout=30)
    category = data.get('category')
    book_url = data.get('url')
    book_id = data.get('id')
    book = data.get('book')

    item = Item(url=book_url,logger=logger)
    core_execute_item(item=item,book=book,category=category,book_id=book_id,logger=logger,table=table,is_test=is_test)





def task_item(logger,t_n=4,g_sleep=180,g_times=20,e_sleep=10,e_times=30,is_filter=True,is_test=False):
    ##多线程任务函数
    
    task_tool =Task_Tool(logger=logger,is_filter=is_filter)
    generate_func_name = u'check_table_book'
    g_kw = {}
    e_kw = dict(queue=task_tool.queue,logger=logger,is_test=is_test)

    tasks = task_tool.thread_tasks(generate_func_name=generate_func_name,execute_func=execute_item,g_kw=g_kw,e_kw=e_kw,
                                    t_n=t_n,g_sleep=g_sleep,g_times=g_times,e_sleep=e_sleep,e_times=e_times)
    return tasks




def test_task_item(is_test=True):

    log = Log(filename='item.log',name=u'item')
    logger = log.Logger
    tasks = task_item(logger=logger,is_test=is_test)
    for t in tasks:
        t.start()
    for t in tasks:
        t.join()

if __name__ == '__main__':


    test_task_item()



