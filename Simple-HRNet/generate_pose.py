import os
import sys
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

path = str(sys.argv[1])

out_path = str(sys.argv[2])

for section in sorted(os.listdir(path),key=numericalSort):
	video_path=os.path.join(path,section)
	pose_path=os.path.join(out_path,section)
	pose_path = pose_path.split('.')[0] + '/'
	# print("\n")
	# print(video_path)
	# print(pose_path)
	os.makedirs(pose_path)
	#for each video run ./scripts/extract-keypoints.py from simple-HRNet to extract pose
	os.system('python ./scripts/extract-keypoints.py --format json --filename '+video_path+' --outdir '+pose_path)