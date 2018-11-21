#coding:utf-8
# lalalala test with baidu api ocr wawawa

from aip import AipOcr
import pdb
import os
import random
import cv2
""" 你的 APPID AK SK """
APP_ID = '14503274'
API_KEY = 'y5RH3E64eKZfGwU4GGRk26OS'
SECRET_KEY = 'SCz6QygkpfqID8Vh8hLPELPHc8xkl82S'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def baidu_ocr(input,input_type="address"):
	result = []
	""" 如果有可选参数 """
	options = {}
	options["detect_direction"] = "true"
	options["probability"] = "true"
	if input_type == "address":
		for i,path in enumerate(input):
			image = get_file_content(path)
			# response = client.basicAccurate(image)
			response = client.handwriting(image,options)
			# response = client.numbers(image,options)
			print(response["words_result"])
			# pdb.set_trace()
			if response["words_result"] != []:
				result.append(response["words_result"][0]["words"])
			else:
				result.append("-1")
	elif input_type == "image":
		path = os.getcwd()
		image_path = path + "/tmp.jpg"
		is_successful = cv2.imwrite('tmp.jpg',input[0])
		if is_successful is False: print("Saving Error!")
		image = get_file_content(image_path)
		response = client.numbers(image,options)
		# pdb.set_trace()
		if response["words_result"] != []:
			word = response["words_result"][0]["words"]
			result.append(word)
		else:
			pass
	else:
		raise ValueError("We do not have this input_type!")	
	return result

def main():
	while True:
		ground_truth = random.randint(0,9)
		print("ground_truth: ",ground_truth)
		path = os.getcwd()
		path += "/ad_mnist_2/"+str(ground_truth)
		examples = os.listdir(path)
		selected_example = examples[random.randint(0,len(examples)-1)]
		example_path = path+"/"+selected_example
		image = get_file_content(example_path)

		""" 调用通用文字识别（高精度版） """
		client.basicAccurate(image);

		""" 如果有可选参数 """
		options = {}
		options["detect_direction"] = "true"
		options["probability"] = "true"

		""" 带参数调用通用文字识别（高精度版） """
		# result = client.basicAccurate(image, options)
		result = client.handwriting(image, options)
		print("answer: ",result["words_result"])
		pdb.set_trace()

if __name__ == '__main__':
	main()




