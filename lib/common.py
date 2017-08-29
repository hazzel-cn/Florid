# Configuration about the project and the current platform
import sys

CONFIG = {
    'OS_type': '',
    'time:': '',
    'project_path': sys.path[0]
}

# Flag for some things
FLAG = {
    'producer_done': False,
    'scan_done': False
}

# A Quere handler to help manage urls
import core.checker

CHECKER_OBJ = core.checker.Checker()

# Modules
MODULE_NAME_LIST = []
MODULE_OBJ_DICT = {}
MODULE_ONE_NAME_LIST = []
MODILE_ONE_OBJ_DICT = {}

# Result Directory
RESULT_DICT = {}
RESULT_ONE_DICT = {}

# Alive Line
ALIVE_LINE = {}

# Source url
SOURCE_URL = ''
