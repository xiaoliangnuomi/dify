# Operation Manual

This is the operation manual for the project.
version: 1.1.3
author: wxl
## environment
    `
     backend:
    local machine: windows 11 
    python 3.12.0 recommented python 3.12.0
    frontend:
     nvm node 20.11.1
    
    `

## local development running
### backend

conda activate dify312
    ### 中间件启动
    `
    cd docker
    cp middleware.env.example middleware.env
    docker compose -f docker-compose.middleware.yaml up -d
    `
    后端启动 

    `
     cp .env.example .env
    ## 生成随机密钥 写入到.env文件中 字段是SECRET_KEY
    awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env

poetry env use 3.12
poetry install
poetry run flask db upgrade
poetry run flask run --host 0.0.0.0 --port=5001 --debug
linux 启动celery
poetry run celery -A app.celery worker -P gevent -c 1 -Q dataset,generation,mail,ops_trace --loglevel INFO

windows 启动celery
poetry run celery -A app.celery worker -P solo --without-gossip --without-mingle -Q dataset,generation,mail,ops_trace --loglevel INFO      
 `

### frontend 启动

Web 前端服务启动需要用到 Node.js v18.x (LTS) 、NPM 版本 8.x.x 或 Yarn。
    `
   nvm use 20
npm install -g pnpm
pnpm install --force
pnpm run build
npm run startwin
`
pnpm start 报错 cp 不是内部命令 用powershell 运行 pnpm start
改了package.json 中的start 命令为
里面的端口和地址去掉
 "startwin": "xcopy .next\\static .next\\standalone\\.next\\static /E /I /Y && xcopy public .next\\standalone\\public /E /I /Y && node .next\\standalone\\server.js",


### 后端知识介绍
`

`
   awk -v key="$(openssl rand -base64 42)" '/^SECRET_KEY=/ {sub(/=.*/, "=" key)} 1' .env > temp_env && mv temp_env .env
  -v key="$(openssl rand -base64 42)"：这是一个变量赋值操作，将生成的随机密钥赋值给变量 key。
  openssl rand -base64 42：这是一个命令，用于生成一个长度为 42 的随机字符串。这里使用了 openssl 工具的 rand 命令，-base64 选项指定生成的字符串是 base64 编码的。
  /^SECRET_KEY=/：这是一个正则表达式，用于匹配以 SECRET_KEY= 开头的行。
  sub(/=.*/, "=" key)：这是一个替换操作，用于将匹配到的行中的 = 后面的内容替换为生成的随机密钥。
  1：这是一个条件操作，用于指定 awk 命令在处理完所有行后继续执行。
  > temp_env && mv temp_env.env：这是一个重定向操作，将生成的随机密钥写入到名为 temp_env 的文件中，然后将 temp_env 文件重命名为 .env 文件。
  这个命令的作用是生成一个随机密钥，并将其写入到.env 文件中，以便在项目中使用。
  ` 

Poetry 相当于npm 本地有个python环境，然后安装pip install poetry 就可以使用poetry命令了。
   `
Poetry：主要专注于Python项目的依赖管理和打包分发。它旨在简化项目依赖的声明、安装和版本控制，同时提供了方便的打包和发布工具，使得开发者可以轻松地将项目打包成可分发的包。
Conda：是一个跨平台的包管理和环境管理系统，不仅支持Python，还支持R、Ruby、Lua、Scala等多种语言。Conda的设计目标是为数据科学和机器学习领域提供一个统一的环境管理解决方案，方便用户在不同的项目和环境中安装和管理各种软件包。   

`  

poetry run celery -A app.celery worker -P solo --without-gossip --without-mingle -Q dataset,generation,mail,ops_trace --loglevel INFO
celery 是一个基于 Python 开发的分布式任务队列系统，用于处理异步任务和定时任务。这个命令启动了 Celery 的相关功能。
-A app.celery：指定 Celery 应用程序的入口点。这里的 app 是你的 Celery 应用程序实例，celery 是实例的属性或方法。
worker：指定启动 Celery 工作进程的命令。工作进程负责执行任务队列中的任务。
-P 是 --pool 的缩写，用于指定任务执行的线程池或进程池类型 solo：指定工作进程的启动方式为 solo。solo 模式下，每个工作进程都在一个单独的进程中运行。
--without-gossip：禁用 Celery 的 gossip 功能。gossip 是一种用于发现和管理 Celery 集群的机制。状态更新和心跳检测
--without-mingle：禁用 Celery 的 mingle 功能。mingle 是一种用于发现和管理 Celery 集群的机制。混合机制用于工作进程之间的初始同步和信息共享
-Q dataset,generation,mail,ops_trace：指定要处理的任务队列。这里指定了多个任务队列，分别是 dataset、generation、mail 和 ops_trace。
--loglevel INFO：指定 Celery 工作进程的日志级别为 INFO。INFO 级别是 Celery 的默认日志级别，用于记录一般的信息和警告。