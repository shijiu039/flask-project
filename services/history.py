import socket
from models.history import History
from flask import jsonify
def get_history(user_id,dialogue_id):
    histories = History.get_history_by_user_id_and_dialogue_id(user_id,dialogue_id)
    # 预处理历史记录，根据type值修改字段
    for history in histories:
        if history.type == 0:
            history.question = f"http://127.0.0.1:5000/{history.question}"
        elif history.type == 1:
            # 手动设置每个result_i属性
            history.result_1 = f"http://127.0.0.1:5000/{history.result_1}"
            history.result_2 = f"http://127.0.0.1:5000/{history.result_2}"
            history.result_3 = f"http://127.0.0.1:5000/{history.result_3}"
            history.result_4 = f"http://127.0.0.1:5000/{history.result_4}"
            history.result_5 = f"http://127.0.0.1:5000/{history.result_5}"
            history.result_6 = f"http://127.0.0.1:5000/{history.result_6}"
            history.result_7 = f"http://127.0.0.1:5000/{history.result_7}"
            history.result_8 = f"http://127.0.0.1:5000/{history.result_8}"
    return jsonify({
                'code': 0,
                'message': '获取对话列表',
                'data':  [history.to_dict() for history in histories]
    })

def deletehistory(id):
    return History.deleteHistory(id)