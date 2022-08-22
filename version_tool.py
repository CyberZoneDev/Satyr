from sys import argv
from core import VERSION
import json
from datetime import datetime

if len(argv) == 1:
    print('Usage: -ma X -mi X -b X -r a|b -ma++ -mi++ -b++')
    exit(0)

major = None
minor = None
build = None
beta = None
alpha = None

version = VERSION

argv = argv[1:]

for i, val in enumerate(argv):
    if val == '-ma':
        major = argv[i + 1]
    elif val == '-mi':
        minor = argv[i + 1]
    elif val == '-b':
        build = argv[i + 1]
    elif val == '-t':
        ab = argv[i + 1].lower().strip()
        if ab == 'a':
            alpha = True
        elif ab == 'b':
            beta = True
        else:
            raise ValueError('Invalid -t parameter')
    elif val == '-ma++':
        major = version.major + 1
    elif val == '-mi++':
        minor = version.minor + 1
    elif val == '-b++':
        build = version.build + 1
    else:
        if val.isdecimal():
            continue
        raise ValueError(f'Unknown parameter {val}')

if major:
    version.major = int(major)

if minor:
    version.minor = int(minor)

if build:
    version.build = int(build)

if alpha is not None:
    version.alpha = alpha
    if alpha:
        version.beta = False

if beta is not None:
    version.beta = beta
    if beta:
        version.alpha = False

with open('version.json', 'w', encoding='UTF-8') as f:
    f.write(json.dumps({
        'version': str(version),
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'inherit': True
    }))
