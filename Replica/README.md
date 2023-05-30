**Blender2Replica.py** converts the pose exported by blender into processed_poses.txt and traj.txt required by Replica.



**render.cpp**: Modified based on the [Replica dataset](https://github.com/facebookresearch/Replica-Dataset) (ReplicaSDK/src/render.cpp). Need to input processed_poses.txt, render and generate corresponding RGB-D image.

Note that the processed_poses.txt is not camera 2 world. but
$$
processed\_poses.txt = (c2w^{-1})^T
$$


```python
# Replica code dependencies
sudo apt-get install build-essential libgl1-mesa-dev
sudo apt-get install libglew-dev libsdl2-dev libsdl2-image-dev libglm-dev libfreetype6-dev
sudo apt-get install libglfw3-dev libglfw3
sudo apt-get install mesa-utils
sudo apt-get install libjpeg-dev libpng12-dev libtiff5-dev libopenexr-dev  
sudo apt-get install libjpeg-dev
sudo apt-get install doxygen
```



After building the Replica project according to [Replica dataset](https://github.com/facebookresearch/Replica-Dataset/tree/main#:~:text=to%20download%20Replica.-,Replica%20SDK,-Setup) 

We render images by scripts（Camera and image parameters are consistent with those provided by [iMAP](https://openaccess.thecvf.com/content/ICCV2021/html/Sucar_iMAP_Implicit_Mapping_and_Positioning_in_Real-Time_ICCV_2021_paper.html)）:

```python
cd ~/ImageSave/office0_loop
~/Replica-Dataset/build/ReplicaSDK/ReplicaRenderer ~/RawMaterial/office_0/mesh.ply  ~/RawMaterial/office_0/textures/ 
```

