import time, sys, os
import numpy as np
from ros import rosbag
import roslib
import rospy
import cv2
roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import yaml
from sensor_msgs.msg import CameraInfo
# import ImageFile
from PIL import ImageFile
from PIL import Image as ImagePIL

def yaml_to_CameraInfo(yaml_fname):
    # Load data from file
    with open(yaml_fname, "r") as file_handle:
        calib_data = yaml.full_load(file_handle)
    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.width = calib_data["image_width"]
    camera_info_msg.height = calib_data["image_height"]
    camera_info_msg.K = calib_data["camera_matrix"]["data"]
    camera_info_msg.D = calib_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calib_data["rectification_matrix"]["data"]
    camera_info_msg.P = calib_data["projection_matrix"]["data"]
    camera_info_msg.distortion_model = calib_data["distortion_model"]
    camName=calib_data["camera_name"]
    return camera_info_msg,camName

'''get image from dir'''
def GetFilesFromDir(dir):
    '''Generates a list of files from the directory'''
    print( "Searching directory %s" % dir )
    color_image = []
    multi_imgs = []

    if os.path.exists(dir):
        for path, names, files in os.walk(dir + 'rgb'):
            for f in sorted(files):
                color_image.append( os.path.join( path, f ) )
        for path, names, files in os.walk(dir + 'depth'):
            for f in sorted(files):
                multi_imgs.append( os.path.join( path, f ) )

    return color_image, multi_imgs

def CreateMonoBag(color_imgs, multi_imgs, bagname, timestamps,yamlName):
    
    '''read time stamps'''
    file = open(timestamps, 'r')
    timestampslines = file.readlines()
    file.close()
    '''Creates a bag file with camera images'''
    bag =rosbag.Bag(bagname, 'w')
    cb = CvBridge()

    try:
        my_frame_id = "r0_link"
        for i in range(len(color_imgs)):
            # A factor of 10 is used to adjust the time.txt timestamp
            Stamp = rospy.rostime.Time.from_sec(float(timestampslines[i]))
            print(i,Stamp)
            
            [calib, cameraName]=yaml_to_CameraInfo(yamlName)
            calib.header.stamp = Stamp
            calib.header.seq = i
            calib.header.frame_id = my_frame_id

            img_color = cv2.imread(color_imgs[i], cv2.IMREAD_UNCHANGED)
            print("Adding %s" % color_imgs[i])

            multi_color = cv2.imread(multi_imgs[i], cv2.IMREAD_UNCHANGED)
            multi_color = multi_color.astype(np.float32)
            multi_color /= 6553.5
            
            if(1 == i):
                print('depth verify',multi_color[:5,:5])
                print(multi_color.dtype)
            
            print("Adding %s" % multi_imgs[i])

            image_color = cb.cv2_to_imgmsg(img_color, encoding='bgr8')
            image_color.header.stamp = Stamp
            image_color.header.frame_id = my_frame_id

            #multi_color = cb.cv2_to_imgmsg(multi_color, encoding='16UC1')
            multi_color = cb.cv2_to_imgmsg(multi_color, encoding='32FC1')
            multi_color.header.stamp = Stamp
            multi_color.header.frame_id = my_frame_id
            
            bag.write( cameraName + '/color/camera_info', calib, Stamp)
            bag.write(cameraName +'/color/image', image_color, Stamp)
            bag.write(cameraName +'/depth/image', multi_color, Stamp)

            
    finally:
        bag.close()       


def CreateBag(args):
    '''Creates the actual bag file by successively adding images'''
    color_imgs, multi_imgs = GetFilesFromDir(args[0])
    #print(args)

    # create bagfile 
    CreateMonoBag(color_imgs, multi_imgs, args[1], args[2],  args[3])    

if __name__ == "__main__":
    if len( sys.argv ) == 5:
        CreateBag(sys.argv[1:])
    else:
        print( "Usage: img2bag_Stereo.py imagedir bagfilename timestamp")
