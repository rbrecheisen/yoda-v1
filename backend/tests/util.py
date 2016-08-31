import os


# --------------------------------------------------------------------------------------------------------------------
def uri(service, path=''):
    if path.startswith(os.path.sep):
        path = path[1:]
    return 'http://{}:{}/{}'.format(
        os.getenv('{}_SERVICE_HOST'.format(service.upper())),
        os.getenv('{}_SERVICE_PORT'.format(service.upper())), path)
