#!/bin/bash
stage=$1

cd $stage
docker build -t $stage-batch .
echo $stage-batch:latest
docker tag $stage-batch:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-batch:$stage-batch-latest
docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/app-batch:$stage-batch-latest
cd ..