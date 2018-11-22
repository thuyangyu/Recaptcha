from flask import Flask, render_template, Response, request
from flask import current_app
from flask import g

from flask import jsonify
import json
import base64
import random
import io
import pdb

from scipy.misc import imsave
from scipy.misc import imread

from mnist_base_test import construct_captcha_game

def generate_randint():
    randint = random.randint(2,3)
    
    return randint


app = Flask(__name__, template_folder='templates')
TEST_TOTAL_NUM = 25
current_test_index = 1
real_category = None
waited_answer = None
record_item = ""
time_list = []
error_num = 0
@app.route('/')
def frontend_index():
    # return "Index Page"

    global record_item
    global waited_answer
    global time_list
    global error_num

    record_item = ""
    waited_answer = None
    time_list.clear()
    error_num = 0

    return render_template('login.html')

@app.route('/name_category', methods=['POST'])
def name_category():
    global real_category
    global current_test_index
    global record_item
    global waited_answer
    global time_list
    global error_num
    real_category = 1
    current_test_index = 1


    usrname = request.form['usrname']
    category = request.form['category']
    record_item += usrname + ',' + category + ','
    if category == "nonad":
        real_category = "imagenet"
    elif category == "ad":
        real_category = "ad_imagenet"
    return render_template('testing.html', category=real_category, cur_num=current_test_index , total_num=TEST_TOTAL_NUM);


@app.route('/record', methods=['POST'])
def record():
    # print("inside record!")
    global time_list
    global waited_answer
    global error_num
    global current_test_index
    jsonData = request.get_json()
    clicked = jsonData['clicked']
    time = jsonData['time']
    print(type(jsonData)) # int.
    # print('clicked', clicked)
    # print('time', time)
    time_list.append(time)

    print('Progress', current_test_index, ' True_label', waited_answer)

    # print(clicked[0], clicked[8], clicked[9]) # 9 out of space.
    original = True
    for i in waited_answer:
        # print(i, clicked[i])
        if clicked[i] == 0:
            # print('clicked i in first round', clicked[i])
            original = False
        else: #click[i] == 1
            clicked[i] = 0

    for i in clicked:
        if i == 1:
            original = False
    if original == False:

        error_num += 1

    print('Result:', original, ' time on page:', time)
    current_test_index += 1

    return "successful"
@app.route('/rerender', methods=['GET'])
def rerender():
    global TEST_TOTAL_NUM
    global record_item
    global current_test_index
    global real_category
    global time_list
    if current_test_index > TEST_TOTAL_NUM:
        current_test_index = 1
        average_time = 0
        for i in time_list:
            average_time += i
        average_time /= TEST_TOTAL_NUM
        record_item += str(TEST_TOTAL_NUM) + ',' + str(error_num) + ',' + str(error_num / TEST_TOTAL_NUM) + ',' + str(average_time)
        for i in time_list:
            record_item += ',' + str(i)
        record_item += '\n'
        result_file = 'result/final_result.csv'
        f = open(result_file, 'a')
        f.write(record_item)
        f.close()
        return render_template('finished.html', category=real_category, cur_num=current_test_index, total_num=TEST_TOTAL_NUM);

    return render_template('testing.html', category=real_category, cur_num=current_test_index , total_num=TEST_TOTAL_NUM);

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

@app.route('/hello_world/<n>', methods=['POST','GET'])
def index(n):
    # I tried multi-process within a flask func but didnt work
    # just render a simple web page and use javascript to call
    # REST api from python server shell
    user_id = request.args.get('numofpeople','')
    s = generate_randint()
    print(s)
    #return numofpeople
    return render_template('captcha_hci.html', user_id=n)#numofpeople)
'''
@app.route('/<order>')
def order(order):
    if order=='forward':
        return 'forward'
    elif order=='left':
        return 'left'
    elif order=='right':
        return 'right'
    elif order=='back':
        return 'back'
    else:
        return order
'''
@app.route('/tmp')
def display():
    num = request.args.get('numofpeople','')
    return num

@app.route('/hci/<gametype>', methods=['POST','GET'])
def give_a_game(gametype):
    global waited_answer

    classes = [
               'binoculars',
               'brown_bear',
               'CD_player',
               'chimpanzee',
               'dam',
               'Labrador_retriever',
               'magnetic_compass',
               'miniskirt',
               'monarch',
               'pill_bottle',
               'rugby_ball',
               'sports_car',
               'tailed_frog',
               'wooden_spoon'
               ]
    
    captcha_game = construct_captcha_game(gametype)
    captcha_image_list = captcha_game.get_captcha_images()
    captcha_game_groundtruth = captcha_game.get_captcha_groundtruth()
    captcha_game_content = {}
    for i,image in enumerate(captcha_image_list):

        temp_file = 'temp/img_' + str(i+1) + '.png'
        imsave(temp_file, image)
        with io.open(temp_file, 'rb') as image_file:
            content = image_file.read()
        # print("temp_file:", temp_file)
        # image_file = io.open(temp_file, 'rb')
        # content = image_file.read()
        # image_file.close()
        base64_bytes = base64.b64encode(content)
        base64_string = base64_bytes.decode('utf-8')
        cur_img_id = 'img_'+ str(i+1)
        captcha_game_content[cur_img_id]=base64_string
        # print("cur_img_id:", cur_img_id)
        # print("base64_string:", base64_string)

    groundtruth_dic = {}
    for i,truth in enumerate(captcha_game_groundtruth):
        if truth in groundtruth_dic:
            groundtruth_dic[truth].append(i)
        else:
            groundtruth_dic[truth]=[i]
    
    question, waited_answer = random.choice(list(groundtruth_dic.items()))
    print(question, waited_answer)
    type(waited_answer)

    captcha_game_content["task_1"] = 'Select all images with'
    captcha_game_content["task_2"] = classes[question]
    captcha_game_content["task_3"] = 'Click verify once there are none left'
    captcha_game_content["true_labels"] = waited_answer
    
    return jsonify(captcha_game_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
