# serverless-video-processing

Slides : https://drive.google.com/file/d/1KgJ_BsiZNoO_pjYIXktzsM2yhA5kcqs3/view?usp=drive_link
Paper: https://drive.google.com/file/d/1j8zuLIPx7Dq8PoC02ySF8df5r7erfTJs/view?usp=drive_link

### Instructions to create and upload Docker image to AWS ECR
1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 075165449331.dkr.ecr.us-west-2.amazonaws.com```
Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

2. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

- For each directory, use ```source build.sh stage``` where stage in [app, bw, crop ....]



### For running Step Functions   
The execution input configuration is generated using `lambda-code-step/scripts/notebooks` and stored at `lambda-code-step/scripts/conf`.    
Run Step function for given stage as:    

`source execute.sh <stage-name> <version(vi)>`
