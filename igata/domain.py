#-*- coding: utf-8 -*-

import os

import igata.data as data

def main(args):
    generate(args.name, args.user, args.password)

def generate(name, user, password):
    print data.domain.format(domain={'name' : name, 'user' : user, 'password' : password})

