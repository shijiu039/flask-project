from config import db_init as db

class Administrator(db.Model):
    __tablename__ = 'administrator'  # 指定表名
    administrator_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    administrator_name = db.Column(db.String(255), nullable=False)
    administrator_email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255),nullable=False)
    def to_dict(self):
        return {
            'administrator_id': self.administrator_id,
            'administrator_name': self.administrator_name,
            'administrator_email': self.administrator_email # 注意：在实际应用中，出于安全考虑，不应该直接返回密
        }
    @classmethod
    def register(cls,administrator):
        db.session.add(administrator)
        db.session.commit()
        return True




