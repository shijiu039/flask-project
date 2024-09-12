import datetime

import torch
from PIL import Image
import os
import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
import json
import pymysql



def getText(image_path,user_id,dialogue_id):
    # 加载CLIP模型和预处理函数
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-B-16")

    print("模型已加载")
    # 连接MySQL数据库
    conn = pymysql.connect(host='localhost', user='root', password='xxy20040805', database='itr')
    cursor = conn.cursor()

    # 读取图片
    image = Image.open(image_path)
    # 预处理图片
    inputs = preprocess(image).unsqueeze(0).to(device)

    # 提取特征向量
    with torch.no_grad():
        image_features = model.encode_image(inputs)
        image_features /= image_features.norm(dim=-1, keepdim=True)

    # 将特征向量转换为JSON字符串
    image_features_json = json.dumps(image_features.tolist())

    # 将图片路径和特征向量存储在数据库中
    cursor.execute('''INSERT INTO image (image_info, image_feature) VALUES (%s, %s)''',
                   (image_path, image_features_json))

    # 初始化一个列表来存储相似度最高的八个记录
    top_eight = [(None, -1)] * 8  # (text_info, similarity)

    # 从数据库中读取所有文本特征
    cursor.execute("SELECT text_info, text_feature FROM text")
    rows = cursor.fetchall()

    # 遍历数据库中的文本特征
    for row in rows:
        text_info, text_features_json = row
        text_features = torch.tensor(json.loads(text_features_json))
        text_features = text_features.to(device)

        # 计算文本特征与图片特征之间的相似度
        similarity = torch.cosine_similarity(text_features, image_features, dim=-1).item()

        # 更新相似度最高的八个记录
        new_record = (text_info, similarity)
        if len(top_eight) < 8:
            top_eight.append(new_record)
        else:
            for i in range(8):
                if similarity > top_eight[i][1]:
                    top_eight[i] = new_record
                    break
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 执行SQL插入语句
    cursor.execute('''INSERT INTO history (question, result_1, result_2, result_3, result_4, result_5, result_6, result_7, result_8,type, user_id, dialogue_id,create_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                   (image_path,top_eight[0][0],top_eight[1][0],top_eight[2][0],top_eight[3][0],top_eight[4][0],top_eight[5][0],top_eight[6][0],top_eight[7][0],0,user_id,dialogue_id,current_time))

    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()

    # 返回相似度最高的八个记录
    return top_eight
def getImage(text,user_id,dialogue_id):
    # 加载CLIP模型和预处理函数
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-B-16")

    print("模型已加载")
    # 连接MySQL数据库
    conn = pymysql.connect(host='localhost', user='root', password='xxy20040805', database='itr')
    cursor = conn.cursor()

    # 预处理文本
    text_tokens = clip.tokenize([text]).to(device)

    # 提取文本特征向量
    with torch.no_grad():
        text_features = model.encode_text(text_tokens)
        text_features /= text_features.norm(dim=-1, keepdim=True)

    # 从数据库中读取所有图片特征
    cursor.execute("SELECT image_info, image_feature FROM image")
    rows = cursor.fetchall()

    # 初始化一个列表来存储相似度最高的八个记录
    top_eight = [(None, -1)] * 8  # (image_path, similarity)

    # 从数据库中读取所有图片特征
    cursor.execute("SELECT image_info, image_feature FROM image")
    rows = cursor.fetchall()

    # 遍历数据库中的图片特征
    for row in rows:
        image_path, image_features_json = row
        image_features = torch.tensor(json.loads(image_features_json))
        image_features = image_features.to(device)

        # 计算文本特征与图片特征之间的相似度
        similarity = torch.cosine_similarity(text_features, image_features, dim=-1).item()

        # 更新相似度最高的八个记录
        for i in range(len(top_eight)):
            if similarity > top_eight[i][1]:
                top_eight.insert(i, (image_path, similarity))
                top_eight.pop()  # 移除相似度最低的记录
                break  # 退出循环，因为已经插入到正确的位置

    # top_eight 现在包含了相似度最高的八个记录

    # 获取当前时间
    current_time = datetime.datetime.now()

    # 执行SQL插入语句
    cursor.execute(
        '''INSERT INTO history (question, result_1, result_2, result_3, result_4, result_5, result_6, result_7, result_8,type, user_id, dialogue_id,create_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        (text, top_eight[0][0], top_eight[1][0], top_eight[2][0], top_eight[3][0], top_eight[4][0],
         top_eight[5][0], top_eight[6][0], top_eight[7][0], 1, user_id, dialogue_id, current_time))

    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()
    return top_eight

