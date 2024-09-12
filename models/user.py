from config import db_init as db

class User(db.Model):
    __tablename__ = 'user'  # 指定表名
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    user_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    img_path=db.Column(db.String(255),nullable=False)
    satisfaction = db.Column(db.Integer, default=5)
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,  # 注意：在实际应用中，出于安全考虑，不应该直接返回密码
            'img_path': f"http://127.0.0.1:5000/{self.img_path}",
            'satisfaction': self.satisfaction
        }

    @classmethod
    def register(cls,user):
        db.session.add(user)
        db.session.commit()
        return True
    @classmethod
    def update_username(cls,user_id,new_username):
        user=User.query.get(user_id)
        user.user_name=new_username
        db.session.commit()
        return user

    @classmethod
    def update_img(cls,user_id,file_path):
        user=User.query.get(user_id)
        user.img_path=file_path
        db.session.commit()
        return user

    @classmethod
    def deleteUser(cls, user_to_delete):
        # 执行删除操作
        db.session.delete(user_to_delete)
        db.session.commit()
        return True

    @classmethod
    def satisfacationSet(cls,user,satisfaction):
        user.satisfaction = satisfaction
        db.session.commit()
        return user

