from flask import Flask, render_template, Response, request
from flask import current_app
from flask import g

from flask import jsonify
import json
import base64
import io

app = Flask(__name__)

context = app.app_context()
context.push()


@app.route('/')
def index():
    # return "Index Page"
    return render_template('login.html')


@app.route('/name_category', methods=['POST'])
def name_category():
    usrname = request.form['usrname']
    category = request.form['category']
    result_file = 'result.txt'
    f = open(result_file, 'a')
    line = usrname + ',' + category + ',\n'
    f.write(line)
    f.close()
    return render_template('testing.html')


@app.route('/get_task')
def get_task():

    file_name = 'static/img/4.PNG'
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    base64_bytes = base64.b64encode(content)
    base64_string = base64_bytes.decode('utf-8')
    # l = {'a': base64_string, 'b': base64_string}

    # return json.dumps(l)
    return jsonify(task_1='Select all images with',
                   task_2='Bicycle',
                   task_3='Click verify once there are none left',
                   img_1=base64_string,
                   img_2=base64_string,
                   img_3=base64_string,
                   img_4=base64_string,
                   img_5=base64_string,
                   img_6=base64_string,
                   img_7=base64_string,
                   img_8=base64_string,
                   img_9=base64_string)

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
