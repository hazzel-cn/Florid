#! /usr/bin/env python
# coding=utf-8

def red(mess):
    print '\033[31m%s\033[0m' % str(mess),


def green(mess):
    print '\033[32m%s\033[0m' % str(mess),


def yellow(mess):
    print '\033[33m%s\033[0m' % str(mess),


def blue(mess):
    print '\033[34m%s\033[0m' % str(mess),


def pink(mess):
    print '\033[35m%s\033[0m' % str(mess),


def sky_blue(mess):
    print '\033[36m%s\033[0m' % str(mess),


def white(mess):
    print '\033[37m%s\033[0m' % str(mess),
