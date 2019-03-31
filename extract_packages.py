import sys
import re
import argparse


def extract_packages():
    # Extract used packages in python file using import and from * import clauses.
    import_pattern = r'^import ([\w]+)[\W]*'
    from_pattern = r'^from ([\w]+)[\W]*'

    def extract_pattern(pat, s):
        m = re.match(pat, s)
        if m:
            print(m.group(1))

    for line in sys.stdin:
        extract_pattern(import_pattern, line)
        extract_pattern(from_pattern, line)


def read_lines(p):
    with open(p, encoding='utf8') as f:
        return [line.rstrip('\n') for line in f.readlines()]


def match(used_path, pip_path):
    # Extract package versions from pip generated files and packages extracted in extract_packages function.
    used = read_lines(used_path)
    used = list(set(used))  # unique packages

    pips = read_lines(pip_path)
    pips = dict(map(lambda x: x.split(), pips))

    found = []
    missed = []

    for p in used:
        if p in pips:
            found.append(p)
        else:
            missed.append(p)

    print('Missed packages:')
    print('\n'.join(missed))
    print('Found packages:')
    for p in found:
        print('{}=={}'.format(p, pips[p]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--extract', action='store_true', help='Extract package names from python files.')
    parser.add_argument('-m', '--match', action='store_true',
                        help='Match packages names with system packages showed by pip.')
    parser.add_argument('-u', '--used', type=str, help='File path of used package names.')
    parser.add_argument('-p', '--pip', type=str, help='File path of system packages showed by pip.')
    args = parser.parse_args()

    if args.extract:
        extract_packages()

    elif args.match:
        match(args.used, args.pip)
