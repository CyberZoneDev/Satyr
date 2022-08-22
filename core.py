import json
import logging
from os import environ
from source.utils.version import Version

if not environ.get('S_T_K'):
    raise Exception('S_T_K is not set')

config = json.load(open('config.json', 'r', encoding='UTF-8'))

db_config = config['database']
vk_config = config['vk']
rest_config = config['rest']
log_config = config['logging']
version_raw = json.load(open('version.json', 'r', encoding='UTF-8'))
VERSION = Version.from_string(version_raw['version'])

logging.basicConfig(filename=log_config['path'], level=logging.INFO,
                    format='%(asctime)-15s | [%(name)s] %(levelname)s => %(message)s')
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
