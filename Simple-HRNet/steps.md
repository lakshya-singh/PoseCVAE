Following steps are needed to perform preprocessing on datasets:

Step 1: Run generate_pose.py on train and test videos seperately, this will extract pose of each individual in a video and will save it in json file per video
File: generate_pose.py
Inputs: path--> path of videos from which pose to be extracted
        out_path--> path to save json file

Outputs: json file per video containing pose keypoint per frame per individual with name:  "output.json"
Note: To generate .csv files intead of .json, simply replace json in "os.system" line with csv in generate_pose.py

Helpful Tip: Before running the next step, keep a copy of Frames aside as next step edits the contents of frames folders and renders them useless for future use in training/testing

Step 2: Now go inside folder PoseFlow and run generate_track.py, this will assign ID to each individual by tracking them throughout the video and saving a json file per video
File: generate_track.py
Inputs: path--> give path of frames on which tracker will be applied (same as step 1)
        in_json--> path to json file from the output of step 1
        out_json--> path to save tracker json file
        
Outputs: json file per video containing tracks of each individual with an ID assigned, name of each file: alphapose-results-forvis-tracked.json

 -----------------------------------------------------------------------------------------------
Friendly Advice: Step 2 takes lot of time to generate results, so its better to run it once on all the datasets and obtain final tracked json file for furhter easy file manipulation steps.
 
 
Step 3: Run generate_npy.py, which converts json to npy file. Each npy file containes continuous tracks and as soon as tracks breaks a new file is created for same person.
File: generate_npy.py
Inputs: path--> path to json file obtained from step2
         save_path--> path to save generate_npy files

Outputs: npy file per continuous track per person. Format: save_path/generate_npy/video_name/personID_tracknum
 
 
Step 4: Run final_npy.py, this file is for getting desired format for each list element inside npy file(obtained from step 3)
File: final_npy.py
Inputs: path--> path to generate_npy folder(from step3)
         save_path--> path to save final_npy files
 
Outputs: npy files in the following format: save_path/final_npy/video_name/personID_tracknum
 ------------------------------------------------------------------------------------------------
Friendly Advice: Above 2 steps also require one time run so output can be saved and used as per requirement

Sliding Window Procedure:

Step 5: Run sliding.py on train and test final_npy files(obtained from step 4) to obtain data in sliding window format.
File: sliding.py
Inputs: sliding_win_len--> length of sliding window(ex. 3,7,13,25)
        path--> path to final_npy folder(output of step 4)
        save_path--> path to save output of sliding window

Outputs: tracks with sliding window applied and trackes smaller than twice of sliding window will be ignored.
 -------------------------------------------------------------------------------------------------
 
 Some additional files:
 visualize.py and visualize_pose.py: helps in visualizing poses 
 
 
