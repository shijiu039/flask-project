from config import db_init as db

class History(db.Model):
    __tablename__ = 'history'  # 指定表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='Primary Key')
    question = db.Column(db.String(255))
    result_1 = db.Column(db.String(255))
    result_2 = db.Column(db.String(255))
    result_3 = db.Column(db.String(255))
    result_4 = db.Column(db.String(255))
    result_5 = db.Column(db.String(255))
    result_6 = db.Column(db.String(255))
    result_7 = db.Column(db.String(255))
    result_8 = db.Column(db.String(255))
    type = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    dialogue_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'result_1': self.result_1,
            'result_2': self.result_2,
            'result_3': self.result_3,
            'result_4': self.result_4,
            'result_5': self.result_5,
            'result_6': self.result_6,
            'result_7': self.result_7,
            'result_8': self.result_8,
            'dialogue_id': self.dialogue_id,
            'type':self.type,
            'user_id': self.user_id,
            'dialogue_id': self.dialogue_id,
            'create_time':self.create_time

        }

    @classmethod
    def get_history_by_user_id_and_dialogue_id(cls,user_id, dialogue_id):
        return History.query.filter_by(user_id=user_id, dialogue_id=dialogue_id).all()

    @classmethod
    def deleteHistory(cls,id):
       h = History.query.filter_by(id=id).first()
       db.session.delete(h)
       db.session.commit()