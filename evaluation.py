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
        sens_list = [None]*20
        for i in range(1,21):
            gc.collect()
            scanPath = self.pathToVessel12Directory + f"data/VESSEL12_{i:02d}/VESSEL12_{i:02d}.mhd"
            gtPath = self.pathToVessel12Directory + f"masks/VESSEL12_01-20_Lungmasks/VESSEL12_{i:02d}.mhd"

            lungSeg = LungSegmentation(scanPath)
            predictedMask = lungSeg.segmentLung()

            GT = self.readScanFrom(gtPath)
            js, sens, fn , fp = self.calculateResults(predictedMask, GT)
            relativeSize = predictedMask.sum()/(GT.shape[0] * GT.shape[1]  * GT.shape[2])
            js_list[i-1] = js
            sens_list[i-1] = sens

            print(f"image number: {i:02d} | jaccard score: {js:.4f} | Sensitivity: {sens:.6f} | FN: {fn} |FP: {fp} | relative Size: {relativeSize}" )

            del lungSeg
            del predictedMask
            del GT
        return js_list, sens_list
    
    @staticmethod
    def readScanFrom(filepath):
        scan = sitk.ReadImage(filepath)
        scan = sitk.GetArrayFromImage(scan)
        return scan

    def calculateResults(self, pred, GT):
        js = self.jaccardScore3dMask(pred, GT)
        sens = self.sensitivity(pred, GT)
        fn = self.falsePositiveCounter(pred, GT)
        fp = self.falseNegativecounter(pred, GT)
        return js, sens, fn , fp

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
        fn = 0
        for i in range(GT.shape[0]):
            fn += cv2.countNonZero(cv2.bitwise_and(GT[i],pred[i]))
        return fn
    
    def sensitivity(self,pred, GT):
        fn = self.falseNegativecounter(pred, GT)
        tp, _ = self.intersectionUnionCounter(pred, GT)
        return tp/(tp+fn)
    
    @staticmethod
    def printFinalResults(js_list, sens_list):
        js_list = np.array(js_list)
        sens_list = np.array(sens_list)
        print("---------------")
        print("---------------")
        print("FINAL RESULTS:")
        print(f"The average jaccard score is {js_list.mean()} with a standard deviation of {js_list.std()}")
        print("The scores for each iteration are:")
        print(js_list)
        print(f"The average sensitivity is {sens_list.mean()} with a standard deviation of {sens_list.std()}")
        print("The scores for each iteration are:")
        print(sens_list)    


if __name__ == "__main__":
    evaluation = Evaluation()
    evaluation.setpathToVessel12Directory("vessel12/")
    js_list, sens_list = evaluation.evaluateVessel12()
    evaluation.printFinalResults(js_list, sens_list)
