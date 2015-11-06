# coding:utf-8
__author__ = 'lufee'
import os
from flask import Flask, request, render_template, redirect, url_for, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt','pdf','png','jpg','jpeg','rar','zip','jar'])


# 判断文件类型是否合法
def allow_file(filename):
    """
    :param filename: 文件名
    :return: 合法 True 否则 False
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']



@app.route('/upload',methods = ['GET','POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        upload_file = request.files['file']
        if upload_file and allow_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            saveFile(upload_file, filename)
            #path = app.config['UPLOAD_FOLDER'] + filename
            #print(path)
            #upload_file.save(path)
        return r'upload successful!'


@app.route('/')
def index():
    return render_template('login.html')


def saveFile(file,filename):
    """
    :param file: 需要保存的文件
    :param filename: 存储在服务器中名字
    :return: 成功存储则返回 True,否则返回 False
    """
    try:
        path = app.config['UPLOAD_FOLDER']
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        file.save(path+filename)
        return True
    except:
        return False


if __name__ == '__main__':
    app.run()