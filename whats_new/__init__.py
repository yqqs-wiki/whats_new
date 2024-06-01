from argparse import ArgumentParser, Namespace


class Args(Namespace):
    update: bool
    download: bool


def main():
    parser = ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true")
    parser.add_argument("-d", "--download", action="store_true")
    args = parser.parse_args(namespace=Args())
    if args.update:
        print("hello world")
