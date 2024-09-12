from config import db_init as db
class Dialogue(db.Model):
    __tablename__ = 'dialogue'  # 指定表名
    dialogue_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), comment='User ID')
    dialogue_time = db.Column(db.DateTime, default=None, comment='Dialogue Time')
    title = db.Column(db.String(255), default=None,  comment='Title')

    # 创建一个外键约束
    user = db.relationship('User', backref='dialogue')

    # 实现 to_dict 方法
    def to_dict(self):
        return {
            'dialogue_id': self.dialogue_id,
            'user_id': self.user_id,
            'dialogue_time': self.dialogue_time.isoformat(),
            'title':self.title,
        }

    @classmethod
    def new_dialogue(cls, dialogue):
        db.session.add(dialogue)
        db.session.commit()
        return True

    @classmethod
    def deleteDialogue(cls,dialogue_id):
        dialogue_to_delete = Dialogue.query.filter_by(dialogue_id=dialogue_id).first()
        if dialogue_to_delete:
            # 如果找到了记录，则删除它
            db.session.delete(dialogue_to_delete)
            db.session.commit()

    @classmethod
    def update_title(cls, dialogue, new_title):
        dialogue.title = new_title
        db.session.commit()
        return dialogue