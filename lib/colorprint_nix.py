#! /usr/bin/env python
# coding=utf-8
import sys


def red(mess):
    sys.stderr.write('\033[31m%s\033[0m' % str(mess)),


def green(mess):
    sys.stdout.write('\033[32m%s\033[0m' % str(mess)),


def yellow(mess):
    sys.stderr.write('\033[33m%s\033[0m' % str(mess)),


def blue(mess):
    sys.stderr.write('\033[34m%s\033[0m' % str(mess)),


def pink(mess):
    sys.stderr.write('\033[35m%s\033[0m' % str(mess)),


def sky_blue(mess):
    sys.stdout.write('\033[36m%s\033[0m' % str(mess))


def white(mess):
    sys.stderr.write('\033[37m%s\033[0m' % str(mess)),
