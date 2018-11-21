import os
import numpy as np
import random
import pdb
import matplotlib.pyplot as plt
import json

from ad_mnist_game import ad_mnist_game

available_games = set(["ad_mnist_2", "ad_mnist_8", "ad_mnist_10", "mnist", "imagenet", "ad_imagenet"])


# generate a list of random number as the final answer
def generate_groundtruth(folder_name,groundtruth_length):
	image_catogories = set(os.listdir(folder_name))
	num_of_catogories = len(image_catogories)
	groundtruth = []
	for i in range(groundtruth_length):
		groundtruth.append(random.randint(0,num_of_catogories-1))

	return groundtruth


# construct captcha game based on type and ground truth
def construct_captcha_game(type="ad_mnist_10"):
    if type not in available_games: raise ValueError("We do not have such game!")
    cwd = os.getcwd()
    folder_name = cwd + "/" + type
    # print(filename_list)
    # print(folder_name)
    groundtruth = generate_groundtruth(folder_name, 9)
    captcha_images_pathlist = read_image_from_file(folder_name, groundtruth)
    captcha_game = ad_mnist_game(captcha_images_pathlist, groundtruth)
    return captcha_game


# return a list of captcha images
def read_image_from_file(folder_name, groundtruth):
    image_catogories = set(os.listdir(folder_name))
    captcha_images_pathlist = []
    for num in groundtruth:
        if str(num) in image_catogories:
            # open num dir and load image
            image_folder_name = folder_name + "/" + str(num)
            image_pool = os.listdir(image_folder_name)
            random_pick = random.randint(0, len(image_pool) - 1)
            selected_name = image_pool[random_pick]
            image_name = image_folder_name + "/" + selected_name
            captcha_images_pathlist.append(image_name)
        else:
            raise ValueError("We have no such images for the answer!")

    return captcha_images_pathlist


def main():
    # init captcha game
    print("available_games: ", available_games)
    game_type = raw_input("Enter game type: ")
    user_id = raw_input("Input your id: ")
    test_result = {}
    num_of_test = 1
    total_test_number = 2
    num_of_practice = 1
    total_practice_number = 3

    # practice warm-up
    print("Practice!")
    pdb.set_trace()
    while num_of_practice <= total_practice_number:
        print(num_of_practice)
        captcha_game = construct_captcha_game(game_type)
        captcha_game()
        num_of_practice += 1
    print("Formal test ready?")
    pdb.set_trace()
    while num_of_test <= total_test_number:
        print(num_of_test)
        captcha_game = construct_captcha_game(game_type)
        # play captcha game
        captcha_game()
        test_result[str(num_of_test)] = captcha_game.record_result()
        num_of_test += 1
    # captcha_game.captcha_api()
    # pdb.set_trace()

    errors = 0
    corrects = 0
    total_time = 0
    for test in test_result:
        if test_result[test]["is_right"] is True:
            corrects += 1
        else:
            errors += 1
        total_time += test_result[test]["time_used"]

    error_rate = float(errors) / (errors + corrects)
    avg_used_time = total_time / len(test_result)
    test_result["error_rate"] = error_rate
    test_result["avg_used_time"] = avg_used_time
    saving_path = os.getcwd() + "/test_result/" + user_id + "_" + game_type + ".json"
    pdb.set_trace()
    with open(saving_path, 'w') as outfile:
        json.dump(test_result, outfile)
    '''
    with open(saving_path, 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, test_result.keys())
        w.writeheader()
        w.writerow(test_result)
    '''
    print("Test done!")
    # pdb.set_trace()


if __name__ == '__main__':
    main()
