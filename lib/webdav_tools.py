from webdav import WebdavClient

def valid_collection(directory, user, password):
    resource = WebdavClient.CollectionStorer(directory)
    resource.connection.addBasicAuthorization(user, password)
    return resource


def valid_resource(resource, user, password):
    resource = WebdavClient.ResourceStorer(resource)
    resource.connection.addBasicAuthorization(user, password)
    return resource
