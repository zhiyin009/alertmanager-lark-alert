# -*- coding: utf-8 -*-
# @Author: zyxiao
# @Date: 2022-02-19 17:31:50

import logging
import time
from collections import defaultdict
from typing import Dict, List

import requests
from flask import Flask, json, request
from markupsafe import escape

STATUS_COLOR = defaultdict(lambda: "green")
STATUS_COLOR["firing"] = "red"

STATUS_EMOJI = defaultdict(lambda: "ℹ️")
STATUS_EMOJI["firing"] = "🔥"
STATUS_EMOJI["resolved"] = "✅"

SEVERITY_EMOJI = defaultdict(lambda: "⚠️")
SEVERITY_EMOJI["critical"] = "💀"

DEFAULT_PANEL_URL = "http://grafana.my/?orgId=1"

def format(data: Dict, override_summary: str = ""):
    alerts = data.get("alerts", None)
    lark_alerts = {
        "tag": "div",
        "fields": [],
    }
    lark_alerts["fields"] = [{
        "is_short": False,
        "text": {
            "content":
            f"[{SEVERITY_EMOJI[alert['labels'].get('severity', '')]} {alert['annotations'].get('description', '该规则未填写 description')}]({alert['annotations'].get('dashboardURL', DEFAULT_PANEL_URL)})",
            "tag": "lark_md",
        },
    } for alert in alerts]
    # print(data)

    status = data["status"]
    common_labels = data["commonLabels"]
    common_annotations = data["commonAnnotations"]
    title = (common_labels["alertname"] if "alertname" in common_labels else common_labels.get("alertgroup", "未知组合报警"))
    if override_summary or common_labels.get("test", False):
        summary = override_summary
    else:
        summary = (f'**{common_annotations["summary"]}** \n\r' if "summary" in common_annotations else "")

    return {
        "msg_type": "interactive",
        "card": {
            "config": {
                "enable_forward": True
            },
            "header": {
                "title": {
                    "content": f"{STATUS_EMOJI[status]} {title}",
                    "tag": "plain_text",
                },
                "template": STATUS_COLOR[status],
            },
            "elements": [
                lark_alerts,
                # {"tag": "hr"},
                {
                    "tag": "note",
                    "content": "",
                    "elements": [
                        {
                            "tag": "lark_md",
                            "content": "".join([
                                summary,
                                f'⏰ **{time.strftime(r"%Y-%m-%d %H:%M:%S")}**',
                            ]),
                            "elements": None,
                        },
                    ],
                },
            ],
        },
    }


app = Flask(__name__)
@app.route("/lark_platform_alert", methods=["GET", "POST"])
def lark_platform_alert():
    data = json.loads(request.get_data())
    msg = format(data)

    headers = {"Content-Type": "application/json"}
    # 飞书报警群 url
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/------------"
    r = requests.post(url=url, headers=headers, data=json.dumps(msg))
    logging.info(f"平台报警: response={r.content}")

    return escape(r)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8201", debug=False)