-------------------------------------------------------------------------------------------------------------------------------------------
Note: HRNet requires CUDA driver version 10 while AlphaPose works with version 9

      If using HRNet+PoseFlow, generate poses using version 10 and rest of the process using version 9
      If using AlphaPose+PoseFlow, do everything using version 9
-------------------------------------------------------------------------------------------------------------------------------------------
Setting up workable virtual environment:

1) Create two seperate anaconda environments for AlphaPose and simple-HRNet to avoid any possible conflicts as they both have common dependencies. Run [pip install -r requirements.txt] in your environment, in both the folders.

2) Poseflow works in both of those environments. If there is some issue, run [pip install -r requirements.txt] inside PoseFlow.
-------------------------------------------------------------------------------------------------------------------------------------------

1) All datasets are in video format make sure to convert them into frames using ffmpeg for tracking using Poseflow

	Step 1: Download Dataset into ./datasets/ and follow readme.txt present in the same

	Step 2: Generate frames using frames.py present in ./frames/ and follow readme.txt present there for further instructions

2) All steps require either AlphaPose and Poseflow OR simple-HRNet and Poseflow, which if need be, pytorch branch can also be cloned from github.

3) Do read the steps.md file present in both alphaPose and simple-HRNet folders to get started.
-------------------------------------------------------------------------------------------------------------------------------------------


