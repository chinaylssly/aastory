#_*_ coding:utf-8 _*_

import MySQLdb
import MySQLdb.cursors
from log import Log
from traceback import format_exc
from config import HOST,USER,PASSWORD,PORT,DATABASE


class MySQL(object):
    u'''数据库主类'''

    def __init__(self,host=HOST,user=USER,password=PASSWORD,port=PORT,db=DATABASE,cursorclass=MySQLdb.cursors.DictCursor,charset='utf8',logger=None):
        u'''初始化'''

        self.host=host
        self.user=user
        self.password=password
        self.port=port
        self.db=db
        self.cursorclass=cursorclass
        self.charset=charset

        if logger is None:
            log=Log()
            logger = log.Logger
        self.logger = logger

        try:
            self.connect=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,port=self.port,charset=self.charset,cursorclass=self.cursorclass)
        except:
            ##捕捉数据库database dont exists的异常（连接不到数据库的异常不管）

            message=u'connect to database:%s catch exception：%s'%(self.db,format_exc())
            self.logger.warning(message)

            connect=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db='',port=self.port,charset=self.charset,cursorclass=self.cursorclass)
            cursor=connect.cursor()
            query='create database if not exists %s'%self.db
            cursor.execute(query)
            connect.commit()
            connect.close()

            message=u'create database:%s'%(self.db)
            self.logger.debug(message)

        self.connect=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db,port=self.port,charset=self.charset,cursorclass=self.cursorclass)
        self.cursor = self.connect.cursor()

        message=u'connect to %s.%s,current db is:%s'%(host,user,db)
        self.logger.info(message)


    def execute(self,query):

        try:
            count=self.cursor.execute(query)
            data=self.cursor.fetchall()
            self.connect.commit()
            message=u'run command:"%s",fetchall count is：%s'%(query,count)
            self.logger.info(message)

            return dict(count=count,data=data)

        except:
            message=u'run command:"%s",catch exception：%s'%(query,format_exc())
            self.logger.error(message)
            # assert 0,message
            return None


    def close(self,):

        message=u'close connect to host=%s as user=%s'%(self.host,self.user)
        self.logger.info(message)
        self.connect.close()

    def truncate_table(self,tb):
        #清空表

        query='truncate table %s'%(tb)
        self.execute(query=query)

    def drop_table(self,tb):
        #删除表
        
        query='drop table %s'%(tb)
        self.execute(query=query)



def test():
    DATABASE='wert'
    mysql=MySQL(db=DATABASE)
    # sql='create database if not exists %s'%(DATABASE)
    # mysql.execute(query=sql)

    
if __name__ == '__main__':
    test()


