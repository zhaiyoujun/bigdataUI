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

Eg：

```
 ZMQ.Context context = ZMQ.context(1);  
 ZMQ.Socket s = context.socket(ZMQ.REQ); 
 s.connect(address); 
 s.send(message.getBytes(), 0);  
 String rev = new String(s.recv(0));  
```

注：连接后，可以反复send和recv，以发送多条消息。
 
LLTS内部之间以及与外部交互的发起方发送的消息都必须包含’\_\_TYPE\_\_’字段，通过’\_\_TYPE\_\_’字段来说明消息的类型。
 
具体的消息类型包括：
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/SUBMIT|提交任务|
|\_\_TYPE\_\_|TASK/KILL|杀死任务|
|\_\_TYPE\_\_|TASK/QUERY|任务状态查询|
|\_\_TYPE\_\_|AGENT/QUERY|Agent信息查询|
|\_\_TYPE\_\_|AGENT/HEARTBEAT|Agent心跳汇报|
|\_\_TYPE\_\_|AGENT/EXIT|Agent退出汇报|
|\_\_TYPE\_\_|TASK/INTERNAL/REPORT|任务状态信息汇报|
|\_\_TYPE\_\_|TASK/INTERNAL/APPLY|任务申请|
|\_\_TYPE\_\_|TASK/INFORM|新任务通知|
|\_\_TYPE\_\_|AGENT/STOP|停止Agent通知|

## 3 LLTS内部设计说明

LLTS包括Controller和Agent两部分。

### 3.1 Controller

Controller通过ZMQ与外部进行通信。主要涉及到三类接口，ZMQ REP接口、ZMQ PUB接口以及ZMQ DEALER接口。ZMQ REP接口用来接收其他组件的ZMQ REQ信息；ZMQ PUB接收用来向Agent发布信息；ZMQ DEALER接口用来向任务发起方发送任务状态。

#### 3.1.1 ZMQ REP接口

对于Controller的ZMQ REP接口，所有的响应消息都包含一个\_\_CODE\_\_字段，当\_\_CODE\_\_为0时，为正常响应，否则为异常响应。
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_|0|正常
|\_\_CODE\_\_|-1001|JSON解析失败
|\_\_CODE\_\_|-1002|缺少\_\_TYPE\_\_字段
|\_\_CODE\_\_|-1003|\_\_TYPE\_\_字段未知
|\_\_CODE\_\_|-1004|无效的\_\_TASK_ID\_\_
|\_\_CODE\_\_|-1005|缺少\_\_AGENT_ID\_\_字段
|\_\_CODE\_\_|-1010|没有task可以分配
 
\_\_EXIT_CODE\_\_字段描述LLTS-Tool 准备和执行过程中的状态。
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_EXIT_CODE\_\_|-129|*.tar.gz不存在
|\_\_EXIT_CODE\_\_|-130|*.tar.gz解压失败
|\_\_EXIT_CODE\_\_|-131|准备过程中的其他异常
|\_\_EXIT_CODE\_\_|-128|准备过程中被杀死
|\_\_EXIT_CODE\_\_|其他|执行run.sh的退出码
 
##### 3.1.1.1 任务提交接口

1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/SUBMIT|表示提交任务
|\_\_OPERATION\_\_| |要运行工具程序（会找到${\_\_OPERATION\_\_}.tar.gz作为任务要执行的内容）
|\_\_ADDRESS\_\_||任务发送方接收任务运行状态的ZMQ DEALER Socket地址
|\_\_GIVEN_ID\_\_| |任务发送方可以自己为任务指定ID，可以根据该ID来查询任务。
|\_\_FATHER_ID\_\_||指定新任务的父任务，父任务在结束时，LLTS会自动将其所有子任务停止掉。
|…| |任务执行时可以访问到的其他参数
 
如果请求中有\_\_ADDRESS\_\_字段，那么LLTS会在任务的状态发生改变时，主动向\_\_ADDRESS\_\_字段所包含的地址发送任务状态，详情见ZMQ DEALER接口部分。
 
2）响应的消息

| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TASK_ID\_\_| |分配给任务的ID
|\_\_CODE\_\_| |0表示消息包含的请求已被接受，非0表示被拒绝

##### 3.1.1.2 任务终止接口

用于主动杀死指定任务。
 
1）发送的消息

| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/KILL|终止任务
|\_\_TASK_ID\_\_| |要终止的任务ID。注意：不是\_\_GIVEN_ID_
 
2）响应的消息

| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0表示请求被接受，非0表示被拒绝

##### 3.1.1.3 任务状态查询接口

用于主动查询指定任务的状态。

1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/QUERY|查询任务状态
|\_\_TASK_ID\_\_| |用提交任务后返回的\_\_TASK_ID\_\_来查询任务状态
|\_\_GIVEN_ID\_\_| |也可用任务发送方自己指定的任务ID来查询任务状态
|…| |查询时可提供多个字段，只有所有字段都匹配才会返回任务信息。
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_STATUS\_\_| |‘WAITING’表示在任务排队中，‘RUNNING’表示运行中，’ENDED’表示正在清理，’FINISHED’表示已结束
|\_\_CODE\_\_| |0表示任务存在，非0表示查询被拒绝
|\_\_EXIT_CODE\_\_| |任务运行结束的退出码，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
|\_\_REPORT_LOG\_\_| |任务产生的报告信息report.log最后10K内容，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
|…| |其他跟任务相关的信息

##### 3.1.1.4 Agent统计信息接口

用于获取Agent统计信息。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/QUERY|获取Agent统计信息
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝
|\_\_TOTAL\_\_| |Agent总数
|\_\_FREE\_\_| |空闲Agent数量
|\_\_BUSY\_\_| |繁忙Agent数量
|\_\_LOST\_\_| |丢失Agent数量（超过两个心跳间隔未收到心跳，则认为Agent丢失）

##### 3.1.1.5 Agent心跳接口

用于Agent向Controller汇报心跳。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/HEARTBEAT|Agent心跳汇报
|\_\_AGENT_ID\_\_| |Agent的标识
|\_\_AGENT_STATUS\_\_| |Agent当前状态
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝

##### 3.1.1.6 Agent 退出接口

用于Agent向Controller发送退出信息。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/EXIT|Agent退出
|\_\_AGENT_ID\_\_| |Agent的标识
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝

##### 3.1.1.7 Agent任务状态汇报接口

用于Agent向Controller汇报任务状态。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INTERNAL/REPORT|Agent任务状态汇报
|\_\_AGENT_ID\_\_| |Agent的标识
|\_\_TASK_ID\_\_| |任务ID
|\_\_STATUS\_\_| |‘WAITING’表示在任务排队中，‘RUNNING’表示运行中，’ENDED’表示正在清理，’FINISHED’表示已结束
|\_\_EXIT_CODE\_\_| |任务运行结束的退出码，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
|\_\_REPORT_LOG\_\_| |任务产生的报告信息report.log（如果有的话）最后10K内容，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝

##### 3.1.1.8 任务申请接口

用于Agent向Controller申请任务。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INTERNAL/APPLY|Agent任务申请
|\_\_AGENT_ID\_\_| |Agent的标识
 
2）响应的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝
|\_\_TASK_ID\_\_| |任务ID
|\_\_OPERATION\_\_| |要运行工具程序（会找到${\_\_OPERATION\_\_}.tar.gz作为任务要执行的内容）
|…| |任务提交时附上的其他字段

#### 3.1.2 ZMQ PUB接口

ZMQ PUB会向Agent发布三类通知，任务通知、任务终止以及Agent终止。

##### 3.1.2.1 任务通知接口

用于Controller向Agent发布任务通知。Agent在订阅到这个通知后，可以通过任务申请接口向Controller申请任务去执行。
 
1）发布的消息

| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INFORM|任务通知

##### 3.1.2.2 任务终止接口

用于Controller向Agent发布任务终止通知。正在运行该任务的Agent在订阅到这个通知后，需要终止这个任务。
 
1）发布的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/KILL|任务终止
|\_\_TASK_ID\_\_| |任务ID
 
##### 3.1.2.3 Agent终止接口

用于Controller向Agent发布Agent终止通知。相应的Agent在订阅到这个通知后，需要停止正在运行的任务，然后向Controller发送Agent退出请求，最后完成退出。
 
1）发布的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/KILL|Agent终止
|\_\_AGENT_ID\_\_| |Agent标识

#### 3.1.3 ZMQ DEALER接口

ZMQ DEALER接口用于Controller向任务发送方发送任务状态。

##### 3.1.3.1 任务状态汇报接口

任务状态汇报接口是Controller在任务状态变化时向任务发起方推送任务状态信息。前提是在提交任务时，信息中包含\_\_ADDRESS\_\_字段，同时任务发起方以ZMQ DEALER方式绑定对应的\_\_ADDRESS\_\_。
 
任务发起方为了接受这个信息，可以：

a） 通过ZMQ.context创建一个context
b）通过context创建一个socket
c） 使用socket的bind方法绑定\_\_ADDRESS\_\_
d）通过socket的revc方法接收LLTS发送来的状态

Eg：

```
ZMQ.Context context = ZMQ.context(1);
ZMQ.Socket s = context.socket(ZMQ.DEALER); 
s.bind(\_\_ADDRESS\_\_); 
String rev = new String(s.recv(0));
``` 

1）发送的信息

| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TASK_ID\_\_| |任务ID
|\_\_STATUS\_\_| |‘WAITING’表示在任务排队中，‘RUNNING’表示运行中，’ENDED’表示正在清理，’FINISHED’表示已结束
|\_\_EXIT_CODE\_\_| |任务运行结束的退出码，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
|\_\_REPORT_LOG\_\_| |任务产生的报告信息report.log最后10K内容，当\_\_STATUS\_\_为’FINISHED’会附上这个字段

### 3.2 Agent

Agent通过ZMQ与Controller进行通信。主要涉及到两类接口，ZMQ REQ接口和ZMQ SUB接口。ZMQ REQ接口用来向Controller发送Agent心跳、申请任务、汇报任务状态和汇报Agent退出；ZMQ SUB接口用来订阅Controller发布的通知，包括新任务通知、终止Agent通知和终止任务通知。
 
#### 3.2.1 ZMQ REQ接口

Agent的ZMQ REQ接口用来向Controller发送Agent心跳、申请任务、汇报任务状态和汇报Agent退出。
 
Agent可通过以下方式与Controller的ZMQ REP接口建立连接：

a）通过ZMQ.context创建一个Context
b）通过context创建一个REQ Socket
c）使用REQ Socket的connect方法连接Controller
d）通过REQ Socket的send方法发送任务提交请求
e）通过REQ Socket的recv方法接收Controller发来的响应

Eg：

```
ZMQ.Context context = ZMQ.context(1);  
ZMQ.Socket s = context.socket(ZMQ.REQ); 
s.connect(address); 
s.send(message.getBytes(), 0);  
String rev = new String(s.recv(0));  
```

##### 3.2.1.1 Agent心跳接口

1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/HEARTBEAT|Agent心跳汇报
| \_\_AGENT_ID\_\_| |Agent的标识
| \_\_AGENT_STATUS\_\_| |Agent当前状态，0表示空闲，1表示忙碌；Agent启动之后要通过Agent心跳接口每3秒（可在 config.py 里配置）向Controller发送一次心跳，直到Agent退出。
 
2）接收的消息

在默认情况下，忽略接收到的消息。

##### 3.2.1.2 Agent退出接口

Agent退出时需要通过Agent退出接口向Controller汇报Agent退出。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
| \_\_TYPE\_\_|AGENT/EXIT|Agent退出
| \_\_AGENT_ID\_\_| |Agent的标识
 
2）接收的消息

在默认情况下，忽略接收到的消息。

##### 3.2.1.3 任务状态汇报接口

Agent在任务状态发生改变时需要向Controller汇报任务的状态。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INTERNAL/REPORT|Agent任务状态汇报
|\_\_AGENT_ID\_\_| |Agent的标识
|\_\_TASK_ID\_\_| |任务ID
|\_\_STATUS\_\_| |‘WAITING’表示在任务排队中，‘RUNNING’表示运行中，’ENDED’表示正在清理，’FINISHED’表示已结束
|\_\_EXIT_CODE\_\_| |任务运行结束的退出码，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
|\_\_REPORT_LOG\_\_| |任务产生的报告信息report.log最后10K内容，当\_\_STATUS\_\_为’FINISHED’会附上这个字段
 
##### 3.2.1.4 任务申请接口

Agent在收到Controller的任务通知后，若空闲，则申请任务。
 
1）发送的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INTERNAL/APPLY|Agent任务申请
|\_\_AGENT_ID\_\_| |Agent的标识
 
Controller接收到Agent的任务请求后：

a. 若该任务还未被领取，Controller接受Agent的任务申请。
b. 若该任务已被领取，Controller拒绝Agent的任务申请。
 
2）接收的消息（申请任务成功）
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_CODE\_\_| |0 表示请求被接收，非0表示请求被拒绝
|\_\_TASK_ID\_\_| |任务ID
|\_\_OPERATION\_\_| |要运行工具程序（会找到${\_\_OPERATION\_\_}.tar.gz作为任务要执行的内容）
|…| |任务提交时附上的其他字段
 
Agent若申请任务成功：

a. 解析接收的消息并在工作目录下准备task.info和Controller.info
b. 解压${\_\_OPERATION\_\_}.tar.gz到工作目录
c. 执行${\_\_OPERATION\_\_}目录下的run.sh，并汇报任务处于RUNNING状态
d. 任务执行完后，读取生成的report.log最后10K内容（如果有的话），并汇报任务处于ENDED状态
e. 清理工作区后，汇报任务处于FINISHED状态。

#### 3.2.2 ZMQ SUB接口

Agent使用ZMQ SUB接口订阅Controller的ZMQ PUB接口发布的通知并根据通知的类型执行相应的动作。
 
Agent可通过以下方式与Controller的ZMQ PUB接口建立连接：

a）通过ZMQ.context创建一个Context
b）通过context创建一个SUB Socket
c）使用SUB Socket的connect方法连接Controller
d）通过SUB Socket的recv方法接收Controller发来的响应

Eg：

```
ZMQ.Context context = ZMQ.context(1);
ZMQ.Socket s = context.socket(ZMQ.SUB); 
s.connect(address); 
String rev = new String(s.recv(0));
```
 
ZMQ SUB从ZMQ PUB订阅三类通知，任务通知、任务终止以及Agent终止。

##### 3.2.2.1 任务通知接口

用于Agent订阅任务通知。
 
1）订阅的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/INFORM|任务通知

收到任务通知后：

若忙碌，忽略该消息。
若空闲，通过任务申请接口申请任务。

##### 3.2.2.2 任务终止接口

用于Agent订阅任务终止通知。
 
2）订阅的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|TASK/KILL|任务终止
|\_\_TASK_ID\_\_| |任务ID
 
收到任务终止通知后：

若不是自己正在执行的任务，忽略该通知。
若是自己正在执行的任务，终止该任务，并调用任务状态汇报接口汇报任务状态。

##### 3.2.2.3 Agent终止接口

用于Agent订阅Agent终止通知。
 
2）订阅的消息
 
| 字段名 | 值 | 说明 |
|:---:|---|---|
|\_\_TYPE\_\_|AGENT/KILL|Agent终止
|\_\_AGENT_ID\_\_| |Agent标识
 
收到Agent终止通知后：

若需要终止的Agent不是自己，忽略该通知。
若需要终止的Agent是自己，终止正在执行的任务，然后调用Agent退出接口发送Agent退出请求，最后完成退出。

### 3.3 Controller和Agent交互信息

#### 3.3.1 Agent向Controller发送信息

Agent通过ZMQ REQ方式主动向Controller发送信息。
 
发送的信息包括：
 
|信息|使用的接口|
|---|---|
|Agent心跳信息|Agent心跳接口
|任务状态信息|Agent任务状态汇报接口
|Agent退出信息|Agent退出接口
|任务申请|任务申请接口
 
#### 3.3.2 Agent订阅Controller发布信息

Agent通过ZMQ SUB方式订阅Controller发布的信息。
 
订阅的信息包括：
 
|信息|使用的接口|
|---|---|
|任务通知信息|任务通知接口
|Agent终止信息|Agent终止接口
|任务终止信息|任务终止接口

## 4 LLTS-Tool规范说明

### 4.1 基本情况

LLTS-Tool是一个能够被LLTS框架运行的 tar.gz 格式的压缩包，该压缩包需要放在config.py中配置的AGENT_TOOLS_DIR目录下。一个LLTS-Tool中必须包含一个run.sh脚本作为LLTS-Tool启动的入口。
 
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

### 4.2 LLTS-Tool的启动

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
__TASK_ID__=TASK_*  (‘*’为任务提交时间)
```

controller.info文件中保存了LLTS框架的地址、运行该任务的Agent的IP。比如：

```
CONTROLLER_ADDRESS=tcp://192.168.1.100:11000
AGENT_IP=192.168.1.100
```

LLTS-Tool可以通过CONTROLLER_ADDRESS表示的ZMQ REQ Socket地址向LLTS发送各种请求。

### 4.3 LLTS-Tool运行过程中产生的数据

LLTS不关心业务逻辑相关的任何问题，因此进度、结果之类的信息的收集、转发、报告，最好 LLTS-Tool自己解决。
 
同时LLTS为LLTS-Tool提供了一种通用的数据收集方式，即LLTS-Tool在运行过程中可以将信息追加到与run.sh同级的report.log文件中。当任务执行完成后，LLTS会从report.log文件中读取最后10K字节的数据，传递给任务发送方。
 
以瓦片切割为例，worker每次向dispatcher申请一个瓦片的输出任务，并在完成后向dispatcher报告，这样dispatcher就可以在任何时刻知道当前有多少个瓦片已经输出完成，又有多少瓦片正在输出中。于是dispatcher就可以在输出进度到达整10百分比的时候直接写数据库，或通过ZMQ向某个地址发送当前的进度。

当运行出现错误时，可以将错误信息写到report.log中，最终通过LLTS将错误信息传递到任务发送方，方便任务发送方追查错误原因。

### 4.4 运行中的LLTS-Tool

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