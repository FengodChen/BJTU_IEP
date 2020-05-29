# 项目说明
北京交通大学大学生创新创业项目
# 项目使用
## 环境配置
本项目主要运行在Docker环境下，请先安装Docker，不同操作系统安装Docker的方式不大一样，请根据自己的系统自行寻找安装教程进行安装。本程序测试环境为Ubuntu 18.04 LTS，根据Docker的特性，绝大部分系统应该都可以正常使用。

本项目基于Docker中的Ubuntu 18.04镜像，在安装时会自动从服务器下载。由于Docker默认的服务器在国外，下载速度较慢，如有需要请自行把镜像服务器地址改为国内地址。本人已将镜像中的apt源改为阿里云的源，如有特殊需求，请自行到Dockerfile中更改。

本项目将会创造5个Docker镜像，其中的主镜像配置文件位于
* Docker/Dockerfile

其余四个镜像均基于主镜像，其配置文件地址为
* App/Lane_Line_Recogniton/docker/Dockerfile
* App/Server/docker/Dockerfile
* App/Vehicle_Identification/docker/Dockerfile
* App/Vitual_Monitor/docker/Dockerfile

本项目默认端口为10，其配置位于文件
* run

如有其他需求请自行修改

本项目安装脚本基于bash，如果无bash请修改“run”文件或者根据“run”文件自行配置安装
## 安装
### 修改run脚本权限（可选）
```shell
 chmod a+x run
 ```

### 运行安装程序
```shell 
./run install
```

如果需要安装虚拟监控摄像头，则使用
```shell
./run install -v
```

下面的命令只要是安装了虚拟监控摄像头，都需要额外加上 “-v“ 这一参数的指令，后面将**不再具体说明**。

（虚拟监控摄像头是指在没有真实摄像头接口的情况下，使用虚拟监控摄像头来模拟实际监控摄像头的情况，一般情况下均需要安装，只有在实际生产环境下配置好了监控摄像头以及一系列相应的接口后才可以不使用虚拟监控摄像头。虚拟监控摄像头会循环播放内置的视频文件并输出，从而模拟真实监控摄像头的情况）

接下来程序会自动安装并在CLI上显示进度，请耐心等待。
### 更多命令说明
启动程序
```shell
./run start
./run start -v
```

停止程序
```shell
./run stop
./run stop -v
```
重启程序
```shell
./run restart 
./run restart -v
```

卸载程序
```shell
./run uninstall
./run uninstall -v
```
帮助
```shell
./run help
```

## 程序运行
### 前置条件
在执行启动命令
```bash
./run start
或
./run start -v
```
之后，即可通过网页启动，为了安全，默认仅通过本地地址[http://127.0.0.1:10/]()启动，若需要通过外网访问，请修改run文件里的配置。
### 车辆识别
程序启动后，边自动开始进行车辆识别并统计。
### 打开界面
使用任意浏览器（推荐使用Google Chrome）打开[http://127.0.0.1:10/]()进入客户端，可在上方的选项中选择各功能。

![初始界面](./md_images/home.png)
### 实时监控界面
点击实时监控即可看到实时监控界面

![实时监控](./md_images/monitor.png)

在左侧输入道路名称并点击输入即可切换道路，如果是虚拟监控摄像头，所有道路名称在
* Share/Vitual_Monitor_Video

文件路径下查找，若为实际监控摄像头，则根据实际提供的信息查找。

### 数据统计界面
点击数据统计即可看到数据统计界面

![数据统计_主界面](./md_images/data_analyze_1.png)

#### 模式一：按日期统计模式

在左侧输入道路名称，并选择“开始时间”和“结束时间”，点击“按日期”，即可得到按日统计的统计结果。

![数据统计_按日期统计](./md_images/data_analyze_2.png)
#### 模式一：按时间统计模式

在左侧输入道路名称，并选择“日期”，点击“按时间”，即可得到按时间统计的统计结果。

![数据统计_按时间统计](./md_images/data_analyze_3.png)

#### 统计数据操作

得到统计结果后，可在统计图上筛选时间、日期以及区域名称。

### 区域设置界面
点击区域设置即可看到区域设置界面。

![区域设置_主界面](./md_images/area_setting_1.png)

在左侧输入路段名称并点击“载入次监控”，便可得到监控当前帧的图像。

![区域设置_载入](./md_images/area_setting_2.png)

在图像中点击，两个点击点之间会出现一条红线，这些红线围起来的区域便是你想要命名的区域。

![区域设置_点击](./md_images/area_setting_3.png)

在操作台输入你想对该区域的命名，点击“确认区域功能”，程序便会将这一区域用颜色标记出来。

![区域设置_确认区域](./md_images/area_setting_4.png)

在确认完所有区域后，点击“保存”即可将区域信息保存，数据文件将存入相应文件夹内。

![区域设置_保存](./md_images/area_setting_5.png)