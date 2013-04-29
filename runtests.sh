# Don't try running the tests directly or else it'll fail
# (you'd need to correctly setup the sys.path)
#
# USAGE
# To run tests/creature.py:
#   $ ./test.sh creature

if [[ $# = 1 ]]; then
    if [[ -f tests/$1.py ]]; then
        python -m tests.$1
    else
        echo "ERROR: cannot find module 'tests/$1.py'"
    fi
else
    echo "USAGE: runtest.sh <test_module>"
fi