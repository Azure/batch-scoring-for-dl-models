# Batch Scoring on Azure for Deep Learning Models

This tutorial demonstrates how to deploy a deep learning model to Azure for batch scoring.

## Requirements

TODO instructions on requirements to run the file (python version, etc...)

## Create your model file and data files

TODO instructions on creating `model/pytorch_classification/model0`, `data/pytorch_classification`...

## Setup Azure Infrastructure

1. Copy `template.env` to `.env` and fill out the configurations
2. Run `source .env` to load the variables into the system environment
3. Run `python azure/scripts/create_cluster.py`
4. Run `python azure/scripts/upload_files.py --upload-data` check that the files are there (in the portal, or on Storage Explorer)
5. Wait for your cluster to finish provisioning...
6. Run `python azure/scripts/create_job.py` & check that the job is submitted (in the portal)
7. Build the dockerfile (`sudo docker build -t bai_job .`) which will upload your azure utility python files as well as the `create_job.py` file to the docker image
8. Run `source azure/docker_run.sh -t bai_job` to test that the job works - This script is essentially a wrapper around `docker run` that helps pass in the environment variables
9. Publish the image to your dockerhub
10. Setup logic app (TODO elaborate...)

## File System
```
.
├── azure/
│   ├── scripts/
│   │   ├── util/
│   │   │   ├── __init__.py
│   │   │   ├── fileshare.py
│   │   │   └── bai.py
│   │   ├── create_cluster.py
│   │   ├── create_job.py
│   │   ├── upload_files.py
│   │   └── delete_resources.py
│   ├── docker_run.sh
│   ├── Dockerfile
│   └── requirements.txt
│
├── scoring_script/
│   ├── pytorch_classification/
│   │   └── score0.py
│   └── tf_mnist/
│       └── score0.py
│
├── training_script/
│   ├── pytorch_classification/
│   │   ├── train0.ipynb
│   │   └── train0.py
│   └── tf_mnist/
│       ├── train0.ipynb
│       └── train0.py
│
│-- Files below this point will be created --
│
├── data/
│   └── pytorch_classification/
│
└── model/
    ├── pytorch_classification/
    └── tf_mnist/
```

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
