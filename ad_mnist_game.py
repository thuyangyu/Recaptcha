import pdb
import matplotlib.pyplot as plt
import numpy as np
from Captcha_game import Captcha_game as cpg
# from baidu_ocr_test import baidu_ocr
from datetime import datetime
# import cv2
import re


class ad_mnist_game(cpg):
    game_name = "Hi Cyberstorm!"

    def __init__(self, captcha_images_pathlist, ground_truth):
        super(ad_mnist_game, self).__init__()
        self.captcha_image_pathlist = captcha_images_pathlist
        self.ground_truth = ground_truth
        self.captcha_image = None
        self.final_answer = None
        self.is_right = None
        self.start_time = None
        self.end_time = None
        self.time_used = None

    def _start_game(self):
        print("game started!")
        captcha_image_list = []
        for image_path in self.captcha_image_pathlist:
            image = plt.imread(image_path)
            captcha_image_list.append(image)
        # pdb.set_trace()
        self.captcha_image = self.synthesis_images(captcha_image_list)
        self.start_time = datetime.now()

    # self.imshow_captcha(self.captcha_image)

    def _classify(self, mode):
        if mode == "human":
            user_input = raw_input("type answer:")
            print("classifing!")
            # pdb.set_trace()
            print(user_input)
            user_input_screened = []
            for i in user_input:
                if re.findall('\d', i) != []:
                    user_input_screened.append(int(i))
                else:
                    user_input_screened.append(None)

            if user_input_screened == self.ground_truth:
                self.is_right = True
                print("HUMAN!")
            else:
                self.is_right = False
                print("BOT!")

            print(self.ground_truth, user_input_screened)
            self.final_answer = user_input_screened

        elif mode == "bot":
            print("classifing!")
            input_type = "image"
            if input_type == "address":
                bot_input = baidu_ocr(self.captcha_image_pathlist, input_type)
            else:
                factor = 2
                captcha_scaled = cv2.resize(self.captcha_image[0], None, fx=factor, fy=factor)
                bot_input = baidu_ocr([captcha_scaled], input_type)
            print(bot_input)
            bot_input_screened = []
            if bot_input != []:
                bot_input_screened = [int(i) for i in bot_input[0]]

            if bot_input_screened == self.ground_truth:
                self.is_right = True
                print("HUMAN!")
            else:
                self.is_right = False
                print("BOT!")

            print(self.ground_truth, bot_input_screened)
            self.final_answer = bot_input_screened

        else:
            pass
        self.end_time = datetime.now()
        self.time_used = (self.end_time - self.start_time).microseconds * 0.000001
        print("used: " + str(self.time_used) + "s")
        return None

    def synthesis_images(self, captcha_images):
        captcha_image = captcha_images[0]
        for image in captcha_images:
            captcha_image = np.c_[captcha_image, image]
        # pdb.set_trace()
        captcha_image = captcha_image[:, 28:]
        return [captcha_image]

    def imshow_captcha(self, captcha_images):
        plt.figure()
        length = len(captcha_images)

        for i in range(length):
            plt.subplot(1, length, i + 1)
            plt.imshow(captcha_images[i])
        plt.show()

    def record_result(self):
        result = {}
        result["ground_truth"] = self.ground_truth
        result["captcha_image"] = self.captcha_image
        result["final_answer"] = self.final_answer
        result["is_right"] = self.is_right
        result["time_used"] = self.time_used

        return result

    def get_captcha_images(self):
        captcha_image_list = []
        for image_path in self.captcha_image_pathlist:
            image = plt.imread(image_path)
            captcha_image_list.append(image)
        return captcha_image_list

    def get_captcha_groundtruth(self):

        return self.ground_truth
