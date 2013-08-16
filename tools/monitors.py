import os
import os.path

def get_files(directory, parent_folder="", EXCLUDES = [], STARTING_FOLDER="/"):
    """
    Grabs all files not in EXCLUDES
    """
    files = []    
    try:
        base_folder = os.path.join(parent_folder, directory)
        for f in os.listdir(base_folder):
            if f.startswith(".") or f.endswith("~") or f.endswith("#"):
                continue
            f = os.path.join(directory, f)
            full_path = os.path.join(parent_folder, f)
            if full_path.replace(STARTING_FOLDER, "") in EXCLUDES:
                continue            
            if os.path.isdir(full_path):
                files += get_files(f,
                                   parent_folder=parent_folder,
                                   EXCLUDES=EXCLUDES,
                                   STARTING_FOLDER=STARTING_FOLDER)
            else:
                files.append(f)
    except OSError, aeError:
        print "Error"
    return files
        
class FolderWatcher(object):

    def _full_file(self, f):
        """
        Returns the full file path for file f
        """
        return os.path.join(self.directory, f)

    def __init__(self, directory, EXCLUDES = []):
        self.directory = directory
        if not self.directory.endswith("/"):
            self.directory += "/"

        self.observers = []            
        self.EXCLUDES = EXCLUDES
        
        self.file_map = dict(
            (f, os.path.getmtime(self._full_file(f)))
            for f in get_files("", self.directory, self.EXCLUDES, self.directory)
        )
        

    def do_check(self):
        for f in get_files("", self.directory, self.EXCLUDES, self.directory):
            time = os.path.getmtime(self._full_file(f))
            if f not in self.file_map or self.file_map[f] < time:
                self.file_map[f] = time
                self.notify_observers(f)

                
    def add_observer(self, observer):
        self.observers.append(observer)

        
    def remove_observer(self, observer):
        self.observers.remove(observer)

        
    def notify_observers(self, f):
        for observer in self.observers:
            observer.do_update(f, open(self._full_file(f), "rb").read())
