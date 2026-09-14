Installation with Docker (Mac, Apple Silicon M1-M5)
================================================================================

This guide adapts the [Linux installation instructions](install_docker_linux.md) for Macs with Apple Silicon (M1, M2, M3, M4, M5). The Docker image `mfocchi/trento_lab_framework:wheresim` is built for the **x86_64/amd64** architecture, so on Apple Silicon it runs through Docker Desktop's Rosetta 2 emulation. It will work, but expect it to be noticeably slower than on a native Linux/x86_64 machine, and there is no GPU (Nvidia) acceleration available.

If you have an Intel Mac, you can follow the same steps; you can ignore the notes about Rosetta emulation and `--platform linux/amd64` is not strictly necessary (but does not hurt).

## 1. Install Docker Desktop and XQuartz

- Install [Homebrew](https://brew.sh/) if you don't already have it.

- Install Docker Desktop and XQuartz (the X11 server needed to display GUI windows such as rviz/Gazebo that run inside the container):

```bash
$ brew install --cask docker
$ brew install --cask xquartz
```

  Alternatively you can install Docker Desktop manually from the [official page](https://docs.docker.com/desktop/install/mac-install/).

- Open **Docker Desktop** once from the Applications folder to complete its setup, and leave it running (check the whale icon in the menu bar).

- In Docker Desktop go to **Settings > General** and enable **"Use Rosetta for x86_64/amd64 emulation on Apple Silicon"**. This significantly improves performance when running the amd64 image.

- **Log out and log back in** (or reboot) after installing XQuartz so that it is registered as the default X11 server.

- Open **XQuartz > Settings > Security** and check **"Allow connections from network clients"**. Restart XQuartz for the change to take effect.

## 2. Run the install script

This script creates the `trento_lab_home` folder that will be mounted inside the container, and (on macOS) installs Docker Desktop via Homebrew if it is missing.

```bash
$ curl -o install_docker.sh https://raw.githubusercontent.com/idra-lab/wheresim/refs/heads/master/docker/install_docker.sh
$ chmod +x install_docker.sh
$ ./install_docker.sh
```

- Unlike on Linux, you do **not** need to reboot the system for Docker to work. Just make sure Docker Desktop is running (open it from Applications if it isn't).
- If you look into your **host** home directory, you will see that the **trento_lab_home** directory has been created with a **ros_ws/src** subfolder.
- Now you can clone the wheresim code inside the **trento_lab_home/ros_ws/src** folder:

```bash
$ cd ~/trento_lab_home/ros_ws/src
$ git clone https://github.com/idra-lab/wheresim.git --recursive
```

**NOTE:** when you clone the code, be sure to have a stable and fast connection. Before continuing, be sure you properly checked out **all** the submodules without any error.

## 3. Get the Docker image

Since the image is built for amd64, always pass `--platform linux/amd64` on Apple Silicon.

- A) Download the docker image from here:

```bash
$ docker pull --platform linux/amd64 mfocchi/trento_lab_framework:wheresim
```

- B) or compile the docker image yourself:

```bash
$ cd ~/trento_lab_home/ros_ws/src/wheresim/docker
$ docker build --platform linux/amd64 -t mfocchi/trento_lab_framework:wheresim -f Dockerfile .
```

## 4. Configure your shell

macOS's default shell is `zsh`, so add the alias to `~/.zshrc` (if you use bash instead, edit `~/.bash_profile` or `~/.bashrc`):

```bash
$ open -e ~/.zshrc
```

and add the following lines at the bottom of the file:

```bash
alias lab_wheresim='open -a XQuartz; \
IP=$(ifconfig en0 | grep "inet " | awk "{print \$2}"); \
xhost + $IP >/dev/null 2>&1; \
docker rm -f where_container >/dev/null 2>&1 || true; \
docker run --name where_container --platform linux/amd64 \
--workdir="/root" \
--env="DISPLAY=$IP:0" \
--env="QT_X11_NO_MITSHM=1" \
--privileged --shm-size 2g --rm \
--volume $HOME/trento_lab_home:/root \
mfocchi/trento_lab_framework:wheresim'
alias where-other='docker exec -it where_container /bin/bash'
```

**NOTE!** Compared to the Linux alias, this version:
- drops `--gpus all` and `--device=/dev/dri`, since there is no Nvidia GPU / DRI device passthrough available on macOS;
- drops `--network=host`, which Docker Desktop for Mac does not support the same way Linux does; if some part of the software needs to reach a service running on your host Mac, use `host.docker.internal` instead of `localhost` from inside the container (this hostname is provided automatically by Docker Desktop on Mac);
- sets `DISPLAY` to your Mac's Wi-Fi/Ethernet IP (`en0`) instead of `$DISPLAY`, and uses `xhost` to authorize that IP, since macOS has no native X11 server/socket to share with the container — GUI windows are instead forwarded over TCP to XQuartz. If `en0` is not your active network interface (e.g. you are on Ethernet), replace it with the correct one (check with `ifconfig`).

- Load the updated shell config (next time you open a terminal this will be automatically loaded):

```bash
$ source ~/.zshrc
```

- Open a terminal and run the "lab_wheresim" alias:

```bash
$ lab_wheresim
```

- You should see your terminal change from `user@hostname` to `root@docker`.
- The **lab_wheresim** alias will mount the folder `~/trento_lab_home` on your **host** Mac. Inside the docker image this folder is mapped to `$HOME`. This means that any files you place in your docker `$HOME` folder will survive the stop/starting of a new docker container. All other files and installed programs will disappear on the next run.
- The alias **lab_wheresim** needs to be called only ONCE and opens the image. To link other terminals to the same image you should run **where-other**; this second command will "**attach**" to the image opened previously by calling the **lab_wheresim** alias. You can call **lab_wheresim** only once and **where-other** as many times as you need to open multiple terminals.

# Compiling the code

- Now you can compile the ROS workspace in the $HOME directory **inside** docker:

```bash
$ cd /root/ros_ws/
$ catkin_make install
```

- Only once, after the first compilation do:

```bash
$ source /root/ros_ws/install/setup.bash
```

**NOTE:** when you run the code, if an error pops-up that tells you a recently compiled package cannot be found you need to run:

```bash
$ rospack profile
```

This function crawls through the packages in ROS_ROOT and ROS_PACKAGE_PATH, reads and parses the package.xml for each package, and assembles a complete dependency tree for all packages.

Now you are ready to run the code as explained [here](https://github.com/idra-lab/wheresim?tab=readme-ov-file#running-the-software-from-python-ide-pycharm).

When you have finished exit from the container typing:

```bash
$ exit
```

# **Committing the image** (optional)

To install new packages open a terminal and call the apt install **without** sudo. To store the changes in the local image, get the HASH (a number) of the active container with:

```bash
$ docker ps
```

Commit the docker image (next time you will open a new container it will retain the changes done to the image without losing them):

```bash
$ docker commit HASH mfocchi/trento_lab_framework:wheresim
```

# Docker Issues (optional)

<a name="docker_issues"></a>

Check this section only if you had any issues in running the docker!

- When launching any graphical interface inside docker (e.g. pycharm or gedit) you get an error such as:

```
No protocol specified
Unable to init server: Could not connect: Connection refused

(gedit:97): Gtk-WARNING **: 08:21:29.767: cannot open display: :0.0
```

  It usually means one of the following:
  - XQuartz is not running: make sure it starts (the `lab_wheresim` alias already tries to open it with `open -a XQuartz`).
  - **"Allow connections from network clients"** is not enabled in XQuartz's Security preferences (restart XQuartz after enabling it).
  - `xhost` did not authorize your container's IP. Check the IP you exported and re-run `xhost + <IP>` from a terminal **outside** docker.
  - The `en0` interface is not the one carrying your active network connection. Run `ifconfig` on your host to find the right interface (e.g. `en1` if you use Ethernet via an adapter) and update the alias accordingly.

- If a service inside the container needs to reach something running on your host Mac (e.g. a ROS master, a database), use the hostname `host.docker.internal` from inside the container instead of `localhost` or `127.0.0.1`.

- Performance is noticeably slower than on native Linux because the image runs under x86_64 emulation. Double check that **"Use Rosetta for x86_64/amd64 emulation on Apple Silicon"** is enabled in Docker Desktop's settings, and that Docker Desktop has been given enough CPU/RAM in **Settings > Resources**.
