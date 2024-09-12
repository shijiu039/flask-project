from datetime import datetime

from config import db_init as db
class VerifyCode(db.Model):
    __tablename__ = 'verifycode'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    # 实现 to_dict 方法
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'code': self.code,
        }

    def __init__(self, email, code):
        self.email = email
        self.code = code
    @classmethod
    def add(cls,verification_code):
        db.session.add(verification_code)
        # 提交数据库更改
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()  # 发送失败，回滚数据库操作

    @classmethod
    def updateCode(cls, email, code):
        verification_code = VerifyCode.query.filter_by(email=email).first()
        print(verification_code)  # 打印出查询结果，检查是否为None
        if verification_code:
            verification_code.code = code
            verification_code.timestamp = datetime.utcnow()
            db.session.commit()
        else:
            print(f"No record found for email: {email}")
    @classmethod
    def deleteCode(cls,verification_code):
        db.session.delete(verification_code)
        db.session.commit()