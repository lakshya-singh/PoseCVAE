import os

path = './sliding_window/'
folders = os.listdir(path)

for folder in folders:
	os.makedirs(path+folder+'/'+'result')