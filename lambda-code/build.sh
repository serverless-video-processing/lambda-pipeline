#!/bin/bash
stage=$1

cd $stage
docker build -t $stage-main .
echo $stage-main:latest
docker tag $stage-main:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/app:$stage-main-latest
docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/app:$stage-main-latest
cd ..