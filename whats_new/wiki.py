import os
import re
from datetime import date
from typing import TYPE_CHECKING

from pwiki import wiki

from .parser import WhatsNewParser
from .types import Vers

if TYPE_CHECKING:
    from .chillyroom import Apk


class Wiki:
    def __init__(self):
        self.vers: Vers
        password = os.environ.get("HUIJIWIKI_PASSWORD")
        self.wiki = wiki.Wiki("yqqs.huijiwiki.com", "慕棱", password or "")

    def find_vers(self, text: str) -> re.Match:
        if m := re.search(r"==(\d).(\d).(\d)", text):
            self.vers = Vers(*m.groups())
            return m

        raise RuntimeError("维基找不到旧版本号")

    def insert_whats_new(self, apk: "Apk", whats_new_text: str):
        parser = WhatsNewParser()
        whats_new = parser.get_result(whats_new_text)

        page_name = "更新日志" if __debug__ else "Project:Sandbox/ML"
        print(f"更新页面为 {page_name}")
        wiki_text = self.wiki.page_text(page_name)

        m = self.find_vers(wiki_text)

        if tuple(map(int, apk.vers)) <= tuple(map(int, self.vers)):
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

        if output_path := os.environ.get("GITHUB_OUTPUT"):
            with open(output_path, "a") as out:
                out.write("need_upload=1\n" f"vers={vers_str}\n")
            with open("whats_new.txt", "w") as f:
                f.write(whats_new_text)

        print(f"将更新至{vers_str}版本")

        insert_index = m.span()[0]
        self.wiki.edit(
            page_name,
            wiki_text[:insert_index] + content + wiki_text[insert_index:],
        )
