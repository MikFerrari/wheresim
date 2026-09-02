

# What is Wheresim?

Wheresim is a reduced version of Locosim didactic framework for the WHERE summer school to learn/test basic controllers schemes on quadruped robots. Locosim has been successfully tested on Aliengo and Go1, Go2 robots. If you just bought a Go1 robot and you want to give a try, follow this [wiki](https://github.com/mfocchi/locosim/blob/develop/figs/go2_setup.md)!

Locosim is composed by a **roscontrol** node called **ros_impedance_controller** (written in C++) that interfaces a python ROS node (where the controller is written) to a Gazebo simulator. 

You have 2 ways to get the Locosim code:  1) with docker 2) by manual installation of dependencies.

**Note**: If you intend to use Locosim for your *research* please cite:

- M. Focchi, F. Roscia, C. Semini, **Locosim: an Open-Source Cross-Platform Robotics Framework**, Synergetic Cooperation between Robots and Humans. CLAWAR, 2023.  

  you can download a pre-print of the paper [here](https://iit-dlslab.github.io/papers/focchi23clawar.pdf). [View BibTeX](https://github.com/mfocchi/locosim/blob/develop/locosim.bib)

 

# Docker Installation

You can alternatively use a docker image that contains Ubuntu 20 and all the required dependencies already installed (you will need only to clone the code and compile it).

**LINUX**: follow this  [procedure](https://github.com/idra-lab/locosim/blob/master/install_docker_linux.md).

**MAC:** follow this  [procedure](https://github.com/idra-lab/locosim/blob/master/install_docker_mac.md).

**WINDOWS:** follow this [procedure](https://github.com/idra-lab/locosim/blob/master/install_docker_windows.md).



# Native Installation 

**LINUX:** follow this [procedure](https://github.com/idra-lab/locosim/blob/master/install_native.md).

**MAC:** follow this [procedure](https://github.com/idra-lab/locosim/blob/master/install_native.md), just replace **"sudo apt install package_name"** with **"brew install package_name"**.

**WINDOWS:** Install Ubuntu 20.4.06 LTS  following this procedure: https://ubuntu.com/tutorials/install-ubuntu-on-wsl2-on-windows-11-with-gui-support#1-overview

If you experiment any issue in using the Nvidia with  OpenGL rendering (the symptom is that you cannot visualize STL meshes in RVIZ) then you should update to the latest mesa-driver:

```
sudo add-apt-repository ppa:kisak/kisak-mesa
sudo apt update
sudo apt install mesa-utils
```

then follow this [procedure](https://github.com/idra-lab/locosim/blob/master/install_native.md).



# **Running the software from Python IDE: Pycharm**

Now that you compiled the code you are ready to run the software! 

We recommend to use an IDE to run and edit the python files, like Pycharm community. 

1. To install it, enter in the $HOME folder of the docker and download it from here:

```
$ wget https://download.jetbrains.com/python/pycharm-community-2021.1.1.tar.gz
```

2. Then, unzip the program:

```
$tar -xf pycharm-community-2021.1.1.tar.gz
```

 and unzip it  *inside* the docker (e.g. copy it inside the `~/trento_lab_home` folder. 

**IMPORTANT**!** I ask you to download this specific version (2021.1.1) that I am sure it works, because the newer ones seem to be failing to load environment variables! 

3. To run Pycharm community type (if you are lazy you can create an alias...): 

```
$ pycharm-community-2021.1.1/bin/pycharm.sh
```

Running pycharm from the terminal enables to use the environment variables loaded inside the .bashrc.

4. click "Open File or Project" and open the folder robot_control. Then launch one of the labs in locosim/robot_control/lab_exercises or in locosim/robot_control/base_controllers  (e.g. ur5_generic.py)  right click on the code and selecting "Run File in Pyhton Console"

5. the first time you run the code you will be suggested to select the appropriate interpreter (/usr/binpython3.8). Following this procedure you will be sure that the run setting will be stored, next time that you start Pycharm.



# Running the Software from terminal

To run from a terminal we  use the interactive option that allows  when you close the program have access to variables:

```
$ python3 -i $LOCOSIM_DIR/robot_control/base_controllers/base_controller.py
```

to exit from python3 console type CTRL+Z



Installing NVIDIA drivers (optional)
==============

If your PC is provided with an NVIDIA graphics card, you can install its drivers in Ubuntu by following these steps:

add the repository

```
sudo add-apt-repository ppa:graphics-drivers/ppa
```

update the repository list:

```
sudo apt-get update
```

Install the driver, note that for Ubuntu 20.04 the 515 version is ok, for Ubuntu 22.04 the 535 is ok, but you can use also other versions:

```
sudo apt-get install nvidia-driver-X
```

The reboot the system

```
sudo reboot
```

Now tell the system to use that driver:

* open the _Software & Updates_ application
* go to "Additional Drivers" and select the latest driver you just installed with "proprietary, tested" description
* press on "Apply Changes".

You can verify if the drivers are installed by opening a terminal and running:

```
nvidia-smi
```

If this does not work, and you are sure you correctly installed the drivers, you might need to deactivate the "safe boot" feature from your BIOS, that usually prevents to load the driver. 

### Go2 Quadruped Robot

and follow this [wiki](https://github.com/mfocchi/locosim/blob/develop/go1_setup.md)!

