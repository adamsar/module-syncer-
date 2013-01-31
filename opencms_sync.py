# -*- coding: utf-8 -*-
import templates
import sys
import os
import os.path
import subprocess

EXCLUDES = ["classes", "conf", "oclibs", "lib"]
SUBS = {"bin": "classes"}
TEMP_FILE = "sync.xml"

def get_all_dirs(directory, parent=""):
    """
    Utility to get all directories recursively in a file system
    """
    directories = []
    directory = os.path.join(parent, directory)

    try:
        for d in os.listdir(directory):
            if d in EXCLUDES or d.startswith("."):
                continue
            d = os.path.join(directory, d)
            if os.path.isdir(d):
                directories.append(d)
                directories = directories + get_all_dirs(d)
    except OSError, aeError:
        pass

    return directories


#自動的にOpenCmsに繋がってデータやり取りできる。
class Syncer(object):

    def __init__(self, user, password, module, endpoint, directory):
        #パラメータを設定する
        self.user = user
        self.password = password
        self.module = module
        self.endpoint = endpoint
        self.directory = directory
        self.file_name = ""

    def generate_ant_script(self):
        template_data = {
            "current":  os.path.dirname(os.path.abspath(__file__)),
            "user": self.user,
            "password": self.password,
            "module": self.module,
            "endpoint": self.endpoint
            }

        directories = get_all_dirs(self.directory)
        transfers = []
        for d in directories:
            d = d.replace(self.directory, "")
            if d in SUBS:
                transfers.append(templates.entry_base % {"url": d, "directory": SUBS[d]})
            else:
                transfers.append(templates.entry_base % {"url": d, "directory": d})

        template_data["transfers"] = "\n".join(transfers)

        #データを書き込む
        self.file_name = os.path.join(self.directory, TEMP_FILE)
        handle = open(self.file_name, "w")
        handle.write(templates.script_base % template_data)
        handle.close()


    def execute(self):
        subprocess.call(["ant", "-buildfile", self.file_name])


if __name__ == "__main__":
    syncer = Syncer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    syncer.generate_ant_script()
    syncer.execute()
