# Batch Scoring on Azure for Deep Learning Models

In this repository, we use the scenario of applying style transfer onto a video (collection of images). This architecture can be generalized for any batch scoring with deep learning scenario.

![Reference Architecture Diagram](/assets/batch-scoring-for-dl-models.PNG)

The end-to-end steps that this repository covers are as follows:
1. Upload your selected style image (like a Van Gogh painting) and your style transfer script to Blob Storage.
2. Split up your video into individual frames and upload those frames into Blob Storage.
3. Logic App will then be triggered, and will create an ACI that runs a Batch AI job creation script.
4. The script running in ACI will create the Batch AI jobs. Each job will apply the style transfer in parallel across the nodes of the Batch AI cluster.
5. Once the images are generated, they will be saved back to Blob Storage.
6. Finally, you can download the generates frames, and stitch back the images into a video.

## Requirements

Local/Working Machine:
- Ubuntu >=16.04LTS (not tested on Mac or Windows)
- [Conda >=4.5.4](https://conda.io/docs/)
- [Docker >=1.0](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1) 
- [AzCopy >=7.0.0](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-linux?toc=%2fazure%2fstorage%2ffiles%2ftoc.json)
- [ffmpeg >=3.4.4](https://tecadmin.net/install-ffmpeg-on-linux/)
- [Azure CLI >=2.0](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)
- Ideally GPU enabled for local testing

Accounts:
- A Dockerhub account
- Azure Subscription quota for GPU-enabled VMs (ideally the V100s)

## 1. Setup

1. Clone the repo `git clone <repo-name>`
2. `cd` into the repo
3. Setup your virtual env `python -m venv <virtual-env-name>`
4. Activate your environment `source <virtual-env-name>/bin/activate`
4. Install packages `pip install -r requirements.txt`

## 2. Set up environment variables & start the Jupyter Notebook

1. Copy __template.env__ to __.env__ and fill out the configurations and credentials in __.env__
2. Run `source .env` to load all the configurations as environment variables
3. Make sure you are logged in to both the __az cli__ and __docker ce__
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
