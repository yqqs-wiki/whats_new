from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true")
    args = parser.parse_args()
    if args.update:
        print("hello world")
