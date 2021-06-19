import os
import os.path
from shutil import copyfile
import sys
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#path="/home/SharedData/Ashvini/Public_Dataset/Training/Train_Frames/" #example path to frames
path = str(sys.argv[1])
#in_json='/home/SharedData/Ashvini/Public_Dataset/Training/Frames_pose/' #example path to pose json
in_json = str(sys.argv[2])
#out_json='/home/SharedData/Ashvini/Public_Dataset/Training/Frames_track/' #example path for save
out_json = str(sys.argv[3])
#out_path="/home/SharedData/Ashvini/shanghaitech/training/Frames_track_vis/"

# my_data=[str(x).zfill(2) for x in range(1,22)]
# my_data=['000109']
# my_data=['01.avi_frames','02.avi_frames','03.avi_frames','04.avi_frames','05.avi_frames','06.avi_frames','07.avi_frames','08.avi_frames','09.avi_frames','10.avi_frames','11.avi_frames','12.avi_frames','13.avi_frames','14.avi_frames','15.avi_frames','16.avi_frames']

my_data = os.listdir(path)
#section = "01_001"
for section in sorted(my_data,key=numericalSort):
#for i in range(1):
	image_path=os.path.join(path,section)
	in_json_path=os.path.join(in_json,section)+'/output.json'
	out_json_path=os.path.join(out_json,section)
	#pose_path=os.path.join(out_path,section)
	#os.makedirs(pose_path)
	if not os.path.exists(out_json_path):
	    os.makedirs(out_json_path)
	out_json_path=out_json_path+'/alphapose-results-forvis-tracked.json'
	print(image_path)
	print(in_json_path)
	print(out_json_path)
	#print(pose_path)
	os.system('python tracker-general.py --imgdir '+image_path+' --in_json '+in_json_path+' --out_json '+out_json_path)
	


##python tracker-general.py --imgdir /home/SharedData/Ashvini/AlphaPose/Pose_tracker/avenue_track/training/frames/01/ --in_json /home/SharedData/Ashvini/AlphaPose/Pose_tracker/avenue_result/training/01/alphapose-results.json --out_json /home/SharedData/Ashvini/AlphaPose/Pose_tracker/avenue_tracker_json/training/01/alphapose-results-forvis-tracked.json --visdir /home/SharedData/Ashvini/AlphaPose/Pose_tracker/avenue_tracker_vis/training/01/




