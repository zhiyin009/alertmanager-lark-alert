import json

import requests

data1 = {
    "receiver":
    "futures_feishu_msg",
    "status":
    "firing",
    "alerts": [
        {
            "status": "firing",
            "labels": {
                "idc": "北京",
                "alertgroup": "节点",
                "alertname": "节点响应超时",
                "instance": "1.1.1.1:8000",
                "job": "node alive",
            },
            "annotations": {
                "description": "上海 1.1.1.1:8000 响应超时",
                "summary": "节点响应超时",
            },
            "startsAt": "2022-02-22T07:31:16.246433346Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://127.0.0.1:3000",
            "fingerprint": "a0a0a0a0a0a0",
        },
        {
            "status": "firing",
            "labels": {
                "idc": "上海",
                "alertgroup": "节点",
                "alertname": "节点响应超时",
                "instance": "2.2.2.2:8000",
                "job": "node alive",
            },
            "annotations": {
                "description": "上海 2.2.2.2:8000 响应超时",
                "summary": "节点响应超时",
            },
            "startsAt": "2022-02-22T07:31:16.246433346Z",
            "endsAt": "0001-01-01T00:00:00Z",
            "generatorURL": "http://127.0.0.1:3000",
            "fingerprint": "a0a0a0a0a0a0",
        },
    ],
    "groupLabels": {
        "idc": "上海",
        "alertname": "节点响应超时"
    },
    "commonLabels": {
        "idc": "上海",
        "alertgroup": "节点",
        "alertname": "节点响应超时",
        "feishu_msg": "true",
        "instance": "127.0.0.1:8000",
        "job": "node alive",
    },
    "commonAnnotations": {
        "summary": "节点响应超时00"
    },
    "externalURL":
    "http://alertmanager:9093",
    "version":
    "4",
    "groupKey":
    '{}/{alertgroup=~"Futures.*",feishu_msg="true"}:{idc="上海", alertname="节点响应超时"}',
    "truncatedAlerts":
    0,
}
r = requests.post("http://127.0.0.1:8201/lark_platform_alert",
                  data=json.dumps(data1))
