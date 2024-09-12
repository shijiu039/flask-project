from config import db_init as db
class Image(db.Model):
    __tablename__ = 'image'  # 指定表名
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    image_info = db.Column(db.String(255), nullable=False, comment='Image Path')
    image_feature = db.Column(db.JSON, nullable=False, comment='Image Feature Vector')


    # 实现 to_dict 方法
    def to_dict(self):
        return {
            'image_id': self.image_id,
            'image_info': self.image_info,
            'image_feature': self.image_feature,
        }

    @classmethod
    def new_image(cls, image):
        db.session.add(image)
        db.session.commit()
        return True

    @classmethod
    def deleteImage(cls, image_to_delete):
        # 执行删除操作
        db.session.delete(image_to_delete)
        db.session.commit()
        return True