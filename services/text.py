from flask import jsonify

from models.text import Text
import torch
from PIL import Image
import os
import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
import json


def new_text(text):
    # 加载CLIP模型和预处理函数
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-B-16")

    # 预处理文本内容以得到特征向量
    text_tokens = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    # # 将特征向量转换为JSON字符串
    # text_features_json = json.dumps(text_features.tolist())
    #
    # new_text = Text(text_info= text,text_feature= text_features_json)
    # Text.new_text(new_text)

    # 将特征向量转换为列表
    text_features_list = text_features.tolist()

    # 创建新的Text实例，并将特征向量列表赋值给text_feature字段
    new_text = Text(text_info=text, text_feature=text_features_list)
    Text.new_text(new_text)
    return True
def deleteText(text_to_delete):
    if Text.deleteText(text_to_delete):
        return jsonify({
                'code': 0,
                'message': '删除成功',
                'data': ''
            })
    else:
        return jsonify({
                'code': 3,
                'message': '删除失败',
                'data': ''
            })