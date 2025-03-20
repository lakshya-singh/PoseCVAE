import os 
import errno
import subprocess
import re
import sys
import shutil

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

in_path=str(sys.argv[1])
if in_path[-1] == '/':
	in_path = in_path[0:-1]
o_path=in_path+'_Frames'
for section in sorted(os.listdir(in_path),key=numericalSort):
		input_path= os.path.join(in_path,section)
		os.makedirs(os.path.join(o_path,section.split('.')[0]))
		out_path= os.path.join(o_path,section.split('.')[0])
		# subprocess.call(['ffmpeg', '-i',input_path,'-vf','-q:v','1',out_path+'/%01d.jpg'] )
		os.system(f"ffmpeg -i {input_path} -qmin 1 -q:v 1 {out_path+'/%01d.jpg'}")
shutil.move(o_path,'./')
