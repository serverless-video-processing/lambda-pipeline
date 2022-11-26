#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "watermark")
# op_count=(1 1 1 2 3 1)
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "mirror_3rotate" )

version=step-v3_3
stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_bw_rotate" "mirror_bw_rotate_watermark")
# stages=("mirror_bw_rotate" "mirror_bw_rotate_watermark")
op_count=(1 1 1 2 3 5)

# Make Output Directory
mkdir ./output/$version

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state

    ## CLI Command to Create a Lambda Function according to given Image URI
    # version=step-v3
    # aws lambda create-function --package-type Image --function-name pipeline-$stage-$version --role "arn:aws:iam::075165449331:role/BurnRate-BurnRateRole-65N0V6IDANLL" --memory-size 2048 --code ImageUri="075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step-latest" --timeout 900 

    ## CLI to Update Lambda Function Configuration
    # aws lambda update-function-configuration --function-name pipeline-$stage-$version --timeout 900 
    source execute.sh $stage $version | tee ./output/$version/$stage.out 
done