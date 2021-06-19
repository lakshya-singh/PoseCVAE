1. Put the frames folder for each training video in ./frames directory
2. Divide sliding_window outputs created from training videos into training set and validation set and keep the divided sliding_window folders in corresponding "sliding_window_train" and "sliding_window_val" folders
3. Run houseKeeping.py once each time you follow step 2

For Training:
1. Before each training session, create new ./checkpoints and ./log using "mkDirs.py". You will also have to move ./checkpoints and ./log directories after each training session to some folder.

   Helpful Tip: Move the two folders in a new folder in ./training/ only

2. You can either run "combined_stages.py" to train all three stages at once OR you can run each stage{x}.py individually.
3. If running stage_combined.py, you will have to search for and specify - n_epochs, pretr, tr once
4. If running each stage individually, you will have to specify - n_epochs, pretr, tr in all three stage{x}.py files individually
   And also specify which ".pth" checkpoint file is being loaded in each of stage 2 and 3 at (or around) "line 395" in the code

Note: The benefit of running each stage seperately is that, you control beginning point of each stage (i.e. train_loss at the beginning epoch of each stage, which if comes high, you can run that stage again till you are satisfied with a low train_loss at the 1st epoch of that stage). This generally helps in quick convergence of training loss to a low value.
