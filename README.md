# securitycam

## Description
This repository contains a multiprocess Python program designed to monitor IP cameras. 
It connects to rtsp streams using OpenCV. The frames from the video stream are
processed using a motion detection algorithm and YoLov5 for people detection.  

The code uses a process per camera. The last picture being processed by every process/camera 
is fed back to a main process through a dictionary. 

Any pictures that activate the detectors are stored in the specified directory.

## Motivation
The motivation behind this project is to create a simple and efficient way to monitor
multiple IP cameras. It is thought as a learning and personal project to avoid exposing
the data from my cameras to third party services.

## Usage
This repo is meant to be used as a docker container in Linux:

1. Clone the repository: `git clone https://github.com/eolus87/securitycam.git`
2. Modify (and duplicate if required) the `abstract_conf.yaml` file to include the 
IP addresses and desired settings of your cameras. 
3. Modify the docker compose to fit your needs if required. Mind the paths.
4. Build the docker image: `docker build -t securitycam:v1.0 .`
5. Run the docker container through the compose: `docker compose -f docker-compose.yaml up -d`

## License
This project is licensed under the terms of the MIT license.

## Work Items
- [ ] Add a web interface to monitor the cameras
- [ ] Detection rework: parts of the image, other objects, more complex logic, detection data as metadata.
- [ ] Exit gracefully rework.
- [ ] Optimisation of the code.
- [ ] Connection to cloud storage services.