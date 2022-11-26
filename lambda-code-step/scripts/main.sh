#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
stages=("crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
version=withoutScaleDown_v1
# Make Output Directory
mkdir ./output/$version

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source execute.sh $stage $version | tee ./output/$version/$stage.out 
done