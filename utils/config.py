#_*_ coding:utf-8 _*_
import os 


##代理配置
PROXIES = {'http':'127.0.0.1:1080','https':'127.0.0.1:1080',}

##文件下载总目录
DOWNLOAD_FOLDER=u'f:/data/aabook'

#config文件所在绝对目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

#日志文件目录
LOG_FOLDER = u'%s/log'%(os.path.dirname(CURRENT_DIR))

LOG_TO_CONSOLE = True
LOG_TO_FILE = True
FORMATTER = u'%(asctime)s-[processid]:%(process)d-[threadid]:%(thread)d-[threadname]:%(threadName)s-[loggername]:%(name)s-[filename]:%(filename)s-[line]:%(lineno)d-%(levelname)s-[message]：%(message)s'
MODE='w'
##请求延迟秒数
PER_REQUESTS_DELAY = 0.1

##下载延迟秒数
PER_DOWNLOAD_DELAY = 2

##连接数据库相关配置
HOST = u'localhost'
USER = u'root'
PASSWORD = ''
PORT = 3306
##需要事先创建数据库
DATABASE = u'aabook'

#网站域名（可能会更换）
WEBHOSTS = ['aastory.club','aabook.xyz','aavbook.fun','aabook.men']

#更换域名
IS_CHANGE_HOST = True
HOST_INDEX = 2


