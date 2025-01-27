

# FurryBot

![Static Badge](https://img.shields.io/badge/python-3.9-green) ![GitHub last commit](https://img.shields.io/github/last-commit/nomyowo/FurryBot)

本项目基于[ClovertaTheTrilobita](https://github.com/ClovertaTheTrilobita)大佬的[SanYeCao-bot](https://github.com/ClovertaTheTrilobita/SanYeCao-bot)项目二次开发而成，新增ai聊天与圣经（类似于qq的设为精华）功能

## 目录

- [上手指南](#上手指南)
  - [开发前的配置要求](#开发前的配置要求)
  - [安装步骤](#安装步骤)
- [文件目录说明](#文件目录说明)
- [贡献者](#贡献者)
- [版本控制](#版本控制)
- [作者](#作者)
- [鸣谢](#鸣谢)

## 上手指南



### 开发前的配置要求

1. Python3.9
2. sm.ms的token
3. QQBot的appid和secret
4. ai聊天的api_key（本项目使用deepseek_api）

### **Ubuntu部署步骤（超级详细版）**

1. 安装前准备：已安装好gcc编译器，已安装好git，已安装wget等下载工具

2. 下载python3.9.10：进入Ubuntu控制台，在命令行输入

   ```
   sudo wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tar.xz
   ```

   下载后输入

   ```
   tar -xf Python-3.9.10.tar.xz
   cd Python-3.9.10
   ```

   解压该压缩包，并进入该目录

3. 安装openssl和libssl-dev：命令行中输入

   ```
   sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libbz2-dev liblzma-dev sqlite3 libsqlite3-dev tk-dev uuid-dev libgdbm-compat-dev openssl libssl-dev
   ```

   注意，Python 的部分功能依赖于对应的库（如 OpenSSL、SQLite3、LZMA 等），如果在编译时未能找到这些库，仍然可能完成编译。此时的 Python 解释器看似可以工作，但在需要使用特定功能时就会出问题。

4. 编译python环境：进入python解压目录中，输入

   ```
   ./configure --with-sqlite3 --with-ssl --enable-optimizations --with-lto
   ```

   之后进行编译，输入

   ```
   sudo make
   ```

   待编译完成后，输入

   ```
   sudo make altinstall
   ```

   安装python二进制文件

5. 验证安装结果：输入python3或python3.9，若出现>>>则安装成功，此时输入

   ```
   import ssl
   import sqlite3
   ```

   若未出现报错则安装成功

6. 同步项目：输入

   ```
   git clone https://github.com/nomyowo/FurryBot.git
   ```

   同步项目至本地，进入项目目录

7. 配置config.yaml文件：在项目根目录中输入

   ```
   vim config.yaml
   ```

   创建配置文件

   在该文件中粘贴

   ```
   # 机器人配置
   appid: "你的appid"
   secret: "你的secret"
   
   # 图床配置
   picturesToken: "sm.ms图床的token"
   
   # AI配置
   api_key: "ai工具的api"
   
   ```

   按esc推出编辑模式，输入:wq保存

8. 新建数据库存放文件夹：项目根目录中输入

   ```
   mkdir database
   ```

   新建database文件夹存放sqlite数据库文件

9. 配置虚拟环境：输入

   ```
   sudo apt install python3-venv 
   ```

   安装Virtualenv工具，之后进入项目目录，输入

   ```
   python3 -m venv venv
   ```

   （前面的python3需为python3.9所属命令），之后输入

   ```
   source venv/bin/activate 
   ```

   进入环境，此时命令行左边会出现（venv）标识，输入

   ```
   pip install -r requirements.txt
   ```

   安装所需包

10. 启动项目：在项目根目录下输入

    ```
    python client.py
    ```

    启动项目，若出现连接成功字样，则启动完成

## 文件目录说明
```
FurryBot
├── LICENSE.txt
├── README.md
├── /database/（数据库存放文件夹，需手动新建）
│  └── chatbot.db （数据库文件，运行后自动创建）
├── /plugins/
│  ├── __init__.py
│  ├── ai_chat.py
│  ├── database_init.py
│  ├── fortune_by_sqlite.py
│  ├── img_save.py
│  ├── img_upload.py
│  ├── sj_get.py
│  ├── user_todo_list.py
│  ├── weather_api.py
│  └── web_screen_shot.py
├── client.py （项目主程序）
├── requirements.txt （python包配置）
├── config.yaml （项目配置文件）
└── botpy.log （系统日志，运行后自动创建）

```



## 贡献者

本项目基于[icevale-sudo (Icevale)](https://github.com/icevale-sudo)的[icevale-sudo/shengjing-bot](https://github.com/icevale-sudo/shengjing-bot)项目进行官方机器人移植



## 版本控制

该项目使用Git进行版本管理。您可以在repository参看当前可用版本。

## 作者

诺米 

## 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](./LICENSE.txt)

## 鸣谢

本项目基于[ClovertaTheTrilobita](https://github.com/ClovertaTheTrilobita)大佬的[SanYeCao-bot](https://github.com/ClovertaTheTrilobita/SanYeCao-bot)项目二次开发而成，新增ai聊天与圣经（类似于qq的设为精华）功能，在此向大佬表达由衷的谢意！🙏🙏

本ReadMe基于[shaojintian (shaojintian)](https://github.com/shaojintian)的[shaojintian/Best_README_template: 🌩最好的中文README模板⚡️Best README template](https://github.com/shaojintian/Best_README_template)的模板编写，在此向大佬表达由衷的谢意！🙏🙏

参考资料：

[Ubuntu系统下启动Python项目文件夹的详细步骤与技巧 - 云原生实践](https://www.oryoy.com/news/ubuntu-xi-tong-xia-qi-dong-python-xiang-mu-wen-jian-jia-de-xiang-xi-bu-zhou-yu-ji-qiao.html)

[在 Ubuntu 22.04 上安装 Python 3.9（多版本适用）_ubuntu22.04安装python3.9-CSDN博客](https://blog.csdn.net/mziing/article/details/124475877)

[Linux(Centos)部署 Python项目_centos部署python项目-CSDN博客](https://blog.csdn.net/weixin_44593504/article/details/123134895)

[“/usr/bin/python3: No module named pip“的解决-CSDN博客](https://blog.csdn.net/LegendNoTitle/article/details/125908900)

[linux下sqlite安装及基本使用_linux sqlite-CSDN博客](https://blog.csdn.net/qq_51368339/article/details/127896474)

[解决 python3 “No module named '_ssl'“ - 知乎](https://zhuanlan.zhihu.com/p/336907257)

