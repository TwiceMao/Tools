# ROS：

```python
pip install rospkg
pip install catkin_pkg
pip install empy     
pip install  lark
pip install gnupg
pip install pycryptodomex

# Note that every time this needs to be executed
source /opt/ros/noetic/setup.bash

rosbag info example.bag
rosbag play ./rgb_office.bag

rostopic list
# view camera_info
rostopic echo /realsense_rgb/camera_info 

# Show images
sudo apt-get install ros-noetic-image-view
rosrun image_view image_view image:=/rgb/color

# Note that in the GUI select the All node\Activate node button
rqt_graph 
```





# ROS2：

```python
sudo apt-get install ros-foxy-rqt
sudo apt-get install ros-foxy-rqt-graph
sudo apt-get install ros-foxy-rqt-common-plugins

source /opt/ros/foxy/setup.bash

ros2 bag play  ./ground-02_0.db3
ros2 topic list
ros2 run image_view image_view image:=/r0/color/image

rqt_graph
ros2 topic hz /r0/color/image
```

