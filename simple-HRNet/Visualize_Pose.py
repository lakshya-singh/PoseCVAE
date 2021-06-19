
#get_ipython().run_line_magic('matplotlib', 'inline')
##library import
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import torch
import os
import math
import pandas as pd


path= './tracks_npy/14_0001_2_32.npy'


data = np.load(path)
print(len(data))


# In[5]:


video_id = data[0][1]
frame_no = data[0][2]
x = data[0][3:19]
y = data[0][20:36]
print(max(x))
print(max(y))
print(video_id)
print(frame_no)


# In[6]:


image_path = './Pose_tracker/avenue/training/frames/01/0000.jpg'
im = mpimg.imread(image_path)
print(im.shape)
plt.imshow(im)


# In[6]:



# Make empty black image
image=np.zeros((360,640,3),np.uint8)

# Make one pixel red
for yi,xi in zip(x,y):
#     image[int(xi),int(yi)] = [0,0,255]
    cv2.circle(image, (int(yi),int(xi)), 0, (0, 20, 200), 5)

# Save
cv2.imwrite("result.png",image)


# In[2]:


def vis_frame(im_res, format='coco'):
    '''
    frame: frame image
    im_res: im_res of predictions
    format: coco or mpii

    return rendered image
    '''
    if format == 'coco':
        l_pair = [
            (0, 1), (0, 2), (1, 3), (2, 4),  # Head
            (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
            (17, 11), (17, 12),  # Body
            (11, 13), (12, 14), (13, 15), (14, 16)
        ]

        p_color = [(0, 255, 255), (0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0), #Nose, LEye, REye, LEar, REar
                    (77,255,255), (77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), #LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
                    (204,77,255), (77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (0, 255, 255)] #LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
        line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
                    (77,255,222), (77,196,255), (77,135,255), (191,255,77), (77,255,77), 
                    (77,222,255), (255,156,127), 
                    (0,127,255), (255,127,77), (0,77,255), (255,77,36)]
    elif format == 'mpii':
        l_pair = [
            (8, 9), (11, 12), (11, 10), (2, 1), (1, 0),
            (13, 14), (14, 15), (3, 4), (4, 5),
            (8, 7), (7, 6), (6, 2), (6, 3), (8, 12), (8, 13)
        ]
        p_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
        line_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
    else:
        raise NotImplementedError
        
    #print(im_res) #added by ashvini   
#     im_name = im_res['imgname'].split('/')[-1]
#     im_name = im_res[2]
    #print(frame.shape)
    img = np.zeros((360,640,3),np.uint8)  #image=frame #added by ashvini
    height,width = img.shape[:2]
    img = cv2.resize(img,(int(width/2), int(height/2)))
#     for human in im_res:
    part_line = {}
    kp_preds =  torch.Tensor(list(zip(im_res[3:20],im_res[20:37])))
    #added by ashvini start here
    y = kp_preds[:,0]
    x = kp_preds[:,1]
    y_stand = 90.0
    x_stand = 160.0
    norm_y = max(y)-min(y)
    norm_x = max(x)-min(x)
    y_c = (max(y)+min(y))/2
    x_c = (max(x)+min(x))/2
    #print(norm_y, norm_x)
    kp_preds[:,0] = (((kp_preds[:,0]-y_c)/norm_y)*y_stand)+y_c
    kp_preds[:,1] = (((kp_preds[:,1]-x_c)/norm_x)*x_stand)+x_c
    print(len(kp_preds))
    #print(kp_preds)
    #print("zero",kp_preds[:,0],type(kp_preds))
    #added by ashvini end here
    kp_scores =torch.Tensor(im_res[37:54]).unsqueeze(1)
    print(kp_scores.shape)
    kp_preds = torch.cat((kp_preds, torch.unsqueeze((kp_preds[5,:]+kp_preds[6,:])/2,0)))
    kp_scores = torch.cat((kp_scores, torch.unsqueeze((kp_scores[5,:]+kp_scores[6,:])/2,0)))
    # Draw keypoints
    for n in range(kp_scores.shape[0]):
        if kp_scores[n] <= 0.05:
            continue
        cor_x, cor_y = int(kp_preds[n, 0]), int(kp_preds[n, 1])
        part_line[n] = (int(cor_x/2), int(cor_y/2))
        bg = img.copy()
        cv2.circle(bg, (int(cor_x/2), int(cor_y/2)), 2, p_color[n], -1)
        # Now create a mask of logo and create its inverse mask also
        transparency = max(0, min(1, kp_scores[n]))
        img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)
    # Draw limbs
    '''
    for i, (start_p, end_p) in enumerate(l_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            bg = img.copy()

            X = (start_xy[0], end_xy[0])
            Y = (start_xy[1], end_xy[1])
            mX = np.mean(X)
            mY = np.mean(Y)
            length = ((Y[0] - Y[1]) ** 2 + (X[0] - X[1]) ** 2) ** 0.5
            angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
            stickwidth = (kp_scores[start_p] + kp_scores[end_p]) + 1
            polygon = cv2.ellipse2Poly((int(mX),int(mY)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
            cv2.fillConvexPoly(bg, polygon, line_color[i])
            #cv2.line(bg, start_xy, end_xy, line_color[i], (2 * (kp_scores[start_p] + kp_scores[end_p])) + 1)
            transparency = max(0, min(1, 0.5*(kp_scores[start_p] + kp_scores[end_p])))
            img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)'''
    img = cv2.resize(img,(width,height),interpolation=cv2.INTER_CUBIC)
    return img


# In[7]:


def vis_frame(im_res, format='coco'):
    '''
    frame: frame image
    im_res: im_res of predictions
    format: coco or mpii

    return rendered image
    '''
    if format == 'coco':
        l_pair = [
            (0, 1), (0, 2), (1, 3), (2, 4),  # Head
            (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
            (17, 11), (17, 12),  # Body
            (11, 13), (12, 14), (13, 15), (14, 16)
        ]

        p_color = [(0, 255, 255), (0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0), #Nose, LEye, REye, LEar, REar
                    (77,255,255), (77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), #LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
                    (204,77,255), (77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (0, 255, 255)] #LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
        line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
                    (77,255,222), (77,196,255), (77,135,255), (191,255,77), (77,255,77), 
                    (77,222,255), (255,156,127), 
                    (0,127,255), (255,127,77), (0,77,255), (255,77,36)]
    elif format == 'mpii':
        l_pair = [
            (8, 9), (11, 12), (11, 10), (2, 1), (1, 0),
            (13, 14), (14, 15), (3, 4), (4, 5),
            (8, 7), (7, 6), (6, 2), (6, 3), (8, 12), (8, 13)
        ]
        p_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
        line_color = [PURPLE, BLUE, BLUE, RED, RED, BLUE, BLUE, RED, RED, PURPLE, PURPLE, RED, RED, BLUE, BLUE]
    else:
        raise NotImplementedError
        
    #print(im_res) #added by ashvini   
#     im_name = im_res['imgname'].split('/')[-1]
#     im_name = im_res[2]
    #print(frame.shape)
    img = np.zeros((360,640,3),np.uint8)  #image=frame #added by ashvini
    height,width = img.shape[:2]
    img = cv2.resize(img,(int(width/2), int(height/2)))
#     for human in im_res:
    part_line = {}
    kp_preds =  torch.Tensor(list(zip(im_res[3:20],im_res[20:37])))
    #added by ashvini start here
#     y = kp_preds[:,0]
#     x = kp_preds[:,1]
#     y_stand = 90.0
#     x_stand = 160.0
#     norm_y = max(y)-min(y)
#     norm_x = max(x)-min(x)
#     y_c = (max(y)+min(y))/2
#     x_c = (max(x)+min(x))/2
#     #print(norm_y, norm_x)
#     kp_preds[:,0] = (((kp_preds[:,0]-y_c)/norm_y)*y_stand)+y_c
#     kp_preds[:,1] = (((kp_preds[:,1]-x_c)/norm_x)*x_stand)+x_c
#     print(len(kp_preds))
    #print(kp_preds)
    #print("zero",kp_preds[:,0],type(kp_preds))
    #added by ashvini end here
    kp_scores =torch.Tensor(im_res[37:54]).unsqueeze(1)
#     print(kp_scores.shape)
    kp_preds = torch.cat((kp_preds, torch.unsqueeze((kp_preds[5,:]+kp_preds[6,:])/2,0)))
    kp_scores = torch.cat((kp_scores, torch.unsqueeze((kp_scores[5,:]+kp_scores[6,:])/2,0)))
    # Draw keypoints
    for n in range(kp_scores.shape[0]):
        if kp_scores[n] <= 0.05:
            continue
        cor_x, cor_y = int(kp_preds[n, 0]), int(kp_preds[n, 1])
        part_line[n] = (int(cor_x/2), int(cor_y/2))
        bg = img.copy()
        cv2.circle(bg, (int(cor_x/2), int(cor_y/2)), 2, p_color[n], -1)
        # Now create a mask of logo and create its inverse mask also
        transparency = max(0, min(1, kp_scores[n]))
        img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)
    # Draw limbs
    
    for i, (start_p, end_p) in enumerate(l_pair):
        if start_p in part_line and end_p in part_line:
            start_xy = part_line[start_p]
            end_xy = part_line[end_p]
            bg = img.copy()

            X = (start_xy[0], end_xy[0])
            Y = (start_xy[1], end_xy[1])
            mX = np.mean(X)
            mY = np.mean(Y)
            length = ((Y[0] - Y[1]) ** 2 + (X[0] - X[1]) ** 2) ** 0.5
            angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
            stickwidth = (kp_scores[start_p] + kp_scores[end_p]) + 1
            polygon = cv2.ellipse2Poly((int(mX),int(mY)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
            cv2.fillConvexPoly(bg, polygon, line_color[i])
            #cv2.line(bg, start_xy, end_xy, line_color[i], (2 * (kp_scores[start_p] + kp_scores[end_p])) + 1)
            transparency = max(0, min(1, 0.5*(kp_scores[start_p] + kp_scores[end_p])))
            img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)
    img = cv2.resize(img,(width,height),interpolation=cv2.INTER_CUBIC)
    return img


# In[8]:


path= './tracks_npy_train_new/'
files = sorted(os.listdir(path))
for file in files:
    os.makedirs('./tracks_npy_train_new_vis/'+file)
    data= np.load(path+file)
    for im_res in data:
        im_name = im_res[2]
        img= vis_frame(im_res)
        new_path = os.path.join('./tracks_npy_train_new_vis/', file, str(im_name)+'.jpg')
        print(new_path)
        cv2.imwrite(new_path, img)


# ## Find mean of the dataset

# In[33]:


def find_mean(im_res):
#     img = np.zeros((360,640,3),np.uint8)
#     img = cv2.resize(img,(int(width/2), int(height/2)))
#     part_line = {}
    kp_preds =  torch.Tensor(list(zip(im_res[3:20],im_res[20:37])))
    y = kp_preds[:,0]
    x = kp_preds[:,1]
    y_stand = (max(y)+min(y))/2
    x_stand = (max(x)+min(x))/2
#     norm_y = max(y)-min(y)
#     norm_x = max(x)-min(x)
#     y_c = (max(y)+min(y))/2
#     x_c = (max(x)+min(x))/2
    #print(norm_y, norm_x)
#     kp_preds[:,0] = (((kp_preds[:,0]-y_c)/norm_y)*y_stand)+y_c
#     kp_preds[:,1] = (((kp_preds[:,1]-x_c)/norm_x)*x_stand)+x_c
#     print(len(kp_preds))
    #print(kp_preds)
    #print("zero",kp_preds[:,0],type(kp_preds))
    #added by ashvini end here
#     kp_scores =torch.Tensor(im_res[37:54]).unsqueeze(1)
#     print(kp_scores.shape)
#     kp_preds = torch.cat((kp_preds, torch.unsqueeze((kp_preds[5,:]+kp_preds[6,:])/2,0)))
#     kp_scores = torch.cat((kp_scores, torch.unsqueeze((kp_scores[5,:]+kp_scores[6,:])/2,0)))
    return y_stand,x_stand
    


# In[42]:


files = os.listdir('./tracks_npy/')
path = './tracks_npy/'
y = list()
x = list()
for file in files:
    data= np.load(path+file)
    for im_res in data:
        y_stand,x_stand = find_mean(im_res)
        y.append(y_stand)
        x.append(x_stand)
    
    break
    
    


# In[43]:


print(np.mean(y))
print(np.mean(x))

