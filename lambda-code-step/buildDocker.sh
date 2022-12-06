#!/bin/bash

stages=("app" "batcher" "bw" "collector" "crop" "mirror" "mirror_bw" "mirror_bw_rotate" "mirror_bw_rotate_watermark" "rotate" "rotate_watermark" "scaledown" "scaledown_mirror_bw_rotate_watermark" "watermark")
version=v5

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source ./build.sh $stage
done