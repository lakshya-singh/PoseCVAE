## Import Library
import json
import numpy as np
import os
import sys

## function to extract index key
def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

## read json file
#path = './Pose_tracker/avenue_tracker_json/training/' #example path for tracker json file
path = str(sys.argv[1])
#save path for generated numpy files
save_path = str(sys.argv[2])
sections = sorted(os.listdir(path))
for section in sections:
    with open(path+section+'/alphapose-results-forvis-tracked.json') as f:
        data = json.load(f) 


## Make new dict with Person id as key
    numpy_data={}
    keys=sorted(data.keys())
    for key in sorted(keys):
#         print('Number of Persons: ',len(data[key]))
        for frame_data in data[key]:
            new_temp = without_keys(frame_data,'idx')
            idx= frame_data['idx']
            new_temp['frame_num'] = key
            if(not(idx in numpy_data)):
                numpy_data[idx]=list()
                numpy_data[idx].append(new_temp)
            else:
                numpy_data[idx].append(new_temp)


## Convert Dict items to list
    new_dict={}
    for key in numpy_data.keys():
        new_data=numpy_data[key]
        final=[]
        for item in new_data:
            dictlist=[]
            [dictlist.extend([v]) for k,v in item.items()]
            final.append(dictlist)
        new_dict[key]=final

## Generate npy file with continues tracks
    total_len=0
    # os.makedirs(save_path+'/generate_npy/'+section)
    os.makedirs(save_path+'/'+section)
    frame_set=list()
    number_list=list()
    for key in new_dict.keys():
        past=int(new_dict[key][0][2].strip('.jpg'))
        print(key,new_dict[key][0][2])
        ini_index=0
        number=1;
        if(len(new_dict[key])==1):
            np.save(save_path+'/'+section+'/'+str(key)+'_'+str(number),new_dict[key][ini_index:1])
            number_list.append(str(key)+'_'+str(number))
            frame_set.append(new_dict[key][ini_index][2])
            total_len+=1
        for i in range(1,len(new_dict[key])):
            present=int(new_dict[key][i][2].strip('.jpg'))
            if(present-past==1):
                past=present
                if(i==len(new_dict[key])-1):
                    np.save(save_path+'/'+section+'/'+str(key)+'_'+str(number),new_dict[key][ini_index:i+1])
                    number_list.append(str(key)+'_'+str(number))
                    total_len+=len(new_dict[key][ini_index:i+1])
                    for m in range(ini_index,i+1):
                        frame_set.append(new_dict[key][m][2])
                continue
            else:
                np.save(save_path+'/'+section+'/'+str(key)+'_'+str(number),new_dict[key][ini_index:i])
                number_list.append(str(key)+'_'+str(number))
                number+=1
                total_len+=len(new_dict[key][ini_index:i])
                for m in range(ini_index,i):
                    frame_set.append(new_dict[key][m][2])
                if(i==len(new_dict[key])-1):    
                    total_len+=1
                    np.save(save_path+'/'+section+'/'+str(key)+'_'+str(number),new_dict[key][i:i+1])
                    number_list.append(str(key)+'_'+str(number))
                    frame_set.append(new_dict[key][i][2])
                past=present
                ini_index=i
                
                
    print(section,total_len)
    print(section,len(frame_set))
    print(section,len(set(frame_set)))
    print(section,len(number_list))
    print(section,len(set(number_list)))
    
