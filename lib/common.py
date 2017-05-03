# coding=utf-8
# Some common configuration information here
# Sharing things here
import platform
import Queue
import sys
import lib.urlentity


# The URL to be checked
SOURCE_URL = ''

# The type of OS which the scripts are being exacuted on
OS = 'WIN' if platform.system() == 'Windows' else "NIX"

# The absolute address of the main script - florid.py
PROJECT_PATH = sys.path[0]

# The queue of all urls to be checked
URL_QUEUE = Queue.Queue()

# The queue of url which on identify an address
PATH_QUEUE = Queue.Queue()

# The set of path
PATH_SET = []

# The set of objects of imported mudiles for phase1
MODULE_OBJ_SET_PRE = []

# The set of name of imported modules for phase1
MODULE_NAME_SET_PRE = []

# The set of objects of imported modules from 'mod'
MODULE_OBJ_SET = []

# The set of name of imported modules from 'mod'
MODULE_NAME_SET = []

# The directory
MODULE_DIRECTORY = {}

# The directory of an args from command line
COMMAND_SET = {
    'module_list': []
}

# The count of urls to be checked
URL_COUNT = 0

# The sharing directory which provides each module with the ability of requesting for data in other modules.
SHARING_DICTIONARY = {
    # '$module_info': SOMETHING',
}

# The directory of result of the check modules
RESULT_DIRECROTY = {
    # '$module_result': []
}

# The directory to count the number of done task for each module
CHECKED_COUNT = {

}

# Current URL
CURRENT_URL = ''

# All done count
ALL_DOWN_COUNT = 0

# The flag to identify whether the work of spider has done
SPIDER_DONE_FLAG = False

# The flag to identify whether the scan work has finished
SCAN_DONE_FLAG = False