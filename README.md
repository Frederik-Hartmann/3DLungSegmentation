# Lung segmentation in 3D computed tomography scans

```mermaid
flowchart LR 
	A["Preprocessing"];
	B["Lung Segmentation"];
	C["Postprocessing"];
	
	A --> B;
    B --> C;
	click A href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/preprocessing.py";
	click B href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/lungSegmentation.py";
	click C href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/postprocessing.py";

```
