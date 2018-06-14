# Batch Scoring on Azure for Deep Learning Models

This tutorial demonstrates how to deploy a deep learning model to Azure for batch scoring.

### Folders

There are a few main folders to take note of in this repository:

__/bait__

This folder contains all the Batch AI scripts, including:
- `cluster_setup.py` - executed locally
- `fileshare_setup.py` - executed locally
- `job_setup.py` - executed by Functions V2

It also contains a `config_template.py` file, which needs to be renamed as `config.py` and filled out.

__/func__

This folder contains everything needed to run your functions v2. (TODO - maybe this should be made by the user?)

__/models__

This folder is where we store the model files that we will use for scoring.

__/scoring_script__

This folder contains the scoring script that will use a model in the /models directory. This scoring script will be executed on nodes in the Batch AI cluster.

__/training_script__

This folder contains the training scripts used to generate the models in the /models directory. This training script will be executed locally on a GPU enabled VM.

=======

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
