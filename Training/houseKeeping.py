import os
import shutil

#This is a housekeeping file. To be run ONCE after you paste fresh "sliding_window files" folder in this "training" folder
#Divide your sliding_window output of the dataset into two parts and keep corresponding training and validation sliding_window data in each folder

path_t = './sliding_window_train/'
path_v = './sliding_window_val/'

train = os.listdir(path_t)
val = os.listdir(path_v)

for folder in train:
	src = os.path.join(path_t,folder)
	file_names = os.listdir(src)
	for file_name in file_names:
		shutil.move(os.path.join(src, file_name), path_t)
	shutil.rmtree(src)

for folder in val:
	src = os.path.join(path_v,folder)
	file_names = os.listdir(src)
	for file_name in file_names:
		shutil.move(os.path.join(src, file_name), path_v)
	shutil.rmtree(src)
