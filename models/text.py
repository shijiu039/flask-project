from config import db_init as db
class Text(db.Model):
    __tablename__ = 'text'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    text_info = db.Column(db.String(255), nullable=False, comment='Image Path')
    text_feature = db.Column(db.JSON, nullable=False, comment='Image Feature Vector')


    # 实现 to_dict 方法
    def to_dict(self):
        return {
            'id': self.id,
            'text_info': self.text_info,
            'text_feature': self.text_feature,
        }

    @classmethod
    def new_text(cls, text):
        db.session.add(text)
        db.session.commit()
        return True
    @classmethod
    def deleteText(cls, text_to_delete):
        # 执行删除操作
        db.session.delete(text_to_delete)
        db.session.commit()
        return True
