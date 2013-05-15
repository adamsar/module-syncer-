import ConfigParser
from tools import monitors, observers
import sys
from time import sleep

if __name__ == "__main__":
    ini_file = sys.argv[1]
    parser = ConfigParser.RawConfigParser(allow_no_value=True)
    parser.readfp(open(ini_file))

    user = parser.get("mymenu", "username")
    password = parser.get("mymenu", "password")
    endpoints = parser.get("mymenu", "endpoints").split(",")
    folder = parser.get("mymenu", "folder")
    excludes = [d.strip() for d in parser.get("mymenu", "excludes").split(",")]

    watcher = monitors.FolderWatcher(folder, EXCLUDES=excludes)
    for endpoint in endpoints:
        watcher.add_observer(observers.WebdavSyncer(endpoint, user, password))
        
    while True:
        sleep(5)
        print "Checking"
        watcher.do_check()
