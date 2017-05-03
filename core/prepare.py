# coding=utf-8
import lib.common
import glob


def import_modules_phase_one():
    # Scan module files in mod/phase1/ and save them into MODULE_NAME_SET_PRE
    for __file_name in glob.glob(lib.common.PROJECT_PATH + 'mod/phase1/*.py'):
        if '__init__' not in __file_name:
            lib.common.MODULE_NAME_SET_PRE.append(__file_name.split('/')[-1].replace('.pyc', '').replace('.py', ''))

    # Import modules in MUDOLE_NAME_SET_PRE and save them into MODULE_OBJ_SET_PRE
    for __module_name in lib.common.MODULE_NAME_SET_PRE:
        print '\t>>>>[2] \_%s\t' % __module_name,
        try:
            __module_obj = __import__(lib.common.PROJECT_PATH + 'mod.phase1' + __module_name, fromlist=["*.py"])
            lib.common.MODULE_OBJ_SET_PRE.append(__module_obj)
            lib.common.MODULE_NAME_SET_PRE.append(__module_name)

            # init the set of result
            lib.common.RESULT_DIRECROTY[__module_name] = []

            # ini the set of sharing things | to be perfect
            # lib.common.SHARING_DICTIONARY[__module_name] = {}
        except Exception, e:
            continue


def run_modules_phase_one():
    print 'INITIALIZING...'
