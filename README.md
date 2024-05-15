# ORB-SLAM3 
### [Link to original ORB-SLAM3's README.md](https://github.com/UZ-SLAMLab/ORB_SLAM3)

# Ubuntu 20.04 in wsl2

Before beginning, you need to install a 20.04 version of Ubuntu on WSL2.
You can check the different [commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands) to handle WSL  

Open a terminal in administrator mode and enter this command : 
```
wsl --install Ubuntu-20.04
```
Then launch the wsl command prompt by entering ``wsl``.  

And create a user/password.  

Recreate and figer le fichier /etc/resolv.conf :
````
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 192.168.5.13" > /etc/resolv.conf'
sudo chattr +i /etc/resolv.conf
````

Modifier le fichier /etc/wsl.conf :

````
sudo bash -c 'echo "[network]" > /etc/wsl.conf'
sudo bash -c 'echo "generateResolvConf = false" >> /etc/wsl.conf'
````
Then, update packages list : ```sudo apt update```  

Now that you have a functionnal Ubuntu distribution working, you need to install the followings :

### Cmake 

```
sudo apt install cmake
```
### C++ Compiler
```
sudo apt install g++
```
### OpenGL Development Libraries
```
sudo apt install mesa-common-dev libgl1-mesa-dev
```
```
sudo apt install libglew-dev
```

# Installation of ROS NOETIC
Now that you have a working Ubuntu environment, you need to install ROS.
The ROs version that works on Ubuntu 20.04 is [ROS Noetic](https://wiki.ros.org/noetic).  


Setup your computer to accept software from packages.ros.org.
````
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
````
Set up your keys
````
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
````
First, make sure your Debian package index is up-to-date:
````
sudo apt update
````
Desktop-full istallation 
````
sudo apt install ros-noetic-desktop-full
````

You must source this script in every bash terminal you use ROS in.
````
source /opt/ros/noetic/setup.bash
````
It can be convenient to automatically source this script every time a new shell is launched. These commands will do that for you.
````
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
````

### Dependencies for building packages
Up to now you have installed what you need to run the core ROS packages. To create and manage your own ROS workspaces, there are various tools and requirements that are distributed separately. For example, rosinstall is a frequently used command-line tool that enables you to easily download many source trees for ROS packages with one command.

To install this tool and other dependencies for building ROS packages, run:

````
sudo apt install python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
````
### Initialize rosdep
Before you can use many ROS tools, you will need to initialize rosdep. rosdep enables you to easily install system dependencies for source you want to compile and is required to run some core components in ROS. If you have not yet installed rosdep, do so as follows.
````
sudo apt install python3-rosdep
````
With the following, you can initialize rosdep :
````
sudo rosdep init
rosdep update
````

Install the usb_cam package that we will need afterwards : 
```` 
sudo apt install ros-noetic-usb-cam
````

# Installation of ORB-SLAM 3
Now that you have ROS installed and working on your Ubuntu, you can install ORB-SLAM3.
## Dependencies 
Install all the dependencies needed : 
````
sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
sudo apt update

sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev

sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libdc1394-22-dev libjasper-dev

sudo apt-get install libglew-dev libboost-all-dev libssl-dev

sudo apt install libeigen3-dev
````
## Prerequisites
#### Pangolin 
Install Pangolin in ~
````
cd ~
git clone https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
mkdir build && cd build
cmake ..
make
sudo make install
````

#### OpenCV

Check the OpenCV version on your computer (required at leat 3.0 as stated in the original README.md):
````
python3 -c "import cv2; print(cv2.__version__)"
````
On a freshly installed Ubuntu 20.04.4 LTS with desktop image, OpenCV 4.2.0 is included.
## Build
In order to build the project, do the following
 * Clone this repository in ~:
````
cd ~
git clone https://github.com/MarinHure/ORB_SLAM3_WSL.git ORB_SLAM3
````
This repository incorporates changes to the source code  necessary to build successfully. For Ubuntu 20.04, it changes CMakeList from C++11 to C++14.  

 * Build
````
cd ORB_SLAM3
chmod +x build.sh
./build.sh
````
 * Make sure that libORB_SLAM3.so is created in the ORB_SLAM3/lib folder. If not, check the issue list from the [original repo](https://github.com/UZ-SLAMLab/ORB_SLAM3/issues) and retry.

# ORB-SLAM3 ros wrapper
The ROS wrapper for ORb-SLAM 3 should be a catkin build workspace, so let's create one.
## Create a ROS catkin workspace
Let's create and build a catkin workspace:

````
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/
````

## Clone the package.
You will need to install and build a ROS package for ORB-SLAM 3 :  

* Install catkin
````
sudo apt-get install python3-catkin-tools
````
* Create a catkin workspace :
````
cd ~/catkin_ws/src/
git clone https://github.com/thien94/orb_slam3_ros_wrapper.git
````
* Open CMakeLists.txt and change the directory that leads to ORB-SLAM3 library at the beginning of the file.
````
cd ~/catkin_ws/src/orb_slam3_ros_wrapper/
nano CMakeLists.txt
````
Change this to your installation of ORB-SLAM3. Default is ~/Packages/
````
set(ORB_SLAM3_DIR
   $ENV{HOME}/ORB_SLAM3
)
````

* Build the package normally.
````
cd ~/catkin_ws/
catkin build
````
* Add the setup file to the bashrc so that it is sourced every time you launch the terminal 
````
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
````
To make sure your workspace is properly overlayed by the setup script, make sure ROS_PACKAGE_PATH environment variable includes the directory you're in.
````
echo $ROS_PACKAGE_PATH
````
You should see
````
/home/youruser/catkin_ws/src:/opt/ros/noetic/share
````

Next, copy the ``ORBvoc.txt`` file from ``ORB-SLAM3/Vocabulary/`` folder to the ``config`` folder in this package. Alternatively, you can change the voc_file param in the launch file to point to the right location.

````
cp ~/ORB_SLAM3/Vocabulary/ORBvoc.txt ~/catkin_ws/src/orb_slam3_ros_wrapper/config/
````
### (Optional) hector-trajectory-server
Install hector-trajectory-server to visualize the real-time trajectory of the camera/imu. Note that this real-time trajectory might not be the same as the keyframes' trajectory.
````
sudo apt install ros-noetic-hector-trajectory-server
````


## Run ORB-SLAM3 with a dataset 
* Download the bag : 
````
wget http://robotics.ethz.ch/~asl-datasets/ijrr_euroc_mav_dataset/machine_hall/MH_01_easy/MH_01_easy.bag
````
* In one terminal, launch the node:
````
roslaunch orb_slam3_ros_wrapper euroc_monoimu.launch
````
It should launch the interface.  

* In a second terminal, playback the bag:
````
rosbag play MH_01_easy.bag
````
It should display the video, and the points generated from it.

# Share the USB camera from windows to Ubuntu

Natively, you cannot use a usb camera in WSL, so when you try to run ORB-SLAM 3, you shall receive this error message *Cannot identify '/dev/video0': 2, No such file or directory*.  
You need to follow these steps to allow the use of the camera by your Ubuntu distribution.  

## Install usbipd 
To share your usb device to your Ubuntu wsl environment, you need to download usbipd (here is the [Windows documentation](https://learn.microsoft.com/fr-fr/windows/wsl/connect-usb)).  
https://github.com/dorssel/usbipd-win/releases/tag/v4.1.0  

In a DOS console as administrator (Windows) : 
````
usbipd list
````
If you installed usbipd correctly, you should see the a list of the different usb devices plugged to your Windows computer.  

## Launch WSL, prepare and build the kernel

* Update WSL
````
wsl --update
````
* Launch wsl
````
wsl
````
* Update resources 
````
sudo apt update
sudo apt upgrade
````

* Install prerequisites
````
sudo apt install build-essential flex bison libssl-dev libelf-dev libncurses-dev autoconf libudev-dev libtool bc dwarves
````
Clone kernel that matches WSL version. To find the version you can run.
````
uname -r
````
The kernel can be found at: https://github.com/microsoft/WSL2-Linux-Kernel

* Clone the kernel repo, then checkout the branch/tag that matches your kernel version.  
 run ``uname -r`` to find the kernel version, for me it is **5.15.146.1-microsoft-standard-WSL2+**, so i identified the  **linux-msft-wsl-5.15.146.1** tag.
````
cd ~
git clone https://github.com/microsoft/WSL2-Linux-Kernel.git
cd WSL2-Linux-Kernel
git checkout linux-msft-wsl-5.15.146.1
````
* Copy current configuration file.
````
cp /proc/config.gz config.gz
gunzip config.gz
mv config .config
````
* Run menuconfig to select kernel features to add.
````
sudo make menuconfig
````  

These are the necessary additional features in menuconfig.  
  

Device Drivers -> USB Support  
Device Drivers -> USB Support -> USB announce new devices  
Device Drivers -> USB Support -> USB Modem (CDC ACM) support  
Device Drivers -> USB Support -> USB/IP  
Device Drivers -> USB Support -> USB/IP -> VHCI HCD  
Device Drivers -> USB Support -> USB Serial Converter Support  
Device Drivers -> USB Support -> USB Serial Converter Support -> USB FTDI Single port Serial Driver  
Device Drivers -> USB support -> USB Gadget Support
Device Drivers -> USB support -> USB Gadget Support -> USB Gadget precomposed configurations -> USB Webcam Gadget 
Device Drivers -> Multimedia support 
Device Drivers -> Multimedia support -> Media drivers -> Media USB Adapters  
Device Drivers -> Multimedia support -> Media drivers -> Media USB Adapters -> USB Video Class  

````
sudo make -j$(nproc) && sudo make modules_install -j$(nproc) && sudo make install -j$(nproc)
````

* From the root of the repo, copy the image.
````
mkdir /mnt/c/Sources/
````
````
cd ~/WSL2-Linux-Kernel
ls
````
You should see a **vmlinux** file
````
sudo cp -rf vmlinux /mnt/c/Sources/
````
* Create a .wslconfig file on **/mnt/c/Users/<username>/** and add a reference to the created image with the following :

````
echo "[wsl2]" > /mnt/c/Users/<username>/.wslconfig && echo "kernel=c:\\Sources\\vmlinux" >> /mnt/c/Users/<username>/.wslconfig
````
## Test your installation 

* Reboot your windows.

* Launch Ubuntu WSL 
````
wsl
````

* Check kernel support in WSL
````
uname -r
````

* Check the different usb devices plugged (in a Windows terminal)

````
usbipd list
````

* Identify the busid of the usb camera you want to share, and share it with wsl
````
usbipd bind -b 1-10
````
Here it is **1-10**

* Attach the webcam to WSL with usbipd (in Windows)
````
usbipd attach --wsl --busid 1-10
````

* Check in WSL
````
lsusb
ls /dev/video*
````
Change the permissions to the video files.
````
sudo chmod 777 /dev/video*
````
It should display the camera files in /dev/.

* Install guvcview and display the camera images 
````
sudo apt install guvcview
guvcview
````

# Run ORB-SLAM 3

In file **~/catkin_ws/src/orb_slam3_ros_wrapper/src/mono_node.cc**, line 65, change **camera** to **usb_cam**

````
ros::Subscriber sub_img0 = node_handler.subscribe("/usb_cam/image_raw", 1, &ImageGrabber::GrabImage, &igb);`
````

Now that you have a working Ubuntu distribution, with ROS, the ORB-SLAM3 ROS wrapper, and that you have allowed tht use of the camera for your Ubuntu environment, you an run ORB-SLAM 3. 

In one terminal use this command to start up the server : 
````
roscore
````

In another terminal run this command to change to usb camera mode :
````
rosrun usb_cam usb_cam_node
````  

Then Launch the orb_slam3 process :
````
roslaunch orb_slam3_ros_wrapper euroc_mono.launch
````


