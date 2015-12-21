# Source Folder

This folder contains the python modules required by various rules to execute. For an AWS Lambda deployment, it's far easier to embed requirements within the function vs. installing during execution. This stabilizes the code base and ensures that execution is consistent.

Each function requires it's own copy of it's pre-requisites.