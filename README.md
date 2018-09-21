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
- [NVIDIA Drivers on GPU enabled machine](https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-18-04-bionic-beaver-linux) _(Optional)_ 
- [Conda >=4.5.4](https://conda.io/docs/)
- [Docker >=1.0](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1) 
- [AzCopy >=7.0.0](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-linux?toc=%2fazure%2fstorage%2ffiles%2ftoc.json)
- [ffmpeg >=3.4.4](https://tecadmin.net/install-ffmpeg-on-linux/)
- [Azure CLI >=2.0](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)

Accounts:
- [Dockerhub account](https://hub.docker.com/)
- [Azure Subscription](https://azure.microsoft.com/en-us/free/) (with a quota for GPU-enabled VMs)

While it is not required, it is also useful to use the [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/) to inspect your storage account.

## 1. Setup

1. Clone the repo `git clone <repo-name>`
2. `cd` into the repo
3. Setup your conda env using the _environment.yml_ file `conda env create -f environment.yml` - this will create a conda environment called __batchscoringdl__
4. Activate your environment `source activate batchscoringdl`
5. Log in to Azure using the __az cli__ `az login`
6. Log in to Docker using the docker cli `docker login`
7. Run through the notebooks starting with [01_apply_style_transfer_locally](./01_apply_style_transfer_locally.ipynb).

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
