# Health-LLM-Using-Bedrock

## environment setup
- 1. Create a virtual environment!!! **THIS IS VERY IMPORTANT**. This will help you to keep your dependencies in a separate environment and not mess up with your system dependencies. And `Dockerizing the application will be easier`.
```bash
python3 -m venv venv
```
- 2. Activate the virtual environment
```bash
source venv/bin/activate
```
- 3. Install the requirements using Makefile
```bash
make install
```

## Credentials Setup
- 1. Make sure you have the `aws credentials` in your system. If not, create one using the following command
```bash
aws configure
```
In the AWS configuration file, you will have to provide the following details:
```bash
AWS Access Key ID [None]: YOUR_ACCESS_KEY
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: us-east-1
Default output format [None]: json
```

## model access setup
- 1. Login to the AWS console and go to the bedrock
- 2. click get started
- 3. On the left side, navigate to model access
- 4. Click orange botton 'manage model access'
- 5. Check box `Titan Embeddings G1 - Text` and `Titan Text G1 - Express`
- 6. Scroll down to click `request model access`
- 7. Wait for the approval. It should be immediate. 

## IAMs setup
![Alt Text](./iams.png)

## Dockerizing the application
** MAKE SURE YOUR DOCKER IS INSTALLED IN YOUR SYSTEM AND ACTIVATED**
- 1. Build the docker image
```bash
docker build -t health-llm:001 .
```
The image has name `health-llm` and tag `001`. You can change the name and tag as per your requirement. This image will be stored in your DockerHub

- 2. Run the docker image
```bash
docker run -p 8501:8501 health-llm:001
```
This will run the docker image in the port `8501`. You can change the port as per your requirement. The first port is the port in your system (in this case I ran on github codespace the default port is `8501` but if you run on local machine, it should be `8000`) and the second port is the port in the docker image. You can define the port in the `Dockerfile` as well. See `EXPOSE 8501` in the `Dockerfile`


## deployment using Kubernates
- 1. Go to Google Cloud Platform and create a project

- 2. Download the `gcloud` sdk from the following link
```bash
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-359.0.0-linux-x86_64.tar.gz
```
- 3. Extract the tar file
```bash
tar -xvf google-cloud-sdk-359.0.0-linux-x86_64.tar.gz
```
- 4. Install the `gcloud` sdk
```bash
cd google-cloud-sdk
./install.sh
```
- 5. Initialize the `gcloud` sdk
```bash
./bin/gcloud init
```
- 6. If you have problem about "mapping", try to use the following command
```bash
sed -i 's/collections.Mapping/collections.abc.Mapping/g' /workspaces/Health-LLM-Using-Bedrock/google-cloud-sdk/google-cloud-sdk/lib/googlecloudsdk/core/console/progress_tracker.py
```

- 7. Install google cloud cli
```bash
sudo apt-get install google-cloud-cli
```
- 8. Install kubectl
```bash
sudo apt-get install kubectl
```

### login to the google cloud
```bash
gcloud auth login
```

```bash
gcloud container clusters get-credentials ["cluster name": health-llm-project] --zone [us-east1] --project ["project_id":reliable-mode-399404]
```
### push image to the google cloud container registry

- Tag Your Docker Image: Before pushing the image to GCR, you need to tag it with the GCR repository URL. The format for the GCR repository URL is gcr.io/[PROJECT_ID]/[IMAGE_NAME], where [PROJECT_ID] is your Google Cloud project ID and [IMAGE_NAME] is the name you want to give to your Docker image.
```bash
docker tag [final:v1] gcr.io/[reliable-mode-399404]/[final]
```

- Authenticate Docker to GCR: Before you can push images to GCR, you need to authenticate Docker to GCR using the Google Cloud SDK. Run the following command:
```bash
gcloud auth configure-docker
```

- Push Your Docker Image to GCR: Once Docker is authenticated, you can push your Docker image to GCR using the following command:
```bash
docker push gcr.io/[PROJECT_ID]/[IMAGE_NAME]
docker push gcr.io/reliable-mode-399404/final
```



