import IPython
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p",
        "--password",
        dest="password",
        required=True)
    args = parser.parse_args()

    hash = IPython.lib.passwd(args.password)
    print("アクセストークン -> " + hash)
