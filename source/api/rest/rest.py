from flask import request, send_from_directory, render_template
from datetime import datetime
from pytz import timezone

from . import app
from core import vk_config
from source.api import Vk
from source.database.methods import TokenMethods, UserMethods
from source.database.models import Token, User
from .utils import Reply


@app.route('/static/<path:path>', methods=['GET'])
def on_static(path):
    return send_from_directory('static', path)


@app.route('/subscribe', methods=['GET'])
def on_subscribe_get():
    return render_template('subscribe.html', app_id=vk_config['callback']['app_id'])


@app.route('/subscribe', methods=['POST'])
def on_subscribe_post():
    access = request.json.get('access')
    if not access:
        return Reply.bad_request(error='Token was empty')

    try:
        vk = Vk(token=access)
        user = vk.who_am_i()
    except Exception as e:
        return Reply.bad_request(error='Token was invalid')

    token_methods = TokenMethods()
    user_methods = UserMethods(session=token_methods.session)
    token = token_methods.get(user_id=user['id'])

    result = ''

    if token:
        token = token[0]
        token.content = access
        token.added_date = datetime.now(timezone('Europe/Moscow'))
        token_methods.update(token)
        result = 'Токен был обновлен'
    else:
        if not user_methods.get(id=user['id']):
            user_methods.add(User(user['id']))

        token_methods.add(Token(content=access, user_id=user['id']))
        result = 'Токен был добавлен'

    return Reply.ok(result=result)


@app.route('/subscribe_done', methods=['GET'])
def on_subscribe_done():
    result = request.args.get('result', '')
    return render_template('subscribe_done.html', result=result,
                           success_redirect_uri=vk_config['callback']['success_redirect_uri'])

