import numpy as np
import cv2

class Postprocessing:
    def __init__(self):
        pass
    
    def postprocessing(self, mask):
        return self.closeHolesForEachAxialSlice(mask.astype("uint8"))


    def closeHolesForEachAxialSlice(self, mask):
        closedMask = np.zeros(mask.shape, dtype="uint8")
        numberOfAxialSlices = mask.shape[0]
        for i in range(0, numberOfAxialSlices):
            closedSlice = self.closeHolesForEachCompoment(mask[i])
            closedMask[i] = closedSlice 
        return closedMask
    
    def closeHolesForEachCompoment(self, axialSlice):
        mask = np.zeros(axialSlice.shape, dtype="uint8")
        numberOfLabels, labelImage = cv2.connectedComponents(axialSlice)
        for label in range(1, numberOfLabels):
            componentImage = np.array(labelImage == label, dtype="uint8")
            closedSlice = self.closeComponent(componentImage)
            mask += closedSlice
        return mask    

    @staticmethod
    def closeComponent(componentImage):
        kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(15,15))  
        return cv2.morphologyEx(componentImage, cv2.MORPH_CLOSE, kernel)
