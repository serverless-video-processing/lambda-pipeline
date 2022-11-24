#!/bin/bash
stage=$1

echo $stage-hello

cd $stage
docker build -t $stage-profile .
docker tag $stage-profile:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-profile:$stage-profile-latest
docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-profile:$stage-profile-latest