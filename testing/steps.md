1. Put the checkpoint '.pth' file you want to use for testing, in ./checkpoint/ folder
2. Put different testing_videos frame folders in ./frames/
3. Put the sliding_window output folders of testing_videos in ./sliding_window/
4. You will have to move final_mse and mse_plots into some folder after each testing session

Helpful Tip: Move the checkpoint '.pth' file used to create final_mse and mse_plots in the same folder as both of them to avoid future hassle of searching for weights of a good performing model.

5. ./auc folder contains text file saving auc score of testing with date-time stamp


Note: "mkResult.py" and "rmResult.py" will be useful when you are testing multiple times.
      They help in creating and removing ./sliding_window/[particular_video_name_folder]/result folder as it is populated each time you test
      The ground_truth folder by default contains ground truth files for CUHK Avenue Dataset
