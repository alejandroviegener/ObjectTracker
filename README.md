# Object Tracker

Application for multi object tracking, given initial bounding boxes.


# Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Project Structure](#structure)
5. [Application Design Basics](#design)


## Requirements  <a name="requierements"></a>

This application requieres the following for its installation and usage:

* [git][git] 
* [Docker][docker]


[git]: https://git-scm.com/
[docker]: https://www.docker.com/   

## Installation <a name="installation"></a>

Download the source repository to the desired location. From now on this directory will be refered to as $REPO_BASE_DIR: 

```bash
cd $REPO_BASE_DIR
git clone git@github.com:alejandroviegener/ObjectTracker.git
```

The application is dockerized, to build the Docker image follow these steps:

1) Change to the source directory in the repository and give permission to the installation script:

```bash
cd source
chmod +x install.sh
```

2) Execute the install script:

```bash
./install.sh
```

The script will create a docker image and an **in_out** directory. This directory will be used as in and out entrypoint for the aplication. 

To confirm the creation of the image, execute:

```bash
docker image ls
```

A docker image tagged "deepvision-tracker" must be listed

## Usage <a name="usage"></a>

Change to the source directory in the repository:

```bash
cd $REPO_BASE_DIR/source
```

Give permissions to the application script:

```bash
chmod +x tracker.sh
```

Run the application help:

```bash
./tracker.sh --help

usage: tracker [-h] [-a {KCF,MOSSE,CSRT}] [-t TEXT_COLOR TEXT_COLOR TEXT_COLOR] [-b BOX_COLOR BOX_COLOR BOX_COLOR] [-o OUT_FILE_NAME] [-v {0,1,2,3}] [-l] video initial_conditions

positional arguments:
  video                 Input video file
  initial_conditions    Initial conditions (json) file

optional arguments:
  -h, --help            show this help message and exit
  -a {KCF,MOSSE,CSRT}, --algorithm {KCF,MOSSE,CSRT}
                        Tracking algorithm (default: KCF)
  -t TEXT_COLOR TEXT_COLOR TEXT_COLOR, --text_color TEXT_COLOR TEXT_COLOR TEXT_COLOR
                        Text color, BGR separated by space (default: [255, 255, 255])
  -b BOX_COLOR BOX_COLOR BOX_COLOR, --box_color BOX_COLOR BOX_COLOR BOX_COLOR
                        Box color, BGR separated by space (default: [0, 255, 0])
  -o OUT_FILE_NAME, --out_file_name OUT_FILE_NAME
  -v {0,1,2,3}, --verbosity {0,1,2,3}
                        Set output verbosity (0- Error, 1 - Warning, 2 - Info, 3 - Debug) (default: 2)
  -l, --log             Log to file (default: False)
```

Typical usage:

1) Copy the input video and initial conditions to the **in_out** directory

2) Execute the tracker application

```bash
./tracker.sh input.mkv initial_conditions.json -a MOSSE -b 0 255 0 -t 255 255 255 -o output -v 3 --log
```

**Note**: The input video file, the initial conditions file and the output of the application, i.e. video and log file, are managed trough the **in_out** directory.

## Project Structure <a name="structure"></a>

## Application Design Basics <a name="design"></a>

