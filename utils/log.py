#_*_ coding:utf-8 _*_

import logging
import os
from config import LOG_FOLDER,LOG_TO_CONSOLE,LOG_TO_FILE,FORMATTER,MODE

'''
logging模块为单例模型
对logging模块的封装 
代码参考来源：https://www.jb51.net/article/161828.htm
'''


class Log(object):
    '''
    logging的封装
    '''

    def __init__(self,log_folder=LOG_FOLDER,filename='log.log',name=__name__,level='DEBUG',mode=MODE,log_to_console=LOG_TO_CONSOLE,log_to_file=LOG_TO_FILE):

        self.__name = name
        self.__level = level
        self.__mode = MODE
        self.__log_folder = LOG_FOLDER

        ##创建日志文件夹，最好在config文件中创建
        if not os.path.exists(self.__log_folder):
            os.makedirs(self.__log_folder)

        self.__filename = filename
        self.__filepath = u'%s/%s'%(self.__log_folder,self.__filename)

        self.__log_to_console = LOG_TO_CONSOLE
        self.__log_to_file = LOG_TO_FILE

        ##同一个name返回同一个logger对象，不指定则默认为root
        self.__logger = logging.getLogger(self.__name)
        self.__logger.setLevel(self.__level)


    def __init_handler(self,):
        '''
        初始化handler
        '''
        
        # StreamHandler()函数默认输出为sys.stdout
        stream_handler = logging.StreamHandler()

        file_handler = logging.FileHandler(self.__filepath,mode=self.__mode,encoding='utf8')
        return stream_handler,file_handler

    def __set_handler(self,stream_handler,file_handler,level='DEBUG'):
        '''
        设置handler级别并添加到logger收集器中
        '''

        stream_handler.setLevel(level)
        file_handler.setLevel(level)
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def __set_formatter(self,stream_handler,file_handler,):
        '''
        设置日志输出格式
        '''
        formatter=logging.Formatter(u'%(asctime)s-[processid]:%(process)d-[threadid]:%(thread)d-[threadname]:%(threadName)s-%(name)s-%(filename)s-[line]:%(lineno)d-%(levelname)s-[message]：%(message)s',
                                    # datefmt=u'%a, %d %b %Y %H:%M:%S'
                                    )

        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

    def __closehandler(self,stream_handler,file_handler):
        '''
        关闭handler
        '''

        stream_handler.close()
        file_handler.close()

    @property
    def Loggers(self,):
        '''
        构造收集器，返回logger
        '''

        stream_handler,file_handler = self. __init_handler()
        self.__set_handler(stream_handler,file_handler)
        self.__set_formatter(stream_handler,file_handler)
        self.__closehandler(stream_handler,file_handler)

        return self.__logger

    @property
    def Logger(self,):
        '''
        更灵活的logger收集器
        '''

        formatter = logging.Formatter(FORMATTER)
        if self.__log_to_console:

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(self.__level)
            stream_handler.setFormatter(formatter)
            stream_handler.close()
            self.__logger.addHandler(stream_handler)

        if self.__log_to_file:

            file_handler = logging.FileHandler(self.__filepath,mode=MODE,encoding='utf-8')
            file_handler.setLevel(self.__level)
            file_handler.setFormatter(formatter)
            file_handler.close()
            self.__logger.addHandler(file_handler)

        return self.__logger




def test():
    log=Log()
    logger=log.Logger
    logger.debug(u'I am a debug message')
    logger.info(u'I am a info message')
    logger.warning(u'I am a warning message')
    logger.error(u'I am a error message')
    logger.critical(u'I am a critical message')



if __name__ =='__main__':

    test()










