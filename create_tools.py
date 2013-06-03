import os
import os.path
EXCLUDES = []

def get_all_dirs(directory, parent_folder=""):
    """
    Utility to get all directories recursively in a file system
    """
    directories = []

    try:
        base_folder = os.path.join(parent_folder, directory)
        for d in os.listdir(base_folder):
            if d in EXCLUDES or d.startswith("."):
                continue
            d = os.path.join(directory, d)
            full_dir = os.path.join(parent_folder, d)
            if os.path.isdir(full_dir):
                directories.append(d)
                directories = directories + get_all_dirs(d, parent_folder=parent_folder)
    except OSError, aeError:
        print "Error"

    return directories
