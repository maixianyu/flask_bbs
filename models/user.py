import hashlib

from sqlalchemy import Column, String, Enum

import config
# import secret
from models.base_model import SQLMixin, db
from .user_role import UserRole


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False, default='/images/3.jpg')
    # email = Column(String(50), nullable=False, default=config.test_mail)
    email = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = hashlib.sha256((password + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        print('register', form)
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            form['role'] = UserRole.normal
            u = User.new(form)
            return u
        else:
            return None

    @staticmethod
    def guest():
        form = dict()
        form['username'] = '游客'
        form['role'] = UserRole.normal
        form['image'] = '/images/3.jpg'
        u = __class__()
        for k, v in form.items():
            setattr(u, k, v)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
