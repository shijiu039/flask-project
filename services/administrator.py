import socket
from models.user import User
from models.administrator import Administrator
from flask import jsonify

def administrator_login(administrator_email,password):
    a = Administrator.query.filter_by(administrator_email=administrator_email).first()
    if not verify_email(administrator_email):
        return jsonify({
            'code': -3,
            'message': '邮箱不合法',
            'data': ''})
    if a is None:
        # 用户不存在
        return jsonify({
            'code': -1,
            "message": "管理员不存在",
            "data":""
        })
    if password != a.password:
        return jsonify({
            'code': -6,
            "message": "密码错误",
            "data": ""
        })
    return jsonify({
            'code': 0,
            "message": "登录成功",
            "data": a.to_dict()
        })

def verify_email(email):
    domain = email.split('@')[-1]
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False


def register(administrator_name,administrator_email,password):
    existing_administrator = Administrator.query.filter_by(administrator_email=administrator_email).first()
    if existing_administrator:
        return jsonify({
            'code': -3,
            'message': '管理员已存在',
            'data': ''})
        # Verify code
    if not verify_email(administrator_email):
        return jsonify({
            'code': -1,
            'message': '邮箱不合法',
            'data': ''})
        # Create new user
    new_administrator = Administrator(administrator_name=administrator_name, administrator_email=administrator_email,password=password)
    if Administrator.register(new_administrator):
        return jsonify({
            'code': 0,
            'message': '注册成功',
            'data': ''})

def userlist():
    return jsonify({
                'code': 0,
                'message': '注册成功',
                'data':  [user.to_dict() for user in User.query.all()]})



