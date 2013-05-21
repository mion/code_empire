#!/usr/bin/env python
import sys

def runtests(args=None):
    import pytest

    if not args:
        args = []

    if not any(a for a in args[1:] if not a.startswith('-')):
        args.append('tests')

    print "ARGS: {}".format(args)

    ret = pytest.main(args)
    sys.exit(ret)

if __name__ == '__main__':
    runtests(sys.argv)
