#!/bin/bash

stages=("crop" "scaledown" "mirror" "bw" "mirror_bw" "mirror_bw_rotate" "mirror_bw_rotate_watermark" "mirror_2rotate" "mirror_3rotate" "watermark")
version=v5

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source ./build.sh $stage
done