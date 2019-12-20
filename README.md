# vision
人脸识别

# 说明
人脸识别，基于bottle框架开发，采用国内七牛存储，百度人脸识别技术


# 项目主要结构
```
├── Dockerfile
├── gunicorn_logger.py
├── pytest.ini
├── README.md
├── requirements-test.txt           -测试程序模块安装
├── requirements.txt                -程序模块安装
├── run.py                          -主程序
├── tests                           -pytest测试
│   ├── functional
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   └── test_qiniu.py
│   ├── helper.py
│   ├── __init__.py
│   └── unit
│       └── __init__.py
└── vision
    ├── api                         -百度API调用
    │   ├── baidu.py
    │   ├── base.py
    │   └── __init__.py
    ├── app.py
    ├── auth.py
    ├── config                      -程序配置文件
    │   ├── base.ini
    │   ├── __init__.py
    │   └── testing.ini
    ├── controllers                 -程序路由逻辑
    │   ├── index.py
    │   ├── __init__.py
    │   ├── qn.py
    │   └── storage.py
    ├── db.py                       -初始化db
    ├── error.py                    -错误定义
    ├── __init__.py
    ├── models.py                   -ORM定义
    ├── plugins.py                  -返回值定义
    ├── qcp.py                      -七牛存储模块
    ├── serializers.py              -marshmallow数据定义
    ├── snowflake.py                -雪花ID算法
    ├── tables.py                   -初始化表
    ├── utils.py                    -组件模块
    └── validators.py               -数据验证
```

# 运行环境
python 3.6.7


# 功能说明
```
    简单web服务

    1.首先百度云申请人脸识别, 创建应用获取的API Key及Secret Key

    2.七牛云存储 申请空间 获取存储空间，AK以及SK

    相关配置填入配置文件：
    [qiniu]
    storage.bucket_name = __placeholder__
    storage.domain_name = __placeholder__
    storage.access_key = __placeholder__
    storage.secert_key = __placeholder__

    [baidu]
    aip.client_secret   = __placeholder__
    aip.client_id       = __placeholder__


    提供两个接口：
    1./api/v1/upload  -图片上传
    2./api/v1/storages/<storage_id>/detect-face -图片检测，是否是人脸图片
```

# 运行方式
    python run.py