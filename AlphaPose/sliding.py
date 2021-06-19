#import Library files

import os
import re
import sys
import numpy as np

sliding_win_len = int(sys.argv[1])

#code for sorting
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def slidingWindow(data, data_len, window_size,view_num,video_id,person_id,example,new_path):
    print("total files ::",data_len-window_size+1)
    i=0
    while (window_size+i<=data_len):
        new_data = data[i:window_size+i]
        video_id = video_id.zfill(4)
        name = view_num+'_'+video_id+'_'+person_id+'_'+str(example)
        print("original:",name, i," to ", window_size+i)
        np.save(new_path+name,new_data)
        example = example+1
        i=i+1
    return example


view_num ='14'

#path = './final_npy/' #example path
path = str(sys.argv[2])
#save_path = './train_'+str(sliding_win_len)+'/' #example save path
save_path = str(sys.argv[3])
sections = sorted(os.listdir(path),key=numericalSort)
example = 1

#code for sliding window, files with length less than 2*sliding_Win_len will be ignored
for section in sections:
    files = sorted(os.listdir(path+section),key=numericalSort)
    video_id = section
    for dfile in files:
        person_id = dfile.split('_')[0]
        data = np.load(path+section+'/'+dfile)
        data_len = len(data)
        print("\ndata loaded:: ",path+section+'/'+dfile)
        if(data_len<2*sliding_win_len):
            print(dfile,"size is ",data_len," and therefore is a short file")
            continue
        
        new_path = save_path+video_id+'/'+person_id+'/'
        new_path = save_path+video_id+'/'
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            #os.makedirs(new_path+'/'+'result')
        
        example = len(os.listdir(new_path))+1
        print("length == ", data_len)
        #if(data_len>=6 and data_len<10):
        if(data_len>=2*sliding_win_len):
           example = slidingWindow(data,data_len,2*sliding_win_len,view_num,video_id,person_id,example,new_path)
'''      
        if(data_len>=10 and data_len<=25):
            example = slidingWindow(data,data_len,10,view_num,video_id,person_id,example,new_path)
        
        if(data_len>=26):
            example = slidingWindow(data,data_len,26,view_num,video_id,person_id,example,new_path)'''                    