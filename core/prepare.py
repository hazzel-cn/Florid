# coding=utf-8
import glob
import re

import lib.colorprint
import lib.common


def import_modules_phase_one():
    # Scan module files in mod/phase1/ and save them into MODULE_NAME_SET_PRE
    for __file_name in glob.glob(lib.common.PROJECT_PATH + '/mod/phase1/*.py'):
        if '__init__' not in __file_name and 'pyc' not in __file_name:
            __module_name = re.findall('.*(/|\\\\)(.+)\.py$', __file_name)[0][1]
            lib.common.MODULE_NAME_SET_PRE.append(__module_name)

    # Import modules in MUDOLE_NAME_SET_PRE and save them into MODULE_OBJ_SET_PRE
    for __module_name in lib.common.MODULE_NAME_SET_PRE:
        lib.colorprint.color().sky_blue('>[1] %s\t' % __module_name)
        try:
            __module_obj = __import__('mod.phase1.' + __module_name, fromlist=["*.py"])
            lib.common.MODULE_OBJ_SET_PRE.append(__module_obj)
            # lib.common.MODULE_NAME_SET_PRE.append(__module_name)

            # init the set of result
            lib.common.RESULT_DIRECROTY[__module_name] = []

            # ini the set of sharing things | to be perfect
            # lib.common.SHARING_DICTIONARY[__module_name] = {}
            lib.colorprint.color().green('DONE' + '\n')
        except Exception, e:
            lib.colorprint.color().red(str(e) + '\n')


def run_modules_phase_one():
    # print 'INITIALIZING PHASE ONE...'
    # print lib.common.RESULT_DIRECROTY
    for __module_obj in lib.common.MODULE_OBJ_SET_PRE:
        __module_obj.run()
