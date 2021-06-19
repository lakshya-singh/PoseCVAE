
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
import math
import pandas as pd
import re


numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

path = './final_npy_train/01/'
files_path = sorted(os.listdir(path),key=numericalSort)

#path_org = './test_32_result/gt/'
#path_pred = './test_32_result/pred/'
#files_org = sorted(os.listdir(path_org),key=numericalSort)
#files_pred = sorted(os.listdir(path_pred),key=numericalSort)

for file_org in files_path:
	datas_org = np.load(path+file_org)
	#datas_pred = np.load(path_pred+file_pred)
	#print("org_shape::",datas_org.shape)
	#print("pred_shape::",datas_pred.shape)
	#os.mkdir('test_32_result_vis/'+file_org)
	names = file_org.split('_')
	video_name = '01'
	for data_org in datas_org:
		count = len(str(len(os.listdir('training/frames/'+video_name))))
		frame = str(int(data_org[2])).zfill(count)
		image = cv2.imread('./training/frames/'+video_name+'/'+frame+'.jpg')
		x_org = data_org[3:20]
		#x_org = [i * 640.0 for i in x_org]
		y_org = data_org[20:37]
		#y_org = [i * 360.0 for i in y_org]
		#print("x_org::",x_org,"    ","y_org::",y_org)		
		#print("x_pred::",x_pred,"    ","y_pred::",y_pred)
		#print(len(x_org),len(y_org),len(x_pred),len(y_pred))
		for yi,xi in zip(x_org,y_org):
			cv2.circle(image, (int(yi),int(xi)), 0, (0,255,0), 5)
		cv2.imwrite('./training/frames/'+video_name+'/'+frame+'.jpg',image)
		print('./training/frames/'+video_name+'/'+frame+'.jpg')
