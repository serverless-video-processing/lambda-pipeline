#!/bin/bash
stage=$1

echo $stage-hello

cd $stage
docker build -t $stage .
docker tag $stage-step:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step:latest
docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step:latest