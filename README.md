# phew
A jobs scheduling center

# Service Description
## verndor
业务对接，负责管理业务层的数据流

## jobcenter
任务管理器，内置任务监控和统计，以及节点健康状态检测
 - state/counter				任务统计数据

 - job/assign		新建任务
 - job/finished		完成的任务
 - job/remove		移除任务	
 - job/detail		任务详情

 - task/get	获取一个子任务
 - task/finish	完成一个子任务
 - task/ping	保持节点状态
 
## woker
核心功能模块，通过port来定向到不同任务的处理
