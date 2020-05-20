#_*_ coding:utf-8 _*_

from table_category import Table_Category
from table_book import Table_Book
from table_item import Table_Item

'''
继承所有SQL的方法

'''

class Table(Table_Category,Table_Book,Table_Item):

    def __init__(self,logger=None):
        super(Table,self).__init__(logger=logger)

    def create_tables(self,):
        ##创建表
        
        self.create_table_category()
        self.create_table_item()
        self.create_table_book()
        self.close()

    def drop_primary_key(self,table):
        #删除主键
        query = u'alter table %s drop primary key'%(table)
        self.execute(query=query)

    def add_primary_key(self,table,pk):
        #添加主键
        query = u'alter table %s add primary key(%s)'%(table,pk)
        self.execute(query=query)
