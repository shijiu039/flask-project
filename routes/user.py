import os
import random

from werkzeug.utils import secure_filename

from config import app
from models.verifycode import VerifyCode
from datetime import datetime, timedelta

from services.user import verify_email
from flask import Blueprint, request, jsonify
from services.user import user_login
import services.user as u
from tools.clip_model import getText
from tools.clip_model import getImage

user = Blueprint('user', __name__)
from tools.email_code import send_verification_email
from services.dialogue import create_dialogue
import services.dialogue as d
import base64
import services.history as h
from models.dialogue import Dialogue

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



# 新版登录
@user.route('/login', methods=['POST'])
def verify_code():
    email = request.form.get('user_email')
    code = request.form.get('v_code')
    if not email:
        return jsonify({
            'code': -1,
            'message': '请输入邮箱',
            'data': ''})
    if not code:
        return jsonify({
            'code': -4,
            'message': '请输入验证码',
            'data': ''})
    # 查询数据库中的验证码
    verification_code = VerifyCode.query.filter_by(email=email).first()
    if verification_code and verification_code.code == code:
        # 检查验证码是否在有效期内
        if datetime.utcnow() - verification_code.timestamp < timedelta(minutes=5):
            # 验证成功后的逻辑，删除验证码
            # VerifyCode.deleteCode(verification_code)
            data = user_login(email, code)
            return data

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

@user.route('/register',methods=['POST'])
def register():
    data = request.form
    user_name = data['user_name']
    email = data['user_email']
    v_code= data['v_code']
    if not user_name:
        return jsonify({
            'code': -3,
            'message': '请输入用户名',
            'data': ''})
    if not email:
        return jsonify({
            'code': -4,
            'message': '请输入邮箱',
            'data': ''})
    if not v_code:
        return jsonify({
            'code': -5,
            'message': '请输入验证码',
            'data': ''})
    # 查询数据库中的验证码
    verification_code = VerifyCode.query.filter_by(email=email).first()
    if verification_code and verification_code.code == v_code:
        # 检查验证码是否在有效期内
        if datetime.utcnow() - verification_code.timestamp < timedelta(minutes=5):
            # 验证成功后的逻辑，删除验证码
            VerifyCode.deleteCode(verification_code)
            img_path = 'flickr30k-images/logo.png'
            return u.register(user_name, email, img_path)
        else:
            return jsonify({
                'code': -2,
                'message': '验证码无效',
                'data': ''})
    else:
        return jsonify({
            'code': -6,
            'message': '验证码错误',
            'data': ''})


# 新版发送验证码
@user.route('/verify', methods=['POST'])
def send_verification_code():
    email = request.form.get('user_email')
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
@user.route('/user_info',methods=['POST'])
def user_info():
    user_id = request.form.get('user_id')
    return u.user_info(user_id)
@user.route('/update_name', methods=['POST'])
def update_user_info():
    user_id = request.form.get('user_id')
    new_username = request.form.get('new_username')
    return u.update_username(user_id, new_username)

@user.route('/update_img',methods=['POST'])
def update_img():
    file = request.files['img_path']
    if 'img_path' not in request.files:
        return jsonify({
            'code': -1,
            'message': '文件上传失败',
            'data': ''})


    if file.filename == '':
        return jsonify({'code':-2,
                        'message': '文件名为空',
                        'data':''})

    user_id=request.form.get('user_id')
    print(user_id)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        nu= u.update_img(user_id,file_path)
        return jsonify({'code': 0,
                        'message': '更改成功',
                        'data': nu.to_dict()})


@user.route('/imagetotext', methods=['POST'])
def imagetotext():

    if 'image' not in request.files:
        return jsonify({'code':-1,
                        'message': '上传文件失败',
                        'data':''})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'code':-2,
                        'message': '文件名为空',
                        'data':''})
    user_id = request.form.get('user_id')
    dialogue_id = request.form.get('dialogue_id')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        top_eight=getText(file_path,user_id,dialogue_id)
        return jsonify({'code':0,
                        'message': 'File uploaded successfully',
                        'data':top_eight})

    return jsonify({'code':-3,
                        'message': '文件类型不接受',
                        'data':''})


@user.route('/texttoimage', methods=['POST'])
def texttoimage():
    # path+name   copy  static      url
    # http://127.0.0.1:5000/flickr30k-images/36979.jpg

    text = request.form.get('text')
    user_id = request.form.get('user_id')
    dialogue_id = request.form.get('dialogue_id')
    top_eight=getImage(text,user_id,dialogue_id)
    if not text:
        return jsonify({
            'code': -1,
            'message': '请输入文本',
            'data': ''})

    updated_top_eight = []
    for image_path, similarity in top_eight:
        # 假设image_path是None，需要替换为新的file_path格式
        # 如果image_path不是None，直接使用它
        if image_path is None:
            # 这里我们使用一个默认的文件名，您可以根据实际情况来指定
            default_filename = "default_image.jpg"
            file_path = f"http://127.0.0.1:5000/{default_filename}"
        else:
            file_path = f"http://127.0.0.1:5000/{image_path}"

        # 将新的file_path和原来的similarity组合成一个元组，并添加到updated_top_two列表中
        updated_top_eight.append((file_path, similarity))

    # 返回更新后的top_two列表和其它信息给前端
    return jsonify({'code': 0,
                    'message': '获取成功',
                    'data': updated_top_eight
                    })

@user.route('/new_dialogue', methods=['POST'])
def new_dialogue():
    user_id = request.form.get('user_id')
    title = request.form.get('title')

    dialogue, error = create_dialogue(user_id,title)
    if error:
        return jsonify({'code': -1,
                        'message': '创建失败',
                        'data': dialogue.to_dict()
                        })
    dialogue_dict = dialogue.to_dict()
    return jsonify({'code': 0,
                    'message': '创建成功',
                    'data': dialogue_dict
                    })

@user.route('deletedialogue',methods=['POST'])
def deletedialogue():
    dialogue_id=request.form.get('dialogue_id')
    print(dialogue_id)
    d.deletedialogue(dialogue_id)
    return jsonify({'code': 0,
                    'message': '删除成功',
                    'data': ''
                    })


@user.route('/dialoguelist', methods=['POST'])
def dialoguelist():
    user_id = request.form.get('user_id')
    return d.dialoguelist(user_id)

@user.route('/get_dialogue', methods=['POST'])
def get_dialogue():
    user_id = request.form.get('user_id')
    dialogue_id = request.form.get('dialogue_id')
    return h.get_history(user_id,dialogue_id)

@user.route('/deletehistory',methods=['POST'])
def deletehistory():
    id=request.form.get('history')
    h.deletehistory(id)
    return jsonify({'code': 0,
                    'message': '删除成功',
                    'data': ''
                    })

@user.route('/dialogue_info',methods=['POST'])
def dialogue_info():
    dialogue_id = request.form.get('dialogue_id')
    dialogue = Dialogue.query.filter_by(dialogue_id=dialogue_id).first()
    if dialogue:
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data':dialogue.to_dict()
            })
    else:
        return jsonify({
            'code': -1,
            'message': '找不到该对话',
            'data':''
            })
@user.route('/update_title',methods=['POST'])
def update_title():
    dialogue_id = request.form.get('dialogue_id')
    new_title = request.form.get('new_title')
    dialogue = Dialogue.query.filter_by(dialogue_id=dialogue_id).first()
    dialogue = Dialogue.update_title(dialogue, new_title)
    if dialogue:
        return jsonify({
            'code': 0,
            'message': '获取成功',
            'data':dialogue.to_dict()
            })
    else:
        return jsonify({
            'code': -1,
            'message': '没有找到对话',
            'data': ''
            })
@user.route('/satisfaction',methods=['POST'])
def satisfactionSet():
    user_id = request.form.get('user_id')
    new_satisfaction = request.form.get('satisfaction')
    return u.satisfactionSet(user_id, new_satisfaction)



