#-*- coding: utf-8 -*-
import argparse

import domain
import engine

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_compile = subparsers.add_parser('generate')
    parser_compile.add_argument('template', metavar='FILE', help='source template for a WLST-script')
    parser_compile.set_defaults(func=engine.main)

    parser_domain = subparsers.add_parser('domain')
    parser_domain.add_argument('name', help='give this domain a specific name')
    parser_domain.add_argument('--user', default = 'weblogic')
    parser_domain.add_argument('--password', default = 'weblogic1')
    parser_domain.set_defaults(func=domain.main)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
       print('exception: ' + str(e))

if __name__ == '__main__':
    main()

