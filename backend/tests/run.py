import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.curdir, 'backend'))
from lib.util import init_env


if __name__ == '__main__':

    init_env()

    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main('. -s -p no:cacheprovider')
