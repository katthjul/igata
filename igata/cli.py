# -*- coding: utf-8 -*-
import argparse

import engine
import run
import sys

# sys.path.append('C:/Program Files/JetBrains/PyCharm 2017.2.1/debug-eggs/pycharm-debug.egg')
#
# import pydevd

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_generate = subparsers.add_parser('generate')
    parser_generate.add_argument('template', metavar='FILE', help='source template for a WLST-script')
    parser_generate.set_defaults(func=engine.main)

    parser_run = subparsers.add_parser('run')
    parser_run.add_argument('script', nargs=argparse.REMAINDER, metavar='COMMAND', help='a WLST-script with arguments')
    parser_run.set_defaults(func=run.main)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        sys.stdout = sys.__stdout__
        print('exception: ' + str(e))
        exit(-1)


if __name__ == '__main__':
    # pydevd.settrace('localhost', port=53704, stdoutToServer=True, stderrToServer=True)
    main()
