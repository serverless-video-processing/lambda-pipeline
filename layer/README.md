### Instructions to create AWS Lambda Layer
Ensure correct runtime versions and follow the instructions
1. Create requirements.txt file as per your dependencies

2. Install the dependencies to Python folder. AWS Lambda uses looks into this folder for packages
```pip install -t ./python -r requirements.txt```
```rm -r ./python/*dist-info ./python/__pycache__ # remove unused files```

3. Compress the python folder into a .zip file and upload it when creating a Lambda layer. 