# alertmanager-lark-alert

包含两类用法
1. [simple](./simple/README.md) 直接 import 函数发送文字
2. [adapter](./adapter/lark_adapter.py): 启动一个本地 flask 服务，上游的 alertmanager 配置 webhook 通过该服务转发给 lark