#!/bin/bash

# stages=("scaledown" "crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")
stages=("crop" "mirrorx" "mirrory" "bw" "rotate" "watermark")

for stage in ${stages[@]}; do 
    source execute.sh $stage v3 | tee $stage.out
done