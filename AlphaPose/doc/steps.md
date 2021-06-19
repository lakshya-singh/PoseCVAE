Following steps are needed to perform preprocessing on datasets:
##### Note: 
1) All datasets are in video format make sure to convert them into frames using ffmpeg (use frames.py available in pytorch branch for conversion of all videos to frames)
2) All steps require Alphapose and Poseflow pytorch branch(available in current repository), so make sure to clone it.

## Pose Trajectory Extraction Procedure

### Step 1:
Run generate_pose.py on train and test frames seperately, this will extract pose of each individual in a frame and will save it in json file per video
- File: generate_pose.py
- Inputs: 
    - path--> path of frames from which pose to be extracted
    - out_path--> path to save json file
- Outputs: json file per video containing pose keypoint per frame per individual with name:  "alphapose-results.json"

If bounding box normalization needed then some changes in dataloader.py(from Alphapose) are needed:
--> Inside dataloader.py instead of importing from "fn" import from fn_norm, this is also mentioned inside dataloader file.


### Step 2: 
Now go inside folder PoseFlow and run generate_track.py, this will assign ID to each individual by tracking them throughout the video and saving a json file per video
- File: generate_track.py
- Inputs: 
    - path--> give path of frames on which tracker will be applied (same as step 1)
    - in_json--> path to json file from the output of step 1
    - out_json--> path to save tracker json file  
- Outputs: json file per video containing tracks of each individual with an ID assigned, name of each file: alphapose-results-forvis-tracked.json

 -----------------------------------------------------------------------------------------------
Friendly Advice: Step 1 and 2 takes lot of time to generate results(2-3 days), so its better to run them once on all the datasets and obtain final tracked json file for furhter easy file manipulation steps.

## JSON to numpy and Desired Format Procedure
### Step 3: 
Run generate_npy.py, which converts json to npy file. Each npy file containes continuous trackes and as soon as trackes breaks a new file is created for same person.
- File: generate_npy.py
- Inputs: 
    - path--> path to json file obtained from step2
- Outputs: npy file per continuous track per person. Format: generate_npy/video_name/personID_tracknum
 
 
### Step 4: 
Run final_npy.py, this file is for getting desired format for each list element inside npy file(obtained from step 3)
- File: final_npy.py
- Inputs: 
    - path--> path to generate_npy folder(from step3)
    - save_path--> path to save final_npy files
- Outputs: npy files in the following format: final_npy/video_name/personID_tracknum

Length: 56

| Index | 0 | 1 | 2 | 3:19 | 20:36 | 37:53 | 54  | 55 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Value | cam_id | video_id | frame_number | 17 x-coordinate for keypoints | 17 y-coordinate for keypoints | 17 confidence score for keypoints | person_id | 0 for train and 1 for test |


 ------------------------------------------------------------------------------------------------
 
Friendly Advice: Above 2 steps also require one time run so output can be saved and used as per requirement

## Sliding Window Procedure
### Step 5: 
Run sliding.py on train and test final_npy files(obtained from step 4) to obtain data in sliding window format.
- File: sliding_train.py
- Inputs: 
    - sliding_win_len--> length of sliding window(ex. 3,7,13,25)
    - path--> path to final_npy folder(output of step 4)
    - save_path--> path to save output of sliding window
- Outputs: tracks with sliding window applied and trackes smaller than twice of sliding window will be ignored.

 -------------------------------------------------------------------------------------------------
 
 Some additional files:
 visualize.py: helps in visualizing poses 
 
 
