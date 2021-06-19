import os 
import errno
import subprocess
import re
import sys

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

in_path=sys.argv[1]
o_path=sys.argv[1]+'_Frames'
for section in sorted(os.listdir(in_path),key=numericalSort):
		input_path= os.path.join(in_path,section,section+'.avi')
		os.makedirs(os.path.join(o_path,section))
		out_path= os.path.join(o_path,section)
		subprocess.call(['ffmpeg', '-i',input_path,'-vf','fps=25','-q:v','1',out_path+'/%06d.jpg'] )