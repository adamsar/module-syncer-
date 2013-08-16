import os
import os.path
from clint.textui import colored
from webdav import WebdavClient
import logging

#Get rid of annoying webdav log messages
logging.getLogger("webdavLogger").handlers[0].level = logging.WARN

def valid_collection(directory, user, password):
    resource = WebdavClient.CollectionStorer(directory)
    resource.connection.addBasicAuthorization(user, password)
    return resource

def valid_resource(resource, user, password):
    resource = WebdavClient.ResourceStorer(resource)
    resource.connection.addBasicAuthorization(user, password)
    return resource


class WebdavSyncer(object):
    
    def __init__(self, endpoint, user, password):
        self.endpoint = endpoint
        self.user = user
        self.password = password

        
    def do_full_sync(self, directories=[]):
        pass

        
    def get_collection(self, d):
        return valid_collection(os.path.join(self.endpoint, d), self.user, self.password)

        
    def get_resource(self, f):
        return valid_resource(os.path.join(self.endpoint, f), self.user, self.password)

        
    def check_folder(self, d):
        folders = d.split("/")
        folder = ""
        for d in folders:
            folder = os.path.join(folder, d)
            collection = self.get_collection(d)
            try:
                collection.listResources()
            except:
                print "Adding %s" % colored.green(folder)
                collection = self.get_collection(os.path.dirname(d))
                collection.addCollection(d)
                
        
    def do_update(self, f, contents):
        if not f.startswith(".") and not f.endswith("~") and not f.endswith("#"):
            self.check_folder(os.path.dirname(f))
            resource = self.get_resource(f)
            print "Updating %s" % colored.green(f)
            resource.uploadContent(contents)
        
