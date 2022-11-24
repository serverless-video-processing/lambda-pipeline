#!/bin/bash
stage=$1

cd $stage
docker build -t $stage .
docker tag $stage:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/app:$stage-latest
docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/app:$stage-latest