import lib.colorprint
import lib.common


class Importer(object):
    def __int__(self):
        lib.colorprint.color().blue('[*] Importing Modules')

    def import_one(self):
        for __module_name in lib.common.MODULE_ONE_NAME_LIST:
            # print '*', __module_name, '\t',
            try:
                __module_obj = __import__('module.phase_one.' + __module_name, fromlist=['*.py'])
                # lib.colorprint.color().green('SUCCESS')
                lib.common.MODILE_ONE_OBJ_DICT[__module_name] = __module_obj
                lib.common.ALIVE_LINE[__module_name] = 0
            except Exception, e:
                lib.colorprint.color().red(str(e))

    def import_two(self):
        for __module_name in lib.common.MODULE_NAME_LIST:
            print '*', __module_name.ljust(40, '.'),
            try:
                __module_obj = __import__('module.phase_two.' + __module_name, fromlist=['*.py'])
                lib.common.MODULE_OBJ_DICT[__module_name] = __module_obj
                lib.common.RESULT_DICT[__module_name] = []
                lib.common.ALIVE_LINE[__module_name] = 0
                __module_obj.init()
                lib.colorprint.color().green('SUCCESS')
            except Exception, e:
                lib.common.MODULE_NAME_LIST.remove(__module_name)
                lib.colorprint.color().red(str(e))
        print

    def do_import(self):
        lib.colorprint.color().blue('[*] Importing Modules')
        self.import_one()
        self.import_two()
