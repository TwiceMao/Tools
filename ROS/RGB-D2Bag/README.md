**MyImg2Bag.py** ：Convert an RGB-D image sequence to a ROS bag, including timestamp, camera internal reference, image height and width, and frame_id.

Example of launching the MyImg2Bag.py script (requires ROS to be installed):

```python
conda create -n Img2Ros python=3.8

pip install rospkg
pip install catkin_pkg
pip install empy     
pip install  lark
pip install gnupg
pip install pycryptodomex
pip install opencv-pthon


python ./MyImg2Bag.py ./Data/office_0/ ./Output/rgbd_office.bag ./Data/timestamps15.txt ./Data/ReplicaCameraInfo.yaml
```



Example script for converting a **ROS bag to a ROS2 bag**:

```python
pip install rosbags
cd Output
rosbags-convert rgbd_office.bag
```

