import json
from os import environ
from source.utils.version import Version

if not environ.get('S_T_K'):
    raise Exception('S_T_K is not set')

S_T_K = environ['S_T_K']
del environ['S_T_K']

config = json.load(open('config.json', 'r', encoding='UTF-8'))

db_config = config['database']
vk_config = config['vk']
rest_config = config['rest']
log_config = config['logging']
engine_config = config['engine']
version_raw = json.load(open('version.json', 'r', encoding='UTF-8'))
VERSION = Version.from_string(version_raw['version'])
