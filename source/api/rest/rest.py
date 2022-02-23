import requests
from flask import request, send_from_directory, render_template, redirect
from datetime import datetime
from pytz import timezone
from urllib.parse import quote

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
    return render_template('subscribe.html', app_id=vk_config['callback']['app_id'],
                           prefix=vk_config['callback']['redirect_prefix'])


@app.route('/auth', methods=['GET'])
def on_auth():
    client_id = vk_config['callback']['app_id']
    display = 'page'
    redirect_uri = quote(vk_config['callback']['unsub_redirect_uri'], safe='')
    scope = '0'
    response_type = 'code'
    v = '5.131'

    return redirect(
        f'https://oauth.vk.com/authorize?client_id={client_id}&display={display}&redirect_uri={redirect_uri}&scope={scope}&response_type={response_type}&v={v}')


@app.route('/unsubscribe', methods=['GET'])
def on_unsubscribe():
    prefix = vk_config['callback']['redirect_prefix']

    if not request.args.get('code'):
        return render_template('unsubscribe.html',
                               unsub_redirect_url=prefix + '/auth',
                               deny_redirect_url=vk_config['callback']['sub_success_redirect_uri'])

    client_id = vk_config['callback']['app_id']
    secret = vk_config['callback']['secret_key']
    redirect_uri = quote(vk_config['callback']['unsub_redirect_uri'], safe='')
    code = request.args['code']

    r = requests.get(
        f'https://oauth.vk.com/access_token?client_id={client_id}&client_secret={secret}&redirect_uri={redirect_uri}&code={code}')
    user_id = r.json().get('user_id')

    if not user_id:
        return Reply.with_code(500, False, error='Something went wrong')

    token_methods = TokenMethods()
    token = token_methods.get(user_id=user_id)

    if not token:
        return Reply.failed_dependency(error='I do not have ur token')

    token_methods.delete(token[0])

    return redirect(prefix + '/unsubscribe_done')


@app.route('/unsubscribe_done', methods=['GET'])
def on_unsubscribe_done():
    return render_template('subscribe_done.html',
                           success_redirect_uri=vk_config['callback']['sub_success_redirect_uri'],
                           prefix=vk_config['callback']['redirect_prefix'])


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
                           success_redirect_uri=vk_config['callback']['sub_success_redirect_uri'],
                           prefix=vk_config['callback']['redirect_prefix'])
