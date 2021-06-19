import os
import shutil

path = './sliding_window/'
folders = os.listdir(path)

for folder in folders:
	shutil.rmtree(path+'/'+folder+'/'+'result')