# coding=utf-8
# This file provide an object of ColorPrint class on different OS
'''
# filename: ColorPrint.py
# phase: 1
'''
import common


def color():
    if common.OS == 'WIN':
        import lib.colorprint_win
        return lib.colorprint_win.ColorPrintWin()
    else:
        import lib.colorprint_nix
        return lib.colorprint_nix.ColorPrintNix()


if __name__ == '__main__':
    color().green('DAWN is HERE')
    print __doc__
