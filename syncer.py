import cli.app
import ConfigParser
import datetime
import logging
import os
import os.path
from time import mktime
from lib import create_tools
from lib import webdav_tools

my_logger = logging.getLogger("webdavLogger")
if len(my_logger.handlers) == 0:
    my_logger.level = logging.WARN
    formatter = logging.Formatter(_fileLogFormat)
    if handler is None:
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setFormatter(formatter)
        my_logger.addHandler(stdoutHandler)
    else:
        my_logger.addHandler(handler)
else:
    my_logger.handlers[0].level = logging.WARN

@cli.app.CommandLineApp
def sync(app):
    parser = ConfigParser.RawConfigParser(allow_no_value=True)
    parser.readfp(open(app.params.config))

    user = parser.get(app.params.app, "username").strip()
    password = parser.get(app.params.app, "password").strip()
    endpoint = parser.get(app.params.app, "endpoint")
    folder = parser.get(app.params.app, "folder")
    create_tools.EXCLUDES = [d.strip() for d in parser.get(app.params.app, "excludes").split(",")]

    directories = create_tools.get_all_dirs("", parent_folder=folder)

    for directory in directories:
        server_dir = os.path.join(endpoint, directory)
        print "Processing %s..." % server_dir
        resource = webdav_tools.valid_collection(os.path.dirname(server_dir), user, password)
        try:
            resource.listResources()
        except webdav.Connection.WebdavError, e:
            if "Not Found" not in str(e):
                raise e
            resource = webdav_tools.valid_collection(os.path.dirname(server_dir), user, password)
            resource.addCollection(os.path.basename(server_dir))

        resource = webdav_tools.valid_collection(server_dir, user, password)
        server_files = dict((os.path.basename(key), value) for key, value in resource.listResources().iteritems())
        directory = os.path.join(folder, directory)
        for f in os.listdir(directory):
            system_file = os.path.join(directory, f)

            if not os.path.isdir(system_file):
                if f not in server_files:
                    if not f.startswith(".") and not f.endswith("~") and not f.endswith("#"):
                        print "Creating %s" % f
                        new_resource = resource.addResource(f)
                        new_resource.uploadFile(open(system_file, "rb"))
                else:
                    if server_files[f].getContentLength() not in [os.path.getsize(system_file) + 3, os.path.getsize(system_file)]:
                        print "Updating %s" % f
                        existing_resource = webdav_tools.valid_resource(os.path.join(server_dir, f), user, password)
                        existing_resource.uploadContent(open(system_file, "rb").read())



sync.add_param("app", help="Configured app to sync to to")
sync.add_param("config", help="The configuration file with syncs defined")

if __name__ == "__main__":
    sync.run()
