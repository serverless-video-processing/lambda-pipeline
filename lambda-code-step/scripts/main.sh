#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
stages=("crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
version=v5
# Make Output Directory
mkdir ./output/$version

# Run Step Functions
for stage in ${stages[@]}; do 
    # aws lambda update-function-configuration --function-name pipeline-$stage-step --timeout 900 
    source execute.sh $stage $version | tee ./output/$version/$stage.out 
done