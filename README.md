# Batch Scoring on Azure for Deep Learning Models

This tutorial demonstrates how to deploy a deep learning model to Azure for batch scoring.

__Requirements__

- Ubuntu 16.04 LTS (not tested on Mac or Windows)
- Python 3.4 or greater
- An Azure Subscription
- Docker 1.0 or greater
- A Dockerhub account

## 1. Setup

1. Clone the repo `git clone <repo-name>`
2. `cd` into the repo
3. Setup your virtual env `python -m venv <virtual-env-name>`
4. Install packages `pip install -r requirements.txt`

## 2. Set up environment variables & start the Jupyter Notebook

1. Copy __template.env__ to __.env__ and fill out the configurations and credentials in __.env__
2. Run `source .env` to load all the configurations as environment variables
3. Run `jupyter notebook` in the root directory

The Jupyter notebook will take you through setting up Azure BatchAI with a file share, ACI, and Logic Apps. The notebook will also show your how to setup your training and scoring script to test locally.

## 3. Setup Azure Batch AI with a file share

1. Copy `template.env` to `.env` and fill out the configurations
2. Run `source .env` to load the variables into the system environment
3. Run `python azure/scripts/create_cluster.py`
4. Run `python azure/scripts/upload_files.py --upload-data` check that the files are there (in the portal, or on Storage Explorer)
5. Wait for your cluster to finish provisioning...
6. Run `python azure/scripts/create_job.py` & check that the job is submitted (in the portal)

## 4. Setup ACI to run BatchAI job
1. Build the dockerfile (`sudo docker build -t bai_job .`) which will upload your azure utility python files as well as the `create_job.py` file to the docker image
2. Run `source azure/docker_run.sh -t bai_job` to test that the job works - This script is essentially a wrapper around `docker run` that helps pass in the environment variables
3. Publish the image to your dockerhub

## 5. Setup ACI
1. Setup logic app (TODO elaborate...)

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
