#!/bin/bash
#stages=("app" "batcher" "bw" "collector" "crop" "mirror" "rotate" "scaledown" "watermark")
stages=("batcher" "collector")

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source ./build.sh $stage
done