
1、python环境 

    python2.7

2、库依赖

    a， bs4          -->pip install bs4

    b， faker        -->pip install faker

    c， MySQLdb      -->pip install MySQL-python
    
    d， pybloom      -->pin install pybloom


3、功能
    
    a, utils/config.py中的各项设置

        DOWNLOAD_FOLDER = 下载目录
        HOST = 数据库连接地址
        PORT = 数据库连接端口
        USER = 数据库连接用户名
        PASSWORD = 数据库连接密码
        PER_REQUEST_DELAY = 请求延迟
        PROXIES = 代理地址

    b, 运行方式，python run.py

    c, 下载可能会有失败的文件，需要删除详见 task/fix.py

    d, 需要将各个章节合并到一起，详见 task/task_combine.py


