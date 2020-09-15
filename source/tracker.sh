#!/bin/bash

docker run -it -v $(pwd)/in_out:/mnt deepvision-tracker "$@" 
