from models.dialogue import Dialogue
from datetime import datetime
from models.dialogue import Dialogue
from flask import jsonify
from models.history import History
def create_dialogue(user_id,title):
    if not title:
        return  "Title is required.",None

    dia = Dialogue(user_id = user_id, dialogue_time = datetime.now(),title=title)
    Dialogue.new_dialogue(dia)

    return dia, None
def dialoguelist(user_id):
    dialogues = Dialogue.query.filter_by(user_id = user_id).all()
    return jsonify({
                'code': 0,
                'message': '获取对话列表',
                'data':  [dialogue.to_dict() for dialogue in dialogues]})

def deletedialogue(dialogue_id):
    hs = History.query.filter_by(dialogue_id=dialogue_id).all()
    for h in hs:
        History.deleteHistory(h.id)
    Dialogue.deleteDialogue(dialogue_id)


def checkdialogue(user_id):
    ds=Dialogue.query.filter_by(user_id=user_id).all()
    for d in ds:
        deletedialogue(d.dialogue_id)
