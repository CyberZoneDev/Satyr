from source.handlers import GroupsWatchDog
from source.api.rest import *
from core import rest_config

gwd = GroupsWatchDog()
gwd.start()

app.run(**rest_config, debug=True)
