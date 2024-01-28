# Lung segmentation in 3D computed tomography scans

Authors: [Frederik Hartmann](https://github.com/Frederik-Hartmann), [Yusuf Baran Tanrıverdi](https://www.github.com/yusuftengriverdi)
\
*Within the scope of the Advanced Image Analysis course taught by [Prof. Alessandro Bria](https://www.unicas.it/didattica/docenti/teacherinfo.aspx?nome_cognome=alessandro_bria). You can reach the full report [here](https://yusuftengriverdi.github.io/blog/2023/04/15/lung_segmentation_3d).*
\
[Erasmus Mundus Joint Master's Degree in Medical Imaging and Application](https://maiamaster.udg.edu/)
\
April 2023
\

## A detailed tutorial
A detailed step-by-step tutorial can be found on [my website](https://frederik-hartmann.github.io/projects/lungSegmentation/). Feel free to reach out for questions of any kind.

## Reproducing Results
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
