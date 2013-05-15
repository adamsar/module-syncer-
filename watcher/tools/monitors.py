import os
import time
import os.path

def get_files(directory, parent_folder="", EXCLUDES = []):
    files = []
    base = os.path.join(parent_folder, directory)
    for d in os.listdir(base):
        full_path = os.path.join(directory, d)
        if full_path in EXCLUDES:
            continue
        if os.path.isdir(os.path.join(parent_folder, full_path)):
            files += get_files(full_path, parent_folder, EXCLUDES)
        elif not d.startswith(".") and not d.endswith("~") and not d.endswith("#"):
            files.append(os.path.join(os.path.join(parent_folder, directory), d))
    return files
    
        
class FolderWatcher(object):

    def __init__(self, directory, EXCLUDES = []):
        self.directory = directory
        if not self.directory.endswith("/"):
            self.directory += "/"

        self.observers = []            
        self.EXCLUDES = EXCLUDES
        
        self.file_map = dict((f, os.path.getmtime(f)) for f in get_files("", self.directory, self.EXCLUDES))
        

    def do_check(self):
        for f in get_files("", self.directory, self.EXCLUDES):
            if f not in self.file_map or self.file_map[f] != os.path.getmtime(f):
                self.file_map[f] = os.path.getmtime(f)
                self.notify_observers(f)

                
    def add_observer(self, observer):
        self.observers.append(observer)

        
    def remove_observer(self, observer):
        self.observers.remove(observer)

        
    def notify_observers(self, f):
        print "Notifying for %s" % f
        for observer in self.observers:
            observer.do_update(f.replace(self.directory, ""), open(f, "rb").read())
