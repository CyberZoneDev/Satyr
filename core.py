import json

config = json.load(open('config.json', 'r', encoding='UTF-8'))

db_config = config['database']
vk_config = config['vk']
rest_config = config['rest']
