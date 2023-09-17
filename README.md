# bachelorProject

***

## Learning BPMN Process Models from Cobot Movements

## Description
This project can connect to the Universal Robots RTDE (Real-Time Data Exchange) Interface to receive position data (waypoints) from the robot when the robot is programmed via free-drive mode.
These waypoints are then published in the SSE channel of the REST Server. Clients can subscribe to the REST Server and receive the data for further processing.
The Client implemented in this project selects waypoints from the received ones. This selection is done based on a minimum and maximum threshold for the distance between the 
waypoints. The user can set the joint thresholds according to how granular the waypoints should be. Furthermore, the Client creates two BPMN models: one based on the originally received waypoints, the other
based on the selected ones. These models are saved as xml-files in the cpee-tree format.

The program test.py reads in already recorded waypoint data from a csv-file and then run the algorithm to create the BPMN models.

The program Evaluation.py reads two xml-files: first the original BPMN model, then the BPMN to be compared and calculates the similarity between the movements saved in the BPMN.
The similarity is calculated as the Discrete Frechet Distance (DFD) from the 'similaritymeasures' package.

## Installation
requires docker, redis, flask and flask-sse for the REST Server and the package 'similaritymeasures' for the Evaluation 

## Usage
Free-drive Teaching and Recording using the terminal:
1. start the REST Server using the commands: 1. docker run --name redis-sse -p 6379:6379 -d redis (first time) or docker start redis-sse, 2. gunicorn RESTServer:app --worker-class gevent --bind 127.0.0.1:5000
2. start Client: python3 Client.py
3. start robot-communication-routine: change the host IP-address in line 44 to the correct one, then start with the command: python3 robot-communication-routine.py
4. teach robot in free-drive mode
5. stop robot-communication-routine with ctr c, this also signals the Client that the movement is finished and the Client will start the algorithm
6. stop REST Server with ctr c and stop the docker container with: docker stop redis-sse

Using test.py:
1. change the csv-file name in line 35 to the desired file and make sure the file is in the bachelorproject-folder
2. select which algorithm with which joint thresholds should be run, by creating a new Algorithm or uncomment an existing one
3. run test.py in IDE or in terminal

Using Evaluation.py:
1. change the xml-file name in line 7 (original BPMN) and the xml-file name in line 19 (proposed BPMN) to the desired files. Make sure the files are in cpee-tree format and located in the bachelorproject-folder
2. run Evaluation.py in IDE or in terminal

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.
