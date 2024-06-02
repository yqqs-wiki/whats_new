from html.parser import HTMLParser


class WhatsNewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._result = ""
        self._prefix = ""
        self._br_count = 0

    def get_result(self, data):
        self.feed(data)
        return self._result

    def handle_endtag(self, tag):
        if tag == "br":
            self._br_count += 1
            self._result += "\n"

        if self._br_count == 2:
            self._prefix = ""

    def handle_data(self, data):
        self._br_count = 0
        if data.startswith("-") and self._prefix != "":
            data = data.removeprefix("-")
            self._prefix = "**"
        elif self._prefix == "**" and not data.startswith("-"):
            self._prefix = "*"

        self._result += self._prefix + data

        if data.startswith("【"):
            self._prefix = "*"
