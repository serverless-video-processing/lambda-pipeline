#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "watermark")
# op_count=(1 1 1 2 3 1)
# stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_2rotate" "mirror_3rotate" )

lambda_version=step-v3
batch_len="2MinBatch"

step_version=step-agg-c-s-m-b-r-w
stages=("crop" "scaledown" "mirror" "bw" "rotate" "watermark")

step_version=step-agg-c-s-mbrw
stages=("crop" "scaledown" "mirror_bw_rotate_watermark")

step_version=step-agg-c-s-mb-rw
stages=("crop" "scaledown" "mirror_bw" "rotate_watermark")

step_version=step-agg-c-smbrw
stages=("crop" "scaledown_mirror_bw_rotate_watermark")

# Make Output Directory
mkdir ./output/$batch_len/$step_version
echo "stages-crop, scaledown, mirror, mirror_bw, mirror_bw_rotate, mirror_bw_rotate_watermark" > ./output/$batch_len/$step_version/stages.txt

# Run Step Functions
for stage in ${stages[@]}; do 
    echo $state

    ## Run Step Function
    source execute.sh $stage $step_version | tee ./output/$batch_len/$step_version/$stage.out 
done