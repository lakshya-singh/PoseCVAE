import os
import sys
import numpy as np
import re

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#path = './Testing/generate_object_npy/'   ##path for old npy files
path = sys.argv[1]
#save_path =  './Testing/final_object_npy/' ##save path for new npy files
save_path = sys.argv[2]
folders = sorted(os.listdir(path)) ##list all folders in the old path
camera_id = 14.0

for folder in folders:   ##enter into each folder
    sections = sorted(os.listdir(path+folder),key=numericalSort)
    #camera_id = float(folder.split('_')[0])
    print(camera_id)
    os.makedirs(save_path+folder) ##make a new folder in new save path
    print(len(sections))
    for section in sections:  ##enter into each section
        data = np.load(path+folder+'/'+section,allow_pickle=True) ##load data for ex 1_1.npy
        video_id = float(folder)
        #video_id = float(folder.split('_')[1])  ##find video_id ex 1.0
        person_id = float(section.split('_')[0]) ##find person_id
        save_list =  list() ##list to save new data
        for person_data in data:   ##enter into data of particular section ex 1_1.npy
            #print(person_data)
            frame_number = float(person_data[2].split('.')[0]) ##read frame number and find coordinates
            coordinate_list = person_data[0]
            x_list = coordinate_list[::3]
            y_list = coordinate_list[1::3]
            conf_list = coordinate_list[2::3]
            new_data = [camera_id,video_id,frame_number]
            new_data.extend(x_list)
            new_data.extend(y_list)
            new_data.extend(conf_list)
            new_data.append(person_id)
            new_data.append(0)
            save_list.append(new_data) ##append the whole new data to save list 
        
        np.save(save_path+folder+'/'+section,save_list) ## save the complete modified person data 