import os
import uuid

from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
    render_template,
)

from models.user import User
from routes import current_user
from models.message import send_mail
from utils import log
import config

main = Blueprint('reset', __name__)

"""
用于重置
"""

token_uid = dict()


def send_mail_reset_password(u):
    # 设置 token 和 uid 的对应关系
    token = str(uuid.uuid4())
    token_uid[token] = u.id

    # 发送邮件到用户的邮箱
    subject = '密码重置'
    author = config.admin_mail
    to = u.email
    content = 'http://www.blackjude.club/reset/view?token={}'.format(token)
    send_mail(subject, author, to, content)


@main.route("/send", methods=['POST'])
def send():
    username = request.form['username']
    u = User.one(username=username)

    if u is None:
        msg = '用户名不存在'
    else:
        msg = '密码重置邮件已发送成功，请查收'
        send_mail_reset_password(u)

    return redirect(url_for('index.index', message=msg))


@main.route("/view")
def view():
    token = request.args.get('token', None)
    uid = token_uid.get(token, None)
    if token is None or uid is None:
        log('token_uid', token_uid)
        msg = 'token不存在'
        return redirect(url_for('index.index', message=msg))
    else:
        msg = ''
        return render_template("reset_view.html", message=msg, token=token)


def update_password(token, password):
    uid = token_uid[token]
    u = User.one(id=uid)
    password_salt = User.salted_password(password)
    User.update(u.id, password=password_salt)

    # 清除token
    del token_uid[token]


@main.route("/update", methods=['POST'])
def update():
    token = request.args.get('token', None)
    password = request.form.get('password', None)

    if token is not None and token in token_uid and password is not None:
        update_password(token, password)
        msg = '密码重置成功，请登录'
    else:
        msg = 'token不存在，更新密码失败，请重新尝试'

    return redirect(url_for('index.index', message=msg))
