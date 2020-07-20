from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from werkzeug.utils import secure_filename

import os
import cv2
import time
from datetime import timedelta
#设置允许的 wenjian geshi
ALLOWD_EXITSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit(".",1)[1] in ALLOWD_EXITSIONS

app = Flask(__name__)
#设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=2)

@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get('name')
        basepath = os.path.dirname(__file__)#当前文件所在的位置
        #没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path = os.path.join(basepath,'static/images', secure_filename(f.filename))
        f.save(upload_path)
        #使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('upload_ok.html', userinput=user_input, val1=time.time())
        return render_template('upload_ok.html', userinput=user_input, val1=time.time())

    return render_template('upload.html')