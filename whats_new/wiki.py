import os
import re

from mwclient import Site

from .types import Vers


class Wiki:
    def __init__(self):
        self.site = Site("yqqs.huijiwiki.com")
        password = os.environ.get("HUIJIWIKI_PASSWORD")
        self.site.login("慕棱", password)

    def get_text(self, name="更新日志"):
        self.whats_new = self.site.pages[name]
        return self.whats_new.text()

    def get_vers(self) -> Vers:
        text = self.get_text()
        for line in text.split("\n"):
            if m := re.match(r"==(\d).(\d).(\d)", line):
                return Vers(*(int(_) for _ in m.groups()))

        raise RuntimeError("维基找不到旧版本号")
