#!/bin/bash

launchStepExec()
{
    # Make Output Directory
    mkdir ./output/$batch_len
    mkdir ./output/$batch_len/$step_version
    printf "%s," "${stages[@]}" > ./output/$batch_len/$step_version/stages.txt

    # Run Step Functions
    for stage in ${stages[@]}; do 
        echo $state

        ## Run Step Function
        source execute.sh $stage $step_version $run_version | tee ./output/$batch_len/$step_version/$stage.out 
    done
}

lambda_version=step-v3
batch_len="150Sec"

run_version="v6.1"
step_version=step-agg-csmbrw-$batch_len-batch
stages=("app")
launchStepExec

step_version=step-agg-c-s-m-b-r-w-$batch_len-batch
stages=("crop" "scaledown" "mirror" "bw" "rotate" "watermark")
launchStepExec

step_version=step-agg-c-s-mbrw-$batch_len-batch
stages=("crop" "scaledown" "mirror_bw_rotate_watermark")
launchStepExec

step_version=step-agg-c-s-mb-rw-$batch_len-batch
stages=("crop" "scaledown" "mirror_bw" "rotate_watermark")
launchStepExec

step_version=step-agg-c-smbrw-$batch_len-batch
stages=("crop" "scaledown_mirror_bw_rotate_watermark")
launchStepExec