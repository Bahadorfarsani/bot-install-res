
import time
from datetime import datetime
import subprocess
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = db.create_engine("mysql://armin:T101vb$!GuYX@ub.pxnet.de/telegram_bot", echo=True)
connection = engine.connect()
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Admin(Base):
    __tablename__ = 'admins'
    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(256))

class User(Base):
    __tablename__ = 'users'
    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(256))
    creator = db.Column(db.ForeignKey(Admin.username, ondelete='CASCADE'))


class Account(Base):
    __tablename__ = 'accounts'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(256))
    host = db.Column(db.String)
    creator = db.Column(db.ForeignKey(User.username, ondelete='CASCADE'))
    created_date = db.Column(db.Date)
    created_time = db.Column(db.Time)
    expiration = db.Column(db.Date)
    month = db.Column(db.Integer)

def set_password(username, password):
    p = subprocess.Popen(["/usr/sbin/chpasswd"], universal_newlines=True, shell=False, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate(username + ":" + password + "\n")
    assert p.wait() == 0
    if stdout or stderr:
        raise Exception("Error encountered changing the password!")

session = Session()
accounts = session.query(Account).filter_by(host="ze.pxnet.de").all()

for account in accounts:
    subprocess.run(['useradd', account.username, '--shell=/bin/false', "--no-create-home", "-e", str(account.expiration)])
    set_password(account.username, account.password)
    print("User created - user: {} , pass: {}".format(account.username,account.password))











