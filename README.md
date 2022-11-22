# serverless-video-processing

### Instructions to create and upload Docker image to AWS ECR
1. Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 075165449331.dkr.ecr.us-west-2.amazonaws.com```
Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

2. Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here . You can skip this step if your image is already built:

```docker build -t video-processing-app .```

3. After the build completes, tag your image so you can push the image to this repository:

```docker tag video-processing-app:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-app:latest```   
```docker tag video-processing-scaledown:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-scaledown:latest```   
```docker tag video-processing-crop:latest 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-crop:latest```

4. Run the following command to push this image to your newly created AWS repository:

```docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-app:latest```       
```docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-scaledown:latest```                                  
```docker push 075165449331.dkr.ecr.us-west-2.amazonaws.com/video-processing-crop:latest```
