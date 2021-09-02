#_*_ coding:utf-8 _*_

import sys
sys.path.insert(0,'..')
from sql.table import Table
from utils.log import Log
from Queue import Queue
import threading
from traceback import format_exc
import json,time

'''
将table item和book中的url转化为id
'''


def update_item_id():

    table_item = Table_Item(logger=logger)
    results_dict=table_item.check_table_item_url()
    data = results_dict.get('data')
    for result in data:
        url=result.get('url')
        id = url.rsplit('=',1)[-1]
        table_item.update_table_item_id_by_url(id=int(id),url=url)
    table_item.close()


def update_book_id():
    table_book = Table_Book(logger=logger)
    results_dict=table_book.check_table_book_url()
    data = results_dict.get('data')
    for result in data:
        url=result.get('url')
        id = url.rsplit('=',1)[-1]
        table_book.update_table_book_id_by_url(id=int(id),url=url)
        
    table_book.close()


def test():

    log=Log(filename=u'history.log',name='history',mode='a')
    logger = log.Logger
    update_item_id()
    update_book_id()


def generate_queue(logger,table,queue,sql_connect=None):

    if sql_connect is None:
        sql_connect = Table(logger=logger)

    check_func_name = u'check_table_%s_url'%(table)
    check_func = getattr(sql_connect,check_func_name)
    results_dict=check_func()
    data = results_dict.get('data')
    for result in data:
        url=result.get('url')
        id = url.rsplit('=',1)[-1]
        send=dict(id=int(id),url=url,table=table)
        queue.put(dict(id=int(id),url=url,table=table))
        message = u'put %s into queue'%(json.dumps(send))
        logger.info(message)
    sql_connect.close()


def update_id(sql_connect,data):

    id = data.get('id')
    url = data.get('url')
    table = data.get('table')

    update_func_name = u'update_table_%s_id_by_url'%(table)
    update_func = getattr(sql_connect,update_func_name)
    update_func(id=id,url=url)


def main(queue,logger):
    ##此种处理方法可以把任务生成模块和任务处理模块都放入线程中处理，可以处理成方法，便于其他模块调用

    sql_connect = Table(logger=logger)

    ##用以标识多久没接收到任务
    waiting = 0

    while True:
        while not queue.empty():
            try:
                data = queue.get(block=True,timeout=30)
                update_id(sql_connect=sql_connect,data=data)
                waiting =0
            except:
                message=u'update id catch exception:%s'%(format_exc())
                logger.debug(message)

        time.sleep(5)
        waiting +=1
        message =u'in %d seconds no task put in queue'%(5*waiting)
        logger.debug(message)

        if waiting ==60:
            message =u'no task executed in %d seconds,will break loop '%(5*waiting)
            logger.debug(message)
            sql_connect.close()
            break

    
            






if __name__ == '__main__':

    log1 = Log(filename=u'history-multi-thread.log',name='history-multi-thread',mode='a')
    logger1 = log1.Logger

    log2 = Log(filename=u'history-queue.log',name='history-queue',mode='a')
    logger2 = log2.Logger

    tasks=[]

    queue = Queue()

    if 1:
        ##多线程模式不能共用同一个sql_connect，否则会引起（MySQL server has gone away)，原因在于共用一个连接发送数据量过大
        g1 = threading.Thread(target=generate_queue,args=(logger2,'book',queue))
        g2 = threading.Thread(target=generate_queue,args=(logger2,'item',queue))
        tasks = [g1,g2]

    else:
        generate_queue(logger=logger2,table='book',queue=queue)
        generate_queue(logger=logger2,table='item',queue=queue)


    for i in range(4):
        t= threading.Thread(target=main,args=(queue,logger1))
        tasks.append(t)

    for t in tasks:
        t.start()

    for t in tasks:
        t.join()

  

    print u'all threads done!'
