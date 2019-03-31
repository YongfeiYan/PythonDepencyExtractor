USED_PKS='/tmp/packages_used.txt'
ALL_PKS='/tmp/pip_packages.txt'
# Extract all used packages in python files.
cat *.py */*.py | python extract_packages.py -e > $USED_PKS
# List all packages installed via pip(NB: not all packages are listed. SAD.).
pip list > $ALL_PKS
# Match the above two files
python extract_packages.py -m -u $USED_PKS -p $ALL_PKS

