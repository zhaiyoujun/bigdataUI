## 1 LLTS简介

Low Latency Task Service简称LLTS，目标是为一组相近的计算需求，提供低延迟的计算任务执行服务。

### 1.1 架构

LLTS包含两种角色：Controller和Agent。Controller负责接收外部程序发来的请求，Agent负责启动和监视具体的计算任务。Agent都是同构的计算单元，每个Agent只能同时容纳一个计算任务。

![LLTS架构](http://upload-images.jianshu.io/upload_images/1752522-eba47d63a181d4e0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 1.2 典型流程

一次典型计算流程如下图（在运行非分布式程序时，不包含启动子任务的部分）：

![计算流程](http://upload-images.jianshu.io/upload_images/1752522-8b5ecd933ab62fa2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 2 LLTS交互说明

LLTS与其他程序之间交互的消息总是一个平铺的JSON对象序列化的结果。LLTS会创建一个ZMQ REP Socket用于接收发来的消息，在收到消息后总是立刻回复。

外部程序向LLTS发送消息的例子：
a）通过ZMQ.context创建一个Context
b）通过context创建一个REQ Socket
c）使用REQ Socket的connect方法连接LLTS
d）通过REQ Socket的send方法发送任务提交请求
e）通过REQ Socket的recv方法接收LLTS发来的响应

Example：

```
ZMQ.Context context = ZMQ.context(1);  
ZMQ.Socket s = context.socket(ZMQ.REQ); 
s.connect(address); 
s.send(message.getBytes(), 0);  
String rev = new String(s.recv(0));  
```

注：连接后，可以反复send和recv，以发送多条消息。

### 2.1 任务提交接口

用于向LLTS提交任务

1）发送的消息

|字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_ | TASK/SUBMIT | 表示提交任务 |
|\_\_OPERATION\_\_ | | 要运行工具程序 （会找到${\_\_OPERATION\_\_}.tar.gz作为任务要执行的内容）|
|\_\_ADDRESS\_\_|  |任务发送方接收任务运行状态的ZMQ DEALER Socket地址|
|\_\_GIVEN_ID\_\_|  | 任务发送方可以自己为任务指定ID，可以根据该ID来查询任务。|
|\_\_FATHER_ID\_\_ |   | 指定新任务的父任务，父任务在结束时，LLTS会自动将其所有子任务停止掉。|
|…  |   |  任务执行时可以访问到的其他参数 |

如果请求中有\_\_ADDRESS\_\_字段，那么LLTS会在任务的状态发生改变时，主动向\_\_ADDRESS\_\_字段所包含的地址发送任务状态。发送时会通过一个ZMQ DEALER Socket连接\_\_ADDRESS\_\_字段包含的地址，然后通过send方法发送任务状态信息。任务发起方为了接受这个信息，可以：

a）通过ZMQ.context创建一个context
b）通过context创建一个socket
c）使用socket的bind方法绑定\_\_ADDRESS\_\_
d）通过socket的revc方法接收LLTS发送来的状态

Example：

```
ZMQ.Context context = ZMQ.context(1);
ZMQ.Socket s = context.socket(ZMQ.DEALER); 
s.bind(__ADDRESS__); 
String rev = new String(s.recv(0));
```

2）响应的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TASK\_ID\_\_|    |  分配给任务的ID |
|\_\_CODE\_\_|   |0表示消息包含的请求已被接受，非0表示被拒绝|

### 2.2 任务终止接口

用于主动杀死指定任务。

1）发送的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_ |  TASK/KILL  | 终止任务 |
|\_\_TASK\_ID\_\_|    |要终止的任务ID。注意：不是\_\_GIVEN\_ID\_|

2）响应的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_CODE\_\_|  |0表示请求被接受，非0表示被拒绝|

### 2.3 任务状态查询接口

用于主动查询指定任务的状态。

1）发送的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_| TASK/QUERY | 查询任务状态 |
|\_\_TASK\_ID\_\_|   | 用提交任务后返回的\_\_TASK\_ID\_\_来查询任务状态|
|\_\_GIVEN\_ID\_\_|    |也可用任务发送方自己指定的任务ID来查询任务状态|
|…|    |     其他字段 |

查询时可提供多个字段，只有所有字段都匹配才会返回任务信息。

2）响应的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_STATUS\_\_|   |‘WAITING’表示在任务排队中，‘RUNNING’表示运行中，’ENDED’表示正在清理，’FINISHED’表示已结束|
|\_\_CODE\_\_|   |0表示任务存在，非0表示查询被拒绝|
|\_\_EXIT\_CODE\_\_|   | 任务运行结束的退出码，当\_\_STATUS\_\_为’FINISHED’会附上这个字段|
|\_\_REPORT\_LOG\_\_|   |任务产生的报告信息report.log最后10K内容，当\_\_STATUS\_\_为’FINISHED’会附上这个字段|
|… |   |  其他字段 |

其他跟任务相关的信息

### 2.4 Agent统计信息接口

用于获取Agent统计信息。

1）发送的消息


|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|  AGENT/QUERY  | 获取Agent统计信息|

2）响应的消息


|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_CODE\_\_|   |0 表示请求被接收，非0表示请求被拒绝| 
|\_\_TOTAL\_\_|  |Agent总数|
|\_\_FREE\_\_|  |空闲Agent数量|
|\_\_BUSY\_\_| |繁忙Agent数量|
|\_\_LOST\_\_|  |丢失Agent数量（超过两个心跳间隔未收到心跳，则认为Agent丢失）|


### 2.5 Task统计信息接口

用于获取task统计信息。

1）发送的消息


|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|  TASK/STATISTIC  | 获取task统计信息|

2）响应的消息


|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_CODE\_\_|   |0 表示请求被接收，非0表示请求被拒绝| 
|DISPATCHED|  |Controller已响应的task数量|
|WAITING|  |等待的task数量|
|PREPARING| |准备中的task数量|
|RUNNING|  |正在执行的task数量|
|ENDED| |执行完毕的task数量|
|FINISHED|  |清理完毕的task数量|

### 2.6 Task详细信息接口

用于获取task详细信息。

1）发送的消息

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|  TASK/DETAILS  | 获取task详细信息|

2）响应的消息

key-value形式。key为具体的\_\_TASK\_ID\_\_,value为该task的详细信息。有多少个task就返回多少个这样的key-value对。

### 2.7 \_\_CODE\_\_和\_\_EXIT\_CODE\_\_字段

当\_\_CODE\_\_为0时，为正常响应，否则为异常响应。具体如下：

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| 0 | 正常|
|\_\_CODE\_\_| -1001 | 不是JSON格式 |
|\_\_CODE\_\_| -1002 | 缺少\_\_TYPE\_\_字段|
|\_\_CODE\_\_| -1003 | \_\_TYPE\_\_字段未知|
|\_\_CODE\_\_| -1004 | 无效的\_\_TASK\_ID\_\_|
|\_\_CODE\_\_| -1005 | 缺少\_\_AGENT\_ID\_\_字段|
|\_\_CODE\_\_| -1010 | 没有task可以分配|

\_\_EXIT\_CODE\_\_字段描述LLTS-Tool 准备和执行过程中的状态。具体如下：

|字段名 | 值  | 说明 |
|:---:|---|---|
|\_\_EXIT\_CODE\_\_| -128  |准备过程中被杀死|
|\_\_EXIT\_CODE\_\_| -129  |*.tar.gz不存在|
|\_\_EXIT\_CODE\_\_| -130  |*.tar.gz解压失败|
|\_\_EXIT\_CODE\_\_| -131  |准备过程中的其他异常|
|\_\_EXIT\_CODE\_\_| 其他  |执行run.sh的退出码|

## 3 LLTS-Tool规范说明

### 3.1 基本情况

LLTS-Tool是一个能够被LLTS框架运行的tar.gz格式的压缩包，该压缩包需要放在config.py中配置的AGENT_TOOLS_DIR目录下。一个LLTS-Tool中必须包含一个run.sh脚本作为LLTS-Tool启动的入口。

以helloworld工具程序为例：

1）部署时

```
AGENT_TOOLS_DIR
└── helloworld.tar.gz
```

2）解压后

```
helloworld
├── other_files
└── run.sh
```

当框架收到启动任务的请求之后，会根据请求的\_\_OPERATION\_\_参数查找到相应的LLTS-Tool，并将LLTS-Tool解压到分配的计算单元所准备的运行环境中，然后执行解压出来的run.sh脚本。run.sh脚本中可以执行任何命令，比如启动包含业务逻辑的具体的程序。

任何任务中的进程，也可以向LLTS提交新的任务。

以瓦片切割为例：

用户可以实现两个LLTS-Tool：dispatcher和worker，dispatcher在启动后可以向LLTS发送多个启动worker的请求，各个worker启动后，再通过网络与dispatcher建立联系（可以使用ZMQ），然后由dispatcher和所有worker协作，并行得完成瓦片切割的任务。

dispatcher和worker也可以不作为两个LLTS-Tool存在，而是作为一个LLTS-Tool中的两种启动模式存在（实际以哪种模式启动可以由参数决定）

### 3.2 LLTS-Tool的启动

为任务准备的目录中，会包含task.info和controller.info以及以LLTS-Tool名称命名的子目录，子目录下会有LLTS-Tool解压出来的所有内容（如run.sh），任务运行时的工作目录，也会在此子目录下，即run.sh中可以通过相对路径../task.info和../Controller.info找到这两个LLTS为任务准备的文件，同时可以在当前目录下输出report.log

task.info文件中保存了LLTS框架收到的启动任务的请求中的所有的参数（每行一个参数，每行的格式总是key=value得形式），以及当前任务的ID。比如提交任务的请求为：

```
{
	‘__TYPE__’: ‘TASK/SUBMIT’,
	‘__OPERATION__’: ‘test’,
	‘param1’: ‘value1’,
	‘param2’: ‘value2’
}
```
那么task.info中的信息则会是：

```
__TYPE__=TASK/SUBMIT
__OPERATION__=test
param1=value1
param2=value2
__TASK_ID__=TASK_*_#  (‘*’为任务提交时间,'#'为长度为5的随机字符串)
```

controller.info文件中保存了LLTS框架的地址、运行该任务的Agent的IP。比如：

```
CONTROLLER_ADDRESS=tcp://192.168.1.100:11000
AGENT_IP=192.168.1.100
```

LLTS-Tool可以通过CONTROLLER_ADDRESS表示的ZMQ REQ Socket地址向LLTS发送各种请求。

### 3.3 LLTS-Tool运行过程中产生的数据 

LLTS不关心业务逻辑相关的任何问题，因此进度、结果之类的信息的收集、转发、报告，最好 LLTS-Tool自己解决。

同时LLTS为LLTS-Tool提供了一种通用的数据收集方式，即LLTS-Tool在运行过程中可以将信息追加到与run.sh同级的report.log文件中。当任务执行完成后，LLTS会从report.log文件中读取最后10K字节的数据，传递给任务发送方。

以瓦片切割为例，worker每次向dispatcher申请一个瓦片的输出任务，并在完成后向dispatcher报告，这样dispatcher就可以在任何时刻知道当前有多少个瓦片已经输出完成，又有多少瓦片正在输出中。于是dispatcher就可以在输出进度到达整10百分比的时候直接写数据库，或通过ZMQ向某个地址发送当前的进度。
当运行出现错误时，可以将错误信息写到report.log中，最终通过LLTS将错误信息传递到任务发送方，方便任务发送方追查错误原因。

### 3.4 运行中的LLTS-Tool

在运行过程中LLTS-Tool被解压，并被调用文件夹中的run.sh。以helloworld为例，说明运行中的LLTS-Tool具体形态。

``` 
LLTS                                                          --LLTS 源码目录
├─ controller.py                                              --Controller主程序
├─ agent.py                                                   --Agent主程序
├─ config.py                                                  --配置文件
├─ const.py                                                   --常量定义文件       
├─ *.py                                                       --Controller和Agent调用的其他程序       
├─ controller.log                                             --Controller的日志文件          
├─ agent.log                                                  --Agent的日志文件
├─ startup-singleton.sh                                       --LLTS启动脚本
├─ shutdown-singleton.sh                                      --LLTS关闭脚本
└─ agentWorkDir                                               --Agent工作目录
     └─ TASK_*                                                --Task 的工作目录
           ├─ controller.info                                 --Agent为LLTS-Tool准备的文件
           ├─ task.info                                       --Agent为LLTS-Tool准备的文件
           └─ helloworld                                      --helloworld.tar.gz解压后产生的同名文件夹
                 ├─ run.sh                                    --LLTS-Tool的启动脚本
                 ├─ report.log                                --LLTS-Tool在运行过程中产生日志类数据             
                 └─ other_files                               --run.sh在运行过程需要的其他文件或文件夹
```

## 4 LLTS使用说明

### 4.1 启动LLTS

运行startup-singleton.sh可以启动整个LLTS，包括Controller和30个Agent（默认），如果需要自己指定Agent的个数为x，只要把x作为startup-singleton.sh的第一个参数即可。

### 4.2 关闭LLTS

运行shutdown-singleton.sh可以关闭整个LLTS。

### 4.3 配置

config.py 是LLTS的配置文件。包含以下配置项：

```
CONTROLLER_REP_PORT = 15555         #Controller的ZMQ.REP端口
CONTROLLER_PUB_PORT = 15556		    #Controller的ZMQ.PUB端口
ZMQ_RECV_TIMEOUT = 3000		        #ZMQ消息超时时间
AGENT_HEARTBEAT_INTERVAL = 3000     #Agent的心跳间隔
CONTROLLER_IP = "127.0.0.1"         #Controller的IP地址
AGENT_WORK_DIR = 'work'			    #Agent的工作目录
AGENT_KILL_INTERVAL = 3000          #Agent杀死任务的间隔
AGENT_KILL_COUNT = 3		        #Agent杀死任务的最大尝试次数
REPORT_LOG_KEEP_BYTES = 10000       #保留的report.log内容的长度，单位：byte
LOG_FORMATTER = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s'   #日志格式
CONTROLLER_LOG_FILE = 'controller.log'    #Controller日志文件名
AGENT_LOG_FILE = 'agent.log'		#Agent日志文件名
AGENT_TOOLS_DIR = 'testTools'	    #LLTS-Tools存放的目录
TASK_KEEP_HOURS = 24		    	#已结束的任务保留的时间，单位：小时
```

注意：向Controller提交任务前请确保已经将需要执行的LLTS-Tool放到AGENT_TOOLS_DIR目录下。
