import os
import re
from datetime import date
from typing import TYPE_CHECKING

from mwclient import Site

from .parser import WhatsNewParser
from .types import Vers

if TYPE_CHECKING:
    from .chillyroom import Apk


class Wiki:
    def __init__(self):
        self.vers: Vers
        ua = 'UpdateWhatsNew/0.1 (F-park@www.github.com)'
        self.site = Site("yqqs.huijiwiki.com", clients_useragent=ua)
        password = os.environ.get("HUIJIWIKI_PASSWORD")
        self.site.login("慕棱", password)

    def get_text(self, name="更新日志"):
        self.whats_new = self.site.pages[name]
        return self.whats_new.text()

    def find_vers(self, text: str) -> re.Match:
        if m := re.search(r"==(\d).(\d).(\d)", text):
            self.vers = Vers(*m.groups())
            return m

        raise RuntimeError("维基找不到旧版本号")

    def insert_whats_new(self, apk: "Apk", whats_new_text: str):
        parser = WhatsNewParser()
        whats_new = parser.get_result(whats_new_text)

        wiki_text = self.get_text("" if __debug__ else "Project:Sandbox/ML")
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
                out.writelines(("need_upload=1", f"vers={vers_str}"))
            with open("whats_new.txt", "w") as f:
                f.write(whats_new_text)

        print(f"将更新至{vers_str}版本")

        insert_index = m.span()[0]
        self.whats_new.edit(
            wiki_text[:insert_index] + content + wiki_text[insert_index:], bot=False
        )
