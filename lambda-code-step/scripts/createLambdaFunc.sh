#!/bin/bash

lambda_version=step-v3
stages=("app" "batcher" "collector" "crop" "scaledown" "mirror" "rotate" "watermark" "bw" "mirror_bw" "rotate_watermark" "mirror_bw_rotate_watermark" "scaledown_mirror_bw_rotate_watermark")

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state

    ## CLI Command to Create a Lambda Function according to given Image URI
    aws lambda create-function --package-type Image --function-name pipeline-$stage-$lambda_version --role "arn:aws:iam::075165449331:role/BurnRate-BurnRateRole-65N0V6IDANLL" --memory-size 2048 --code ImageUri="075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step-latest" --timeout 900 

    # aws lambda create-function --package-type Image --function-name batch-$stage --role "arn:aws:iam::075165449331:role/BurnRate-BurnRateRole-65N0V6IDANLL" --memory-size 2048 --code ImageUri="075165449331.dkr.ecr.us-west-2.amazonaws.com/app-batch:$stage-batch-latest" --timeout 900 


    
    # aws lambda update-function-code --function-name pipeline-$stage-$lambda_version --image-uri "075165449331.dkr.ecr.us-west-2.amazonaws.com/app-step:$stage-step-latest"

    ## CLI to Update Lambda Function Configuration
    # aws lambda update-function-configuration --function-name pipeline-$stage-$lambda_version --timeout 900 
    # aws lambda update-function-configuration --function-name batch-$stage --timeout 900 #--code ImageUri="075165449331.dkr.ecr.us-west-2.amazonaws.com/app-batch:$stage-batch-latest"
done