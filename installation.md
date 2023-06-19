## Installation
It is recommended to use a virtual environment:
```shell
  python -m venv venv
```
To install the libraries:
```shell
  pip install -r requirements.txt
```
To recreate the results on the Vessel12 dataset the following file layout is assumed:
```
project
│   evaluation.py
│   lungSegmentation.py
│   ploting.py
│   postprocessing.py
│   preprocessing.py
│
└───vessel12
│   └───data
│       └───VESSEL12_01
│           │   VESSEL12_01.mhd
│           │   VESSEL12_01.raw
│       └───VESSEL12_02
│           │   ...
│   └───masks
│       │   VESSEL12_01.mhd
│       │   VESSEL12_01.raw
│       │   ...
```
If you want to adapt the path to the Vessel12 dataset edit evaluation.py line 111.
```python
  evaluation.setpathToVessel12Directory("PATH/TO/DATASET")

```