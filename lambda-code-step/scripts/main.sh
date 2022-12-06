#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "watermark")
# op_count=(1 1 1 2 3 1)
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "mirror_3rotate" )

lambda_version=step-v3
step_version=step-agg1
stages=("crop" "scaledown" "mirror_bw" "rotate_watermark")
# stages=("mirror_bw_rotate" "mirror_bw_rotate_watermark")

# Make Output Directory
mkdir ./output/$version
echo "stages-crop, scaledown, mirror, mirror_bw, mirror_bw_rotate, mirror_bw_rotate_watermark" > ./output/$version/stages.txt

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state

    ## CLI Command to Create a Lambda Function according to given Image URI
    # aws lambda create-function --package-type Image --function-name pipeline-$stage-$lambda_version --role "arn:aws:iam::075165449331:role/BurnRate-BurnRateRole-65N0V6IDANLL" --memory-size 2048 --code ImageUri="075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step-latest" --timeout 900 

    ## CLI to Update Lambda Function Configuration
    # aws lambda update-function-configuration --function-name pipeline-$stage-$lambda_version --timeout 900 

    ## Run Step Function
    # source execute.sh $stage $step_version | tee ./output/$step_version/$stage.out 
done