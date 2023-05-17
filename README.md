# Lung segmentation in 3D computed tomography scans

In this tutorial it is explained how to segment a lung in a a 3d CT scan. First let's take a look at a CT scan.

<p align="center">
	<img src="./visualization/CTScan.png" width=30% height=30%>
</p>
In the picture above you can vaguely outline the body, head and arms of the person. Below the person a table, on which the person is lying, can be spotted. It is worth mentioning that the table is not broken and the gaps are due to the displaying technique used. Now lets take a look at a axial slice in the center.

<p align="center">
	<img src="./visualization/AxialSlice.png" width=30% height=30%>
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
## Preprocessing
The first step is the preprocessing. The goal is to remove the table and make the background the same intensity as the tissue surrounding the lung. Each pixel/vocel in a computed tomography scan is not encoded in a range from 0-255 (8-bit unsigned), but rather in a range from −32,768 to 32,767 (16-bit signed). However, there is more to it. Each value represents a Hounsfield unit (HU) and Hounsfield units can be attributed to a specific tissue. Because we are only interested in lung tissue, we choose a range in which the lung is safely included and set all other pixels to the maximum of the range. In this case a range of -1000 HU to -500 HU.

<table style="width: 100%;">
  <tr>
    <th style="width: 40%;">Input</th>
    <th style="width: 40%;">Output</th>
    <th style="width: 20%;">Implementation</th>
  </tr>
  <tr>
    <td style="width: 33.33%;"><img src="./visualization/AxialSlice.png"></td>
    <td style="width: 33.33%;"><img src="./visualization/clippedAxialSlice.png">
    <td style="width: 33.33%;">
      <pre lang="python"><code style="font-size: 18px;">
def clipScanToHounsfieldUnitRange(scan,HounsfieldUnitRange):
	HU_min = HounsfieldUnitRange[0]
	HU_max = HounsfieldUnitRange[1]
	return np.clip(scan,a_min=HU_min, a_max=HU_max) 
      </code></pre>
    </td>
  </tr>
</table>

This is done for the entire scan. The steps after this are applied to each slice seperately. It can be seen that the table in this viewing direction is not a straight line. This will become important later. To make the table straight, we use the sagittal view and therefore use sagittal slices. 
1. First we loop through the sagittal slices:
<table style="width: 100%;">
  <tr>
    <th style="width: 50%;">Sagittal slice</th>
    <th style="width: 50%;">Implementation</th>
  </tr>
  <tr>
    <td style="width: 50%;"><img src="./visualization/clippedSagittalSlice.png"></td>
    <td style="width: 50%;">
      <pre lang="python"><code>
def createMaskForEachSliceOf(self, clippedScan):
	mask = np.zeros(clippedScan.shape, dtype="int16")
	numberOfSagittalSlices = clippedScan.shape[1]
		for i in range(0,numberOfSagittalSlices):
			sagittalSlice = clippedScan[:,:,i]
			sliceMask = self.createMaskFrom(sagittalSlice)
			mask[:,:,i] = sliceMask.astype("int16")
	return mask
      </code></pre>
    </td>
  </tr>
</table>

