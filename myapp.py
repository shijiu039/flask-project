from flask import Flask, request
from routes.user import user
from config import app
from routes.administrator import administrator
from flask_cors import CORS

#注册蓝图
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(administrator, url_prefix="/administrator")

CORS(app)



@app.route('/')
def ping():
    return 'ok'

# @app.before_request
# def before():


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
