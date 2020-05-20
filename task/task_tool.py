#_*_ coding:utf-8 _*_
import sys
sys.path.insert(0,'..')

import time,json
from traceback import format_exc
from pybloom import ScalableBloomFilter
from Queue import Queue
from threading import Thread
from sql.table import Table


'''
task任务的核心函数
'''

class Task_Tool(object):

    def __init__(self,logger,is_filter=True):
        '''
        params: is_filter ->是否对任务生成函数启用ScalableBloomFilter
        '''

        self.queue = Queue()
        self.logger = logger
        self.is_filter = is_filter

 


    def loop_task(self,execute_func,e_kw={},flag=1,sleep=10,times=30):
        '''
        params: execute_func ->execute function
        params: e_kw ->keyword params of execute_func
        params: flag ->flag=1,loop_task is generate_task,otherwise loop_task is execute_task
        params: sleep,times->每次轮询的休息的时间，和轮询的次数
        用于多线程处理任务,flag=1时，为任务生成函数；flag=0时，为任务处理函数


        '''
        execute_func_name = execute_func.__name__

        ##用以标识多久没接收到任务
        waiting = 0

        while True:

            if flag:
                condition = self.queue.empty()
            else:
                condition = not self.queue.empty()

            while condition:
                try:
                    execute_func(**e_kw)
                    waiting = 0
                except:
                    message=u'catch exception:%s'%(format_exc())
                    self.logger.debug(message)
                    

                if flag:
                    condition = self.queue.empty()
                else:
                    condition = not self.queue.empty()

            time.sleep(sleep)
            waiting +=1
            if flag:
                message = u'by function:%s, no task put in queue in %d seconds'%(execute_func_name,sleep*waiting)
            else:
                message = u'function:%s cant get task from queue in %d seconds'%(execute_func_name,sleep*waiting)
            self.logger.debug(message)

            if waiting ==times:
                if flag:
                    message = u'no task generate by function:%s in %d seconds,will break loop'%(execute_func_name,sleep*waiting)
                else:
                    message = u'no task for function:%s to execute in %d seconds,will break loop'%(execute_func_name,sleep*waiting)
                self.logger.debug(message)

                break



    def core_generate_task(self,generate_func,g_kw={}):
        '''
        params: generate_func -> task generate function
        params: g_kw-> keyword params of generate_func

        装载有bloom过滤器的任务生成核心函数
        '''

        result_dict = generate_func(**g_kw)
        data = result_dict.get('data')


        count = 0
        for each in data:
            
            if self.is_filter:
                ##开启过滤器
                is_exists = self.sbf.add(each)
            else:
                is_exists = False

            if is_exists:
                message = u'data :%s already sended to queue once'%(json.dumps(each,ensure_ascii=False))
                self.logger.debug(message)
            else:
                self.queue.put(each)
                message = u'put %s into queue'%(json.dumps(each,ensure_ascii=False))
                self.logger.info(message)
                count +=1

        if count == 0:
            message = u'all data already in bloomfilter or no data generate by function:%s !'%(generate_func.__name__)
            self.logger.debug(message)
            raise Exception,message


    def generate_task(self,generate_func_name,g_kw={},sleep=180,times=20,):
        '''
        params: generate_func_name -> 任务生成函数的名字
        params: g_kw -> generate_func的关键字参数
        params: sleep,times ->每过sleep秒执行一次generate_func，times为执行的次数

        任务生成函数，可多次执行generate_func,无需多次将times设置为1即可
        '''
        if self.is_filter:
            self.sbf = ScalableBloomFilter()
        else:
            self.sbf =None

     
        table = Table(logger=self.logger)
        generate_func =getattr(table,generate_func_name)
        e_kw=dict(generate_func=generate_func,g_kw=g_kw,)

        self.loop_task(execute_func=self.core_generate_task,e_kw=e_kw,flag=1,sleep=sleep,times=times)
        table.close()


    def execute_task(self,execute_func,e_kw,sbf=None,sleep=10,times=30):
        '''
        params: execute_func -->任务处理函数
        params: e_kw  -->execute_func 的keyword参数
        params: sbf  -->对任务处理结果进行过滤
        '''

        table =  Table(logger=self.logger)
        e_kw = dict(e_kw,table=table)

        self.loop_task(execute_func=execute_func,e_kw=e_kw,flag=0,sleep=sleep,times=times)
        table.close()


    def add_sbf(self,query=None):
        '''
        params: query -->mysql 查询语句
        过滤任务处理结果
        '''

        if query is None:
            return None

        sbf = ScalableBloomFilter()
        table = Table(logger=self.logger)
        result_dict = table.execute(query=query)
        data = result_dict.get('data')
        for each in data:
            id = each.get('id')
            sbf.add(int(id))
        table.close()
        return sbf


    def thread_tasks(self,generate_func_name,execute_func,g_kw={},e_kw={},t_n=2,query=None,g_sleep=180,g_times=20,e_sleep=10,e_times=36):

        tasks= [Thread(target=self.generate_task,name='Thread-generate',kwargs=dict(generate_func_name=generate_func_name,g_kw=g_kw,
                                                                                    sleep=g_sleep,times=g_times))]

        
        sbf = self.add_sbf(query=query)
        if sbf is not None:
            e_kw = dict(e_kw,sbf=sbf) 
   

        for i in range(t_n):
            t = Thread(target=self.execute_task,name='Thread-execute-%d'%(i+1),kwargs=dict(execute_func=execute_func,e_kw=e_kw,
                                                                                            sleep=e_sleep,times=e_times)) 
            tasks.append(t)

        return tasks



