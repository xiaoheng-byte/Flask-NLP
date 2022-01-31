import datetime
import os
import jiagu
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
import jieba
import re
import jiagu as jg
import json
import base64

from matplotlib import image
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
from stanfordcorenlp import StanfordCoreNLP
#nlp = StanfordCoreNLP(r'C:\Users\29271\Desktop\stanford-corenlp-full-2018-10-05', lang='zh')
import jieba.posseg as pseg
app = Flask(__name__)
from flask_cors import CORS


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/segmentation',methods=["GET"])
def reslut():
    text = request.values.get('text')
    print("--------------text", text)
    result = segmentation(text)
    print("--------------result", result)
    return (jsonify(result))  #列表转化json

def segmentation(text):
    ttt= jieba.cut(text)
    ttt= list(ttt)
    print("ttt",ttt)
    print("【返回列表】"+"/".join(ttt))
    return ttt

@app.route('/pos',methods=["GET"])
def result2():
    text = request.values.get('text')
    print("--------------text", text)
    result = pos(text)
    print("--------------result", result)
    return (jsonify(result))  #列表转化json

def pos(text):
    poswords=[]
    posword= pseg.cut(text)
    for item in posword:
        poswords.append(item.word+"---"+item.flag)
    print("【返回列表】"+"/".join(posword))
    return poswords
'''
@app.route('/ner',methods=["GET"])
def result3():
    text = request.values.get('text')
    print("--------------text", text)
    result = ner(text)
    print("--------------result", result)
    return (jsonify(result))
'''

'''
def ner(text):
  nerwords = []
  nerword = nlp.ner(text)
  for item in nerword:
    if(item[1] == "O"):
      continue
    nerwords.append(item[0] + "--" + item[1])
  return nerwords
'''


@app.route('/sentiment',methods=["GET"])
def result4():
    text = request.values.get('text')
    print("--------------text", text)
    result = sentiment(text)
    print("--------------result", result)
    return (jsonify(result))  #列表转化json

def sentiment(text):
    senti=[]
    articles_sentences=cutsentences(text)
    for sentence in articles_sentences:
        sentiment = jg.sentiment(sentence)
        senti.append(str(sentiment[0])+","+str("%.4f" %sentiment[1])+" : "+sentence)

    return senti

def cutsentences(text):
    sentences = re.split("(。|！|\!|？|\?|\\n)", text)
    nsent  = []
    for i in range(int(len(sentences) / 2)):
        if (sentences[2 * i + 1] == "\n"):
            sent = sentences[2 * i]
        else:
            sent = sentences[2 * i] + sentences[2 * i + 1]
        if sent!= '':
            nsent.append(sent)

    if sentences[len(sentences)-1] != '':
        nsent.append(sentences[len(sentences)-1])
    return nsent

@app.route('/wordcloud',methods=["GET"])
def result5():
    text = request.values.get('text')
    print("--------------text", text)
    result5 = wordclouds(text)
    print("--------------result", result5)
    return result5

def wordclouds(text):
  font_path = '方正品尚黑简体.ttf'
  # 2.结巴中文分词，生成字符串，默认精确模式，如果不通过分词，无法直接生成正确的中文词云
  cut_text = jieba.cut(text)
  # print(type(cut_text))
  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
  result = " ".join(cut_text)
  # print(result)
  # 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
  # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
  wc = WordCloud(
    # 设置字体，不指定就会出现乱码
    font_path= font_path,
    # 设置背景色
    background_color='white',
    # 设置背景宽
    width=500,
    # 设置背景高
    height=350,
    # 最大字体
    max_font_size=50,
    # 最小字体
    min_font_size=10,
    mode='RGB'
    # colormap='pink'
  )
  # 产生词云
  wc.generate(result)
  # 保存图片
  nowTime = datetime.datetime.now().strftime('%H-%M-%S')
  filename = "ciyun" + str(nowTime) + ".jpg"
  wc.to_file(filename)
  return filename


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run(port=5000)
