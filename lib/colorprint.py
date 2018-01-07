import common


def color():
    if common.CONFIG['OS_type'] == 'WIN':
        import __colorprint_win
        return __colorprint_win.ColorPrintWin()
    else:
        import __colorprint_nix
        return __colorprint_nix.ColorPrintNix()
