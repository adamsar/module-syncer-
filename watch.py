#Python 3 imports and what not
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
from tools import monitors, observers
import sys
from time import sleep

if __name__ == "__main__":
    section, ini_file = sys.argv[1], sys.argv[2]
    parser = ConfigParser.RawConfigParser(allow_no_value=True)
    parser.readfp(open(ini_file))

    user = parser.get(section, "username")
    password = parser.get(section, "password")
    endpoint = parser.get(section, "endpoint")
    folder = parser.get(section, "folder")
    excludes = [
        d.strip() for d in parser.get(section, "excludes").split(",")
    ]

    watcher = monitors.FolderWatcher(folder, EXCLUDES=excludes)
    watcher.add_observer(observers.WebdavSyncer(endpoint, user, password))
        
    while True:
        sleep(5)
        watcher.do_check()
