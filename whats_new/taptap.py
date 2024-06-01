from dataclasses import dataclass
from typing import TypedDict

import httpx


class TextDict(TypedDict):
    text: str


@dataclass
class WhatsNewDict:
    version_label: str
    update_date: int
    whatsnew: TextDict

    def get_vers(self):
        return self.version_label.split(" (")[0]


def get_last_update() -> WhatsNewDict:
    headers = {
        "user-agent": "Mozilla/6.0 (Windows NT 10.0; Win64; x64) AppleWebKit/666.66 (KHTML, like Gecko) Edg/100.0.0.0"
    }
    r = httpx.get(
        "https://www.taptap.cn/webapiv2/apk/v1/list-by-app?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D66%26LOC%3DCN%26PLT%3DPC&app_id=34751",
        headers=headers,
    )
    d = r.json()
    if d["success"] == "false":
        raise RuntimeError("获取更新公告失败")

    return WhatsNewDict(**d["data"]["list"][0])
