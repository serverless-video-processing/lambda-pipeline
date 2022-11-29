#!/bin/bash

stages=("batcher" "app" "collector" "bw" "crop" "mirror" "rotate" "scaledown" "watermark")

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source ./build.sh $stage
done