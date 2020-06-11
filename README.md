# phew
A jobs scheduling center

# Service Description
进入sdk目录，查看使用代码

## verndor
业务对接，负责管理业务层的数据流

 - assign		新建任务
 - done			完成的任务
 - delete		移除任务	
 - detail		任务详情
 - read			标记任务已读
 - ping			保持节点状态
 - retry		重试失败或超时的任务
 

## woker
核心功能模块，通过port来定向到不同任务的处理
 - get			获取一个子任务
 - finish		完成一个子任务
 - ping			保持节点状态
  
# Monitor
任务管理器，内置任务监控和统计，以及节点健康状态检测。外部访问请打开防火墙2020端口。
http://127.0.0.1:2020

# How to use
安装redis服务，使用配置文件 redis.conf 启动redis服务

进入src安装requirements.txt

pip install -r requirements.txt -i https://pypi.douban.com/simple/

配置缓存目录
src/app/init.py 中 修改79行

启动服务
python3 jobcenter.py

