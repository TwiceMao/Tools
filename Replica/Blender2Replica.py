import cv2
import torch
import numpy as np
import glob
import os
from PIL import Image
import os.path
import math
import csv
import pandas as pd

#camera_transforms.txt is the pose exported by Blender, and each pose is a 4*4 matrix.
#traj.txt is the pose of c2w (camera to world), which is a 1*16 matrix, and the difference from camera_transforms.txt is the inverse of the y and z axis rotation.
#processed_poses.txt is the world2camera transformation required by the Replica SDK render.cpp

base_dir = 'YourBaseDir'


path = base_dir + 'camera_transforms.txt'

poses = []
c2ws = []

with open (path,'r') as f:
    pose_txt = f.readlines()

print(pose_txt)
print(len(pose_txt))

for i in range(len(pose_txt)//4):
    tmp_pose = np.zeros((4,4))
    for j in range(4):
        tmp_pose[j,:] = np.array(pose_txt[4*i+j].split(' '))

    tmp_pose[:3,1] *= -1
    tmp_pose[:3,2] *= -1
    c2ws.append(tmp_pose.reshape(-1,))
    
    tmp_pose = np.linalg.inv(tmp_pose)
    tmp_pose = tmp_pose.T
    tmp_pose = tmp_pose.reshape(-1,)
    poses.append(tmp_pose)
c2ws = np.array(c2ws)
np.savetxt(base_dir+'traj.txt', c2ws)

poses = np.array(poses)
np.savetxt(base_dir+'processed_poses.txt', poses)

