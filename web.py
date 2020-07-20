from flask import Flask,render_template,request,redirect,url_for,make_response,jsonify
from kafka import KafkaConsumer
import yolov3_deepsort
from flask_script import Manager




#设置允许的 wenjian geshi
app = Flask(__name__)

# manager = Manager(app=app)
def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    # img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream



@app.route('/sendMsg',methods=['POST','GET'])
def gotoSendMSG():
    if request.method == 'POST':

        user_input = request.form.get('name')
        print(user_input)
        # print(user_input,"video/my_videoLine.mkv")
        yolov3_deepsort.runPro(user_input)
        consumer = KafkaConsumer('test', bootstrap_servers=["192.168.6.153:9092"])
        # for msg in consumer:
        #     # str(msg, encoding="utf-8")
        #     recv = "value=%s" % bytes.decode(msg.value)
        #     # print(msg.value)
        #     print(recv,"----------------------------------------------")
        #     img_url = return_img_stream(recv).decode()
        img_url = return_img_stream(user_input).decode()
        return render_template('sendMsg_ok.html', userinput=user_input, pictureName=img_url)
        # img_path = 'output/img288.jpg'
        # img_path = '/home/xd/Desktop/pedestrainYolu3Okbak/output/img336.jpg'
        # img_path = recv
        # print(img_path)

    return render_template('sendMsg.html')


if __name__ == '__main__':
    # from livereload import Server
    #
    # server = Server(app.wsgi_app)
    # server.watch('**/*.*')
    # server.serve()
    app.run(debug=True)