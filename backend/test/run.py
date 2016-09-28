import os
import sys
sys.path.insert(0, os.path.join(os.curdir, 'backend'))
import pytest


if __name__ == '__main__':

    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large numbers
    # of test cases
    pytest.main('. -s -p no:cacheprovider')
