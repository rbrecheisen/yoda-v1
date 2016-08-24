import os
import pytest


def init_env():
    port = 5000
    for service in ['AUTH', 'COMPUTE', 'STORAGE', 'FILE']:
        if os.getenv('{}_SERVICE_HOST'.format(service), None) is None:
            os.environ['{}_SERVICE_HOST'.format(service)] = '0.0.0.0'
            os.environ['{}_SERVICE_PORT'.format(service)] = str(port)
            port += 1
    if os.getenv('DATA_DIR', None) is None:
        os.environ['DATA_DIR'] = '/Users/Ralph/download'


if __name__ == '__main__':

    init_env()

    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main('. -s -p no:cacheprovider')
