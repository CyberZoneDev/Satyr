from flask import request, send_from_directory, render_template
import json
import requests
from datetime import datetime
from pytz import timezone

from . import app
from core import vk_config
from source.api import Vk
from source.database.methods import TokenMethods
from source.database.models import Token
from .utils import Reply


@app.route('/static/<path:path>', methods=['GET'])
def on_static(path):
    return send_from_directory('static', path)


@app.route('/subscribe', methods=['GET'])
def on_subscribe():
    code = request.args.get('code')

    if not code:
        return Reply.bad_request(error='Code must exists')

    access = json.loads(requests.get(
        f"https://oauth.vk.com/access_token?client_id={vk_config['callback']['app_id']}&client_secret={vk_config['callback']['secret_key']}&redirect_uri=https://icyftl.ru/subscribe&code=" + code).text)

    user = None

    try:
        vk = Vk(token=access)
        user = vk.who_am_i()
    except:
        return Reply.bad_request(error='Token was invalid')

    token_methods = TokenMethods()
    token = token_methods.get(user_id=user['id'])

    result = ''

    if token:
        token = token[0]
        token.content = access
        token.added_date = datetime.now(timezone('Europe/Moscow'))
        token_methods.update(token)
        result = 'Token was updated'
    else:
        token_methods.add(Token(content=access, user_id=user['id']))
        result = 'Token was added'

    return render_template('subscribe_done', result=result,
                           success_redirect_uri=vk_config['callback']['success_redirect_uri'])
