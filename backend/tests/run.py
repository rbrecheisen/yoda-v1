import pytest


if __name__ == '__main__':
    # The '-p no:cacheprovider' option prevents .cache directory which clutters
    # the source code and only serves for speed ups if you have large quantities
    # of test cases
    pytest.main('. -s -p no:cacheprovider')
