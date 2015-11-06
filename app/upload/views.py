# coding:utf-8
__author__ = 'lufee'
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from . import upload
import os

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','rar','zip','jar'])
UPLOAD_FOLDER = os.getcwd() + '/uploads/'

def allow_file(filename):
    """
    :param filename: 文件名
    :return: 合法 True 否则 False
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@upload.route('/',methods = ['GET','POST'])
def upload_file():
    print 'ufile', request.method
    if request.method == 'GET':
        return render_template('upload/upload.html')
    elif request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allow_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            saveFile(upload_file, filename)
            #path = app.config['UPLOAD_FOLDER'] + filename
            #print(path)
            #upload_file.save(path)
        return r'upload successful!'

def saveFile(file,filename):
    """
    :param file: 需要保存的文件
    :param filename: 存储在服务器中名字
    :return: 成功存储则返回 True,否则返回 False
    """
    try:
        path = UPLOAD_FOLDER
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        file.save(path+filename)
        return True
    except:
        return False
