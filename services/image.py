from flask import jsonify

from models.image import Image as img
import torch
from PIL import Image
import os
import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
import json


def new_image(image_path):
    # 加载CLIP模型和预处理函数
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-B-16")

    # 读取图片
    image = Image.open(image_path)

    # 预处理图片
    inputs = preprocess(image).unsqueeze(0).to(device)

    # 提取特征向量
    with torch.no_grad():
        image_features = model.encode_image(inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    # 将特征向量转换为列表
    image_features_list = image_features.tolist()

    # 创建新的Text实例，并将特征向量列表赋值给text_feature字段
    new_img = img(image_info=image_path, image_feature=image_features_list)
    img.new_image(new_img)
    return True

def deleteImage(image_to_delete):
    if img.deleteImage(image_to_delete):
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