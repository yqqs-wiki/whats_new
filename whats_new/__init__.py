from argparse import ArgumentParser, Namespace

from .chillyroom import download_apk, get_apk
from .github import check_release_needed
from .taptap import get_last_update
from .wiki import Wiki


class Args(Namespace):
    update: bool
    download: bool


def main():
    parser = ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-d", "--download", action="store_true")
    args = parser.parse_args(namespace=Args())
    if args.update:
        last_update = get_last_update()
        wiki = Wiki()

        wiki.insert_whats_new(get_apk(), last_update.whatsnew["text"])
    elif args.download:
        if check_release_needed(get_apk()):
            download_apk()
