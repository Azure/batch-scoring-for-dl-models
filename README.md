# Batch Scoring on Azure for Deep Learning Models

This tutorial demonstrates how to do batch scoring for deep learning models on Azure.

In this tutorial, we walk through the scenario of applying style transfer to a video. Once you have your style transfer script, the steps are as follows:
1. Upload your selected style image (like a Van Gogh painting) and your style transfer PyTorch script to Blob as well.
2. Split up your video into individual frames and upload those frames into Blob.
3. Logic App will be triggered, and will create an ACI that runs a Batch AI job creation script.
4. The script running in ACI will create the Batch AI jobs. Each job will apply the style transfer in parallel across the nodes of the Batch AI cluster.
5. Once the images are generated, they will be saved back to blob.

__Requirements__

Local/Working Machine:
- Ubuntu 16.04 LTS (not tested on Mac or Windows)
- Python 3.4 or greater
- Docker 1.0 or greater
- Ideally GPU enabled for local testing

Accounts:
- A Dockerhub account
- Azure Subscription quota for GPU-enabled VMs (ideally the V100s)
- An Azure Storage account

## 1. Setup

1. Clone the repo `git clone <repo-name>`
2. `cd` into the repo
3. Setup your virtual env `python -m venv <virtual-env-name>`
4. Install packages `pip install -r requirements.txt`

## 2. Set up environment variables & start the Jupyter Notebook

1. Copy __template.env__ to __.env__ and fill out the configurations and credentials in __.env__
2. Run `source .env` to load all the configurations as environment variables
3. Run `jupyter notebook` in the root directory and run through [style_transfer.ipynb](./style_transfer.ipynb).

The Jupyter notebook will take you through setting up Azure BatchAI with a file share, ACI, and Logic Apps. The notebook will also show your how to setup your training and scoring script to test locally.

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
