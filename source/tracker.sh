#!/bin/bash

if [[ $1 == "--test" ]]; then
    docker run -it --entrypoint "./test.sh" aviegener/deepvision-tracker
else
    docker run -it -v $(pwd)/in_out:/usr/src/app/in_out aviegener/deepvision-tracker "$@" 
fi
