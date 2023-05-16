from lungSegmentation import LungSegmentation
import SimpleITK as sitk
import numpy as np
import gc
import cv2

class Evaluation:
    pathToVessel12Directory = ""

    def __init__(self):
        pass

    def setpathToVessel12Directory(self, path):
        self.pathToVessel12Directory = path
    
    def evaluateVessel12(self):
        js_list = [None]*20
        for i in range(1,21):
            gc.collect()
            scanPath = self.pathToVessel12Directory + f"data/VESSEL12_{i:02d}/VESSEL12_{i:02d}.mhd"
            gtPath = self.pathToVessel12Directory + f"masks/VESSEL12_01-20_Lungmasks/VESSEL12_{i:02d}.mhd"

            lungSeg = LungSegmentation(scanPath)
            predictedMask = lungSeg.segmentLung()

            print("---------------")
            print(i)
            GT = self.readScanFrom(gtPath)
            js = self.calculateResults(predictedMask, GT)
            js_list[i-1] = js

            del lungSeg
            del predictedMask
            del GT
        return js_list
    
    @staticmethod
    def readScanFrom(filepath):
        scan = sitk.ReadImage(filepath)
        scan = sitk.GetArrayFromImage(scan)
        return scan

    def calculateResults(self, pred, GT):
        js = self.jaccardScore3dMask(pred, GT)
        fn = self.falsePositiveCounter(pred, GT)
        fp = self.falseNegativecounter(pred, GT)

        print(f"jaccard score: {js} | FN: {fn} |FP: {fp}")

        return js

    def jaccardScore3dMask(self, pred, GT):
        intersection, union = self.intersectionUnionCounter(pred, GT)
        if union != 0:
            return intersection/union
        else:
            return 1.0
    
    @staticmethod
    def intersectionUnionCounter(pred, GT):
        GT = GT.astype("uint8")
        pred = pred.astype("uint8")
        inter = 0
        union = 0
        for i in range(GT.shape[0]):
            inter += cv2.countNonZero(cv2.bitwise_and(GT[i],pred[i]))
            union += cv2.countNonZero(cv2.bitwise_or(GT[i],pred[i]))
        return inter, union
    
    @staticmethod
    def falsePositiveCounter(pred, GT):
        GT = (np.logical_not(GT)).astype("uint8")
        pred = pred.astype("uint8")
        fp = 0
        for i in range(GT.shape[0]):
            fp += cv2.countNonZero(cv2.bitwise_and(GT[i],pred[i]))
        return fp

    @staticmethod
    def falseNegativecounter(pred, GT):
        pred = (np.logical_not(pred)).astype("uint8")
        GT = GT.astype("uint8")
        fp = 0
        for i in range(GT.shape[0]):
            fp += cv2.countNonZero(cv2.bitwise_and(GT[i],pred[i]))
        return fp
    
    @staticmethod
    def printFinalResults(js_list):
        js_list = np.array(js_list)
        print("---------------")
        print("---------------")
        print("FINAL RESULTS:")
        print(f"The average jaccard score is {js_list.mean()} with a standard deviation of {js_list.std()}")
        print("The scores for each iteration are:")
        print(js_list)
            




if __name__ == "__main__":
    evaluation = Evaluation()
    evaluation.setpathToVessel12Directory("vessel12/")
    js_list = evaluation.evaluateVessel12()
    evaluation.printFinalResults(js_list)
