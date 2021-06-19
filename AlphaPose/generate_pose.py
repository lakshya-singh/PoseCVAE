import os
import os.path
from shutil import copyfile
import sys
import re

#code for sorting
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#path="/home/SharedData/Ashvini/Public_Dataset/Training/Train_Frames/" #example of path
path = str(sys.argv[1])
#out_path="/home/SharedData/Ashvini/Public_Dataset/Training/Frames_pose" #example of save_path
out_path = str(sys.argv[2])

for section in sorted(os.listdir(path),key=numericalSort):
	image_path=os.path.join(path,section)
	pose_path=os.path.join(out_path,section)
	os.makedirs(pose_path)
	#for each frame run demo.py from alphapose to extract pose
	os.system('python demo.py --indir '+image_path+' --outdir '+pose_path)
	

#python demo.py --indir /home/SharedData/Royston/AlphaPose/Pose_tracker/avenue/training/frames/16 --outdir /home/SharedData/Royston/#AlphaPose/Pose_tracker/avenue_result/training/16/

		




