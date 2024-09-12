from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,static_folder='./flickr30k-images')


app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '2084609377@qq.com'
app.config['MAIL_PASSWORD'] = 'grcvwrkpbpwqbiih'
app.config['MAIL_DEFAULT_SENDER'] = '2084609377@qq.com'
# 连接数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:xxy20040805@127.0.0.1:3306/itr'

app.config['UPLOAD_FOLDER'] = 'flickr30k-images/'  # 指定上传文件夹
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的文件扩展名

# 数据库连接对象
db_init = SQLAlchemy(app)
