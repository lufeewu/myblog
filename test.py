# coding:utf-8
__author__ = 'lufee'


import os
from flask import Flask, make_response, request,render_template,send_from_directory

app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return render_template('index.html')



# 提供下载模块
@app.route('/download/<filename>')
def download_file(filename):
    if filename == 'sybase':
        return send_from_directory('/home/lufee/Downloads/sybase/', 'installwin_ZH.pdf')
    elif filename == 'sybase2':
        return send_from_directory('/home/lufee/Downloads/sybase/', 'sybase15.tar')
    elif filename == 'db2':
        return send_from_directory('/home/lufee/Downloads/', 'db2_v101_win_expc.exe')
    elif filename == 'webapp':
        return send_from_directory('/home/lufee/Downloads/','WebGoat-6.0.1.war')
    elif filename == 'benchmark':
        return send_from_directory('/home/lufee/data/source/db2performance/','SolarWinds-DPA-v10.0.352-SR1-Windows-64Bit-Eval.zip')

    return 'error!'

@app.route('/transform', methods=["POST"])
def transform_view():
    file = request.files['data_file']
    if not file:
        return "No file"

    file_contents = file.stream.read().decode("utf-8")

    result = transform(file_contents)

    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

'''
import os
# 获取当前目录
path = os.getcwd() + '/uploads/'

try:
    os.mkdir(path)
except Exception as e:
    print e
'''