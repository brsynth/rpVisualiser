#!/bin/bash

docker-compose run --rm -v $PWD:$PWD -w $PWD rpvisualizer python /home/src/rpvisualizer.py $@
