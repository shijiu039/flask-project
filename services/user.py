import socket

from flask_login import login_user

from models.user import User
from flask import jsonify

def user_login(email,v_code):
    u = User.query.filter_by(email=email).first()
    if u:
        return jsonify({
                'code': 0,
                "message": "登录成功",
                "data": u.to_dict()
            })
    else:
        return jsonify({
            'code': -5,
            "message": "用户不存在",
            "data": ''
        })

def verify_email(email):
    domain = email.split('@')[-1]
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False


def register(user_name,email,img_path):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            'code': -3,
            'message': '用户已存在',
            'data': ''})
        # Verify code
    if not verify_email(email):
        return jsonify({
            'code': -1,
            'message': '邮箱不合法',
            'data': ''})
        # Create new user
    new_user = User(user_name=user_name, email=email, img_path=img_path)
    if User.register(new_user):
        return jsonify({
            'code': 0,
            'message': '注册成功',
            'data': new_user.to_dict()})
def user_info(user_id):
    user=User.query.filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({
        'code': -1,
        'message': '用户不存在',
        'data': ''
    })
    return jsonify({
        'code': 0,
        'message': '获取成功',
        'data':user.to_dict()
    })

def update_username(user_id, new_username):
    user=User.update_username(user_id,new_username)
    return jsonify({
    'code': 0,
    'message': '更新成功',
    'data':user.to_dict()})

def update_img(user_id,file_path):
    user=User.update_img(user_id,file_path)
    return user

def deleteUser(user_to_delete):
    if User.deleteUser(user_to_delete):
        return jsonify({
                'code': 0,
                'message': '删除成功',
                'data': ''
            })
    else:
        return jsonify({
                'code': 3,
                'message': '删除失败',
                'data': ''
            })
def satisfactionSet(user_id, new_satisfaction):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        user = User.satisfacationSet(user, new_satisfaction)
        return jsonify({
            'code': 0,
            'message': '修改成功',
            'data':user.to_dict()
            })
    else:
        return jsonify({
            'code': -1,
            'message': '获取失败',
            'data': ''
            })


