# Fine-grained Visual Counting

This project is part of our research course "Topics in Computer Science" at the University of Adelaide.
The project's goal for this semester is to create a custom dataset and test its results on a few different SOTA models.
Right now, we only have the code for the CountGD model, and we will update more in the future.

## How To Use

Create a new Conda environment and install all the dependencies
```
conda create -n fgcount python=3.9.19
conda activate fgcount
pip install -r requirements.txt
```

Install the Dataset folder from Google Drive and unzip it.

```
gdown --folder https://drive.google.com/drive/folders/1ZQtbgaL8DEw3JnPes3iEr_CsbmoVgRaV -O .
```

Run the create_dataset.py file

```
python create_dataset.py
```

Clone the CountGD repo and follow the instructions from their Github repo

Run the test_dataset.py file

```
python test_dataset.py
```
