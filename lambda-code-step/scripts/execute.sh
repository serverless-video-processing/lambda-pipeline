#!/bin/bash
# config
STACK_NAME=lambda-power-tuning
INPUT=$(cat conf/$1.json)  # or use a static string

# retrieve state machine ARN
STATE_MACHINE_ARN="arn:aws:states:us-west-2:075165449331:stateMachine:powerTuningStateMachine-HuOjPttogOIp"

# start execution
EXECUTION_ARN=$(aws stepfunctions start-execution --name "$1-step_profile_$2" --state-machine-arn $STATE_MACHINE_ARN --input "$INPUT"  --query 'executionArn' --output text)

echo -n "Execution started..."

# poll execution status until completed
while true;
do
    # retrieve execution status
    STATUS=$(aws stepfunctions describe-execution --execution-arn $EXECUTION_ARN --query 'status' --output text)

    if test "$STATUS" == "RUNNING"; then
        # keep looping and wait if still running
        echo -n "."
        sleep 1
    elif test "$STATUS" == "FAILED"; then
        # exit if failed
        echo -e "\nThe execution failed, you can check the execution logs with the following script:\naws stepfunctions get-execution-history --execution-arn $EXECUTION_ARN"
        break
    else
        # print execution output if succeeded
        echo $STATUS
        echo "Execution output: "
        # retrieve output
        aws stepfunctions describe-execution --execution-arn $EXECUTION_ARN --query 'output' --output text
        break
    fi
done
