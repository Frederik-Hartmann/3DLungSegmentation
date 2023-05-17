# Lung segmentation in 3D computed tomography scans

In this tutorial it is explained how to segment a lung in a a 3d CT scan. First let's take a look at a CT scan.

<p align="center">
	<img src="./visualization/CTScan.png" width=30% height=30% class="center">
</p>
In the picture above you can vaguely outline the body, head and arms of the person. Below the person a table, on which the person is lying, can be spotted. It is worth mentioning that the table is not broken and the gaps are due to the displaying technique used. Now lets take a look at a axial slice in the center.

<p align="center">
	<img src="./visualization/AxialSlice.png" width=30% height=30% class="center">
</p>
In this image the lung is displayed in dark. The surrounding tissues and bones appear brighter. The background is rouhly the same intensity as the lung tissue. In the bottom of the picture multiple lines can be seen. These lines are the edges of the patient table and what appears to be a cushion. The goal of the lung segmentation is to find/segment the lung. In order to do accomplish this the table, background and surrounding tissues need to be removed. The flow diagramm below shows the workflow. In the following all steps will be explained in detail with text, pictures and code.


```mermaid
flowchart LR 
	A["Preprocessing"];
	B["Lung Segmentation"];
	C["Postprocessing"];
	
	A --> B;
    	B --> C;
	click A href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/preprocessing.py" _blank;
	click B href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/lungSegmentation.py" _blank;
	click C href "https://github.com/Frederik-Hartmann/3DLungSegmentation/blob/main/postprocessing.py" _blank;

```
