# 智能路况监测员
## 项目说明
北京交通大学大学生创新创业项目
## 项目使用
### 环境配置
本项目主要运行在Docker环境下，请先安装Docker，不同操作系统安装Docker的方式不大一样，请根据自己的系统自行寻找安装教程进行安装。本程序测试环境为Ubuntu 18.04 LTS，根据Docker的特性，绝大部分系统应该都可以正常使用。

本项目基于Docker中的Ubuntu 18.04镜像，在安装时会自动从服务器下载。由于Docker默认的服务器在国外，下载速度较慢，如有需要请自行把镜像服务器地址改为国内地址。本人已将镜像中的apt源改为阿里云的源，如有特殊需求，请自行到Dockerfile中更改。

本项目将会创造5个Docker镜像，其中的主镜像配置文件位于
* Docker/Dockerfile

其余四个镜像均基于主镜像，其配置文件地址为
* App/Lane_Line_Recogniton/docker/Dockerfile
* App/Server/docker/Dockerfile
* App/Vehicle_Identification/docker/Dockerfile
* App/Vitual_Monitor/docker/Dockerfile

本项目默认端口为80，其配置位于文件
* run

如有其他需求请自行修改

本项目安装脚本基于bash，如果无bash请修改“run”文件或者根据“run”文件自行配置安装
### 安装
#### 修改run脚本权限（可选）
```shell
 chmod a+x run
 ```

#### 运行安装程序
如果不需要安装虚拟监控摄像头，则使用
```shell 
./run install
```

如果需要安装虚拟监控摄像头，则使用
```shell
./run install -v
```

下面的命令只要是安装了虚拟监控摄像头，都需要在后面加上 “-v“ 这一参数，后面将**不再具体说明**。

（虚拟监控摄像头是指在没有真实摄像头接口的情况下，使用虚拟监控摄像头来模拟实际监控摄像头的情况，一般情况下均需要安装，只有在实际生产环境下配置好了监控摄像头以及一系列相应的接口后才可以不使用虚拟监控摄像头。虚拟监控摄像头会循环播放内置的视频文件并输出，从而模拟真实监控摄像头的情况）

接下来程序会自动安装并在CLI上显示进度，请耐心等待。
### 更多命令说明
#### 启动程序
```shell
./run start
或
./run install -v
```

#### 停止程序
```shell
./run stop
或
./run stop -v
```
#### 重启程序
```shell
./run restart 
或
./run restart -v
```

#### 卸载程序
```shell
./run uninstall
或
./run uninstall -v
```