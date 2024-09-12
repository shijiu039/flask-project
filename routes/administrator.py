import random
import services.administrator as a
from flask import Blueprint, request, jsonify

from models.verifycode import VerifyCode
from services.image import new_image
from services.image import deleteImage as dele_image
from services.text import new_text
from services.text import deleteText as dele_text
from models.user import User
from models.text import Text
from models.image import Image
from tools.email_code import send_verification_email
from tools import md5
from werkzeug.utils import secure_filename
from config import app
import os
from services.user import verify_email
from datetime import datetime, timedelta
import services.dialogue as d

administrator = Blueprint('administrator', __name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
@administrator.route('login', methods=['POST'])
def login():
    data = request.form
    administrator_email = data['administrator_email']
    password=data['password']
    password1 = md5.md5(password)

    data = a.administrator_login(administrator_email, password1)
    return data

# 旧版管理员注册
# @administrator.route('register',methods=['POST'])
# def register():
#     data = request.form
#     administrator_name = data['administrator_name']
#     administrator_email = data['administrator_email']
#     v_code= data['v_code']
#     key=data['key']
#     password1=data['password1']
#     password2=data['password2']
#     if key != "aaaaaa":
#         return jsonify({
#             'code': -6,
#             'message': '激活码不一致',
#             'data': ''})
#     if password1 != password2:
#         return jsonify({
#             'code': -5,
#             'message': '密码不一致',
#             'data': ''})
#     if  v_code != verify_code:
#         return jsonify({
#             'code': -2,
#             'message': '验证码错误',
#             'data': ''})
#     password=md5.md5(password1)
#     return a.register(administrator_name,administrator_email,password)

# 新版管理员注册
@administrator.route('register',methods=['POST'])
def register():
    data = request.form
    administrator_name = data['administrator_name']
    email = data['administrator_email']
    code= data['v_code']
    key=data['key']
    password1=data['password1']
    password2=data['password2']
    if not email:
        return jsonify({
            'code': -7,
            'message': '请输入邮箱',
            'data': ''})
    if not administrator_name:
        return jsonify({
            'code': -8,
            'message': '请输入姓名',
            'data': ''})
    if not code:
        return jsonify({
            'code': -9,
            'message': '请输入验证码',
            'data': ''})
    if not key:
        return jsonify({
            'code': -10,
            'message': '请输入激活码',
            'data': ''})
    if not password1:
        return jsonify({
            'code': -11,
            'message': '请输入密码',
            'data': ''})
    if not password2:
        return jsonify({
            'code': -12,
            'message': '请重复输入密码',
            'data': ''})
    if key != "aaaaaa":
        return jsonify({
            'code': -6,
            'message': '激活码错误',
            'data': ''})
    if password1 != password2:
        return jsonify({
            'code': -5,
            'message': '密码不一致',
            'data': ''})
    # 查询数据库中的验证码
    verification_code = VerifyCode.query.filter_by(email=email).first()
    if verification_code and verification_code.code == code:
        # 检查验证码是否在有效期内
        if datetime.utcnow() - verification_code.timestamp < timedelta(minutes=5):
            # 验证成功后的逻辑，删除验证码，注册成功
            VerifyCode.deleteCode(verification_code)
            password = md5.md5(password1)
            return a.register(administrator_name, email, password)
        else:
            return jsonify({
                'code': -2,
                'message': '验证码无效',
                'data': ''})
    else:
        return jsonify({
            'code': -3,
            'message': '验证码错误',
            'data': ''})


# 新版管理员验证
@administrator.route('/verify', methods=['POST'])
def send_verification_code():
    email = request.form.get('email')
    if not verify_email(email):
        return jsonify({
            'code': -3,
            'message': '邮箱不合法',
            'data': ''
        })

    # 生成验证码
    code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=6))

    # 检查是否已经存在验证码记录，如果存在则更新，否则创建新记录
    verification_code = VerifyCode.query.filter_by(email=email).first()
    if verification_code:
        VerifyCode.updateCode(email, code)
    else:
        verification_code = VerifyCode(email=email, code=code)
        VerifyCode.add(verification_code)

    # 发送验证码
    try:
        send_verification_email(email, code)
        return jsonify({
            'code': 0,
            'message': '发送成功',
            'data': ''})
    except Exception as e:
        VerifyCode.rollback()
        return jsonify({
            'code': -2,
            'message': '发送失败',
            'data': ''})
@administrator.route('/userlist',methods=['POST'])
def userlist():
    return a.userlist()
@administrator.route('/addimage',methods=['POST'])
def addimage():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if new_image(file_path):
            return jsonify({
            'code': 0,
            'message': '上传成功',
            'data': ''})

    return jsonify({
            'code': -1,
            'message': '上传失败',
            'data': ''})
@administrator.route('/addtext',methods=['POST'])
def addtext():
    text = request.form.get('text')

    if new_text(text):
        return jsonify({
        'code': 0,
        'message': '上传成功',
        'data': ''})

    return jsonify({
            'code': -1,
            'message': '上传失败',
            'data': ''})

@administrator.route('/UserSearch',methods=['POST'])
def usersearch():
    data=request.form
    keyword=data.get('input_user')
    require_users=User.query.filter((User.user_name.like('%'+keyword+'%'))|(User.email.like('%'+keyword+'%'))|(User.user_id.like('%'+keyword+'%'))).with_entities(User.user_name,User.email,User.user_id).all()
    require_list = []
    for user in require_users:
        require_list.append({
            'user_name': user.user_name,
            'email': user.email,
            'user_id': user.user_id
        })

    return jsonify(require_list)
@administrator.route('/TextSearch',methods=['POST'])
def Textsearch():
    data=request.form
    keyword=data.get('input_text')
    require_texts=Text.query.filter((Text.text_info.like('%'+keyword+'%'))|(Text.id.like('%'+keyword+'%'))).with_entities(Text.text_info,Text.id).all()
    require_list = []
    for text in require_texts:
        require_list.append({
            'text_id': text.id,
            'text_info': text.text_info,
            # 'text_feature':text.text_feature
        })

    return jsonify(require_list)
@administrator.route('/textlist',methods=['POST'])
def textlist():
    all_texts = Text.query.with_entities(Text.id, Text.text_info).all()
    require_list = []
    for text in all_texts:
        require_list.append({
             'text_id': text.id,
            'text_info': text.text_info,
        })
    return jsonify({
            'code':0,
            'message': '获取成功',
            'data': require_list})

@administrator.route('/imagelist',methods=['POST'])
def imagelist():
    all_images = Image.query.with_entities(Image.image_id, Image.image_info).all()
    require_list = []
    for image in all_images:
        require_list.append({
            'image_id': image.image_id,
            'image_info': f"http://127.0.0.1:5000/{image.image_info}"
        })
    return jsonify({
            'code': 0,
            'message': '获取成功',
            'data': require_list})

@administrator.route('/deleteText',methods=['POST'])
def deleteText():
    # 从请求头中获取 text_id
    text_id = request.form.get('text_id')

    # 检查 text_id 是否为空
    if not text_id:
        return jsonify({
            'code': 1,
            'message': 'text_id 不能为空',
            'data': ''
        })
    # 查询并删除 Text 对象
    text_to_delete = Text.query.get(text_id)
    if not text_to_delete:
        return jsonify({
            'code': 2,
            'message': '没有找到指定 ID 的 Text 对象',
            'data': ''
        })
    return dele_text(text_to_delete)

@administrator.route('/deleteImage',methods=['POST'])
def deleteImage():
    # 从请求头中获取 image_id
    image_id = request.form.get('image_id')

    # 检查 image_id 是否为空
    if not image_id:
        return jsonify({
            'code': 1,
            'message': 'image_id 不能为空',
            'data': ''
        })
    # 查询并删除 Image 对象
    image_to_delete = Image.query.get(image_id)

    if not image_to_delete:
        return jsonify({
            'code': 2,
            'message': '没有找到指定 ID 的 Image 对象',
            'data': ''
        })

    # 获取文件路径
    file_path = os.path.abspath(image_to_delete.image_info)
    # 检查文件是否存在
    if os.path.exists(file_path):
        # 删除文件
        os.remove(file_path)
    else:
        return jsonify({
            'code': 3,
            'message': '文件不存在',
            'data': {
                'image_id': image_id
            }
        })
    return dele_image(image_to_delete)
@administrator.route('/deleteUser',methods=['POST'])
def deleteUser():
    # 从请求头中获取 user_id
    user_id = request.form.get('user_id')

    # 检查 image_id 是否为空
    if not user_id:
        return jsonify({
            'code': 1,
            'message': 'user_id 不能为空',
            'data': ''
        })
    # 查询并删除 Image 对象
    d.checkdialogue(user_id)
    user_to_delete = User.query.get(user_id)

    if not user_to_delete:
        return jsonify({
            'code': 2,
            'message': '没有找到指定 ID 的 User 对象',
            'data': ''
        })
    return dele_image(user_to_delete)
@administrator.route('/ImageSearch',methods=['POST'])
def imagesearch():
    data = request.form
    keyword = data.get('input_image')
    if not keyword:
        return jsonify({
            "code": -1,
            "message": "Keyword is required",
            "data": ''
        })
    image_to_return = Image.query.filter_by(image_id= keyword).first()
    require_list=[]
    require_list.append({
        'image_id': image_to_return.image_id,
        'image_info': f"http://127.0.0.1:5000/{image_to_return.image_info}"
    })
    if image_to_return:
        return jsonify({
                "code": 0,
                "message": "获取图片",
                "data": require_list
            })
    return jsonify({
                "code": -2,
                "message": "无法获取图片",
                "data": ''
            })