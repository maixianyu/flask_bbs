import uuid
from functools import wraps

from flask import (
    request,
    abort,
    redirect,
    url_for,
)

from models.user import User
import redis
import json

# 初始化 redis
cache_csrf = redis.StrictRedis()
# 初始化 session_redis
cache_session = redis.StrictRedis(db=1)


def current_user():
    # uid = session.get('user_id', '')
    s = request.cookies.get('session')
    # 从 redis 中找 u.id
    if s is not None and cache_session.exists(s):
        uid = cache_session.get(s)
        uid = json.loads(uid)
        u = User.one(id=uid)
        return u
    else:
        return User.guest()


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        # v = None

        if u.is_guest():
            return redirect(url_for('.index', message='请登录'))
        elif cache_csrf.exists(token)\
                and json.loads(cache_csrf.get(token)) == u.id:
            cache_csrf.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)
            # resp = 'token={}, v={} ({}), uid={}'.format(
            #     token, v, type(v), u.id)
            # abort(Response(resp))

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    # csrf_tokens[token] = u.id
    v = json.dumps(u.id)
    cache_csrf.set(token, v)
    return token
