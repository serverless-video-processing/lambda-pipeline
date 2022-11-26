This run has the following params

input video: Elephants Dream - 40mb file - 2:00min
version=step-v3_4
stages=("crop" "scaledown" "mirror" "mirror_bw" "mirror_bw_rotate" "mirror_bw_rotate_watermark")
powerValues=[2048,4096,8192]


for the crop stage, refer to step-v3_3 run on the AWS UI. The lambda function started updating when the state was running and hence failed 