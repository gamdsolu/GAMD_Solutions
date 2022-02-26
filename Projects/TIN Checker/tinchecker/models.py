from flask import Flask
from tinchecker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))

class Admins(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email_add = db.Column(db.String(length=1024), nullable=False)
    fullname = db.Column(db.String(length=100), nullable=False)
    job = db.Column(db.String(length=100), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    profile_img = db.Column(db.String(length=1024), nullable=False)

    def check_password_correction(self, attempted_password):
        return self.password_hash == attempted_password

class Users(db.Model):
    __tablename__='users_detail'
    id = db.Column(db.Integer, primary_key=True)
    tin_num=db.Column(db.String(200))
    userIP=db.Column(db.String(200))
    deviceInfo=db.Column(db.String(200))
    browserInfo=db.Column(db.String(200))
    dateTime=db.Column(db.String(200))

    def __init__(self, tin_num, userIP, deviceInfo, browserInfo, dateTime):
        self.tin_num=tin_num
        self.userIP=userIP
        self.deviceInfo=deviceInfo
        self.browserInfo=browserInfo
        self.dateTime=dateTime

        