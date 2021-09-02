#_*_ coding:utf-8 _*_
import sys
sys.path.append('..')

from sql.table import Table
from utils.log import Log
from task_tool import Task_Tool

'''
更新category中的book_count，book表中d_count,total,rate
'''



def update_category(logger,is_test=False):

    ##更新table category 的book_count
    table = Table(logger=logger)
    book_count_result = table.count_table_book_count_by_category()
    book_count_data = book_count_result.get('data')
    for each in book_count_data:
        book_count = each.get('book_count')
        category = each.get('category')
        if is_test:
            message = u'table category set book_count =%s where category = %s'%(book_count,category)
            table.logger.debug(message)
        else:
            table.update_table_category_book_count(book_count=book_count,category=category)
    table.close()


def execute_update_book(table,queue,logger,is_test=False):


    data = queue.get(block=True,timeout=30)
    book_id = data.get('id')
    d_count = table.count_table_item_total_by_book_id(book_id=book_id,is_download=1)
    total = table.count_table_item_total_by_book_id(book_id=book_id,is_download=-1)
    if total:
        rate = int(d_count*100.0 / total)
    else:
        rate = 0

    if is_test:
        message=u'table book set d_count=%d,total=%d,rate=%d where book_id=%d'%(d_count,total,rate,book_id)
        logger.debug(message)
    else:
        table.update_table_book_status(d_count,total,rate,book_id)



def task_table_book(logger,t_n=4,g_sleep=0,g_times=1,e_sleep=10,e_times=30,is_filter=True,is_test=False):

    
    task_tool =Task_Tool(logger=logger,is_filter=is_filter)
    generate_func_name = u'check_table_book_for_timer'
    g_kw = dict()
    e_kw = dict(queue=task_tool.queue,logger=logger,is_test=is_test)

    tasks = task_tool.thread_tasks(generate_func_name=generate_func_name,execute_func=execute_update_book,g_kw=g_kw,e_kw=e_kw,
                                    t_n=t_n,g_sleep=g_sleep,g_times=g_times,e_sleep=e_sleep,e_times=e_times)
    return tasks



def task_table(logger,t_n=4,g_sleep=0,g_times=1,e_sleep=10,e_times=30,is_filter=True,is_test=False):

    update_category(logger=logger,is_test=is_test)
    tasks = task_table_book(logger=logger,t_n=t_n,g_sleep=g_sleep,g_times=g_times,
                                e_sleep=e_sleep,e_times=e_times,is_filter=is_filter,is_test=is_test)


    return tasks



def test_task_table(t_n=5,is_test=True):

    logger = Log(filename=u'update.log',name=u'update').Logger
    tasks =task_table(logger,t_n=t_n,is_test=is_test)
    print tasks

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()


    print u'all jobs done'







if __name__ == '__main__':

    test_task_table(t_n=30,is_test=False)
    pass




