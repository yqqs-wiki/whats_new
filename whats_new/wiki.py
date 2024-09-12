import re
from datetime import date
from os import environ
from typing import TYPE_CHECKING

from mwclient import Site

from .parser import WhatsNewParser

if TYPE_CHECKING:
    from .chillyroom import Apk


class Wiki:
    def __init__(self):
        KEY = environ.get("HUIJIWIKI_KEY")
        PASSWORD = environ.get("HUIJIWIKI_PASSWORD")
        self.site = Site("yqqs.huijiwiki.com", custom_headers={"X-authkey": KEY})
        self.site.login("慕棱", PASSWORD)

    def find_vers(self, text: str) -> re.Match:
        if m := re.search(r"==(\d).(\d).(\d)", text):
            return m

        raise RuntimeError("维基找不到旧版本号")

    def insert_whats_new(self, apk: "Apk", whats_new_text: str):
        parser = WhatsNewParser()
        whats_new = parser.get_result(whats_new_text)

        page_name = "更新日志" if __debug__ else "Project:Sandbox/ML"
        print(f"更新页面为 {page_name}")
        page = self.site.pages[page_name]
        page_text = page.text()

        m = self.find_vers(page_text)

        if tuple(map(int, apk.vers)) <= tuple(map(int, m.groups())):
            print("已是最新版本")
            return

        today = date.today()
        vers_str = ".".join(apk.vers)
        today_str = today.strftime("%Y.%m.%d")
        content = "\n\n".join(
            (
                f"=={vers_str}版本==\n{today_str}",
                f"[{apk.url} {vers_str}安卓官网包下载]",
                whats_new,
                "",
            )
        )

        if output_path := environ.get("GITHUB_OUTPUT"):
            with open(output_path, "a") as out:
                out.write("need_upload=1\n" f"vers={vers_str}\n")
            with open("whats_new.txt", "w") as f:
                f.write(whats_new_text)

        print(f"将更新至{vers_str}版本")

        insert_index = m.span()[0]
        page.edit(
            page_text[:insert_index] + content + page_text[insert_index:], bot=False
        )
