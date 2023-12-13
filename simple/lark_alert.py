# -*- coding:utf-8 -*-

import json
import logging
from enum import Enum, auto
from typing import List

import requests


class Severity(Enum):
    Announce = 0
    Warning = auto()
    Critical = auto()

    def color(self) -> str:
        return ["blue", "yellow", "red"][self.value]


def lark_alert(title: str, severity: Severity, error_reasons: List[str]):
    try:
        lark_md_content = "\n".join([str(error) for error in error_reasons])
        lark_title = title
        msg = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True, "enable_forward": True},
                "elements": [
                    {
                        "tag": "div",
                        "text": {"content": lark_md_content, "tag": "lark_md"},
                        "content": "",
                        "elements": None,
                    },
                ],
                "header": {
                    "title": {"content": lark_title, "tag": "plain_text"},
                    "template": f"{severity.color()}",
                },
            },
        }

        if severity == Severity.Critical:
            msg["card"]["elements"].insert(0, {
                "tag": "div",
                "text": {"content": "<at id='all'></at>", "tag": "lark_md"}}
            )

        headers = {"Content-Type": "application/json"}
        lark_url = {
            "xxx通知群": "https://open.feishu.cn/open-apis/bot/v2/hook/---------------",
        }

        for url in lark_url.values():
            r = requests.post(url=url, headers=headers, data=json.dumps(msg))

        if r:
            logging.info(r.content)
    except Exception as e:
        logging.error(e)

def test():
    lark_alert("test", Severity.Announce, ["老六到楼下了"])
    lark_alert("test", Severity.Warning, ["热水开了"])
    lark_alert("test", Severity.Critical, ["煤气漏了"])