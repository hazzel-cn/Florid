# coding=utf-8

import lib.common
import lib.colorprint


def import_modules_phase_two():
    for __module_name in lib.common.COMMAND_SET['module_list']:
        lib.colorprint.color().sky_blue('> [%s]\t' % __module_name)
        try:
            __module_obj = __import__('mod.phase2.' + __module_name, fromlist=["*.py"])

            lib.common.MODULE_DIRECTORY[__module_name] = __module_obj

            # init the set of result
            lib.common.RESULT_DIRECROTY[__module_name] = []

            # init the set of sharing things | to be perfect
            # lib.common.SHARING_DICTIONARY[__module_name] = {}

            lib.common.CHECKED_COUNT[__module_name] = 0

            __module_obj.init()
            lib.colorprint.color().green('DONE\n')
        except Exception, e:
            lib.colorprint.color().red(str(e) + '\n')
            pass
    lib.colorprint.color().green('\nImportation Done\n')
