import rasterio as rio
import numpy as np


def calculateRatio(rgb, pan, weight):
    return pan / ((rgb[0] + rgb[1] + rgb[2] * weight) / (2 + weight))

def calculateRatio2(rgb, pan, weight):
    ratio = (pan - (rgb[3]*weight[3]))/(rgb[0]*weight[0] + rgb[1]*weight[1] + rgb[2]*weight[2])

    return ratio


def Brovey(rgb, pan, weight, pan_dtype):
    """
    Brovey Method: Each resampled, multispectral pixel is
    multiplied by the ratio of the corresponding
    panchromatic pixel intensity to the sum of all the
    multispectral intensities.
    """
    with np.errstate(invalid='ignore', divide='ignore'):
        ratio = calculateRatio2(rgb, pan, weight)
    with np.errstate(invalid='ignore'):
        #sharp = np.clip(ratio * rgb, 0, np.iinfo(pan_dtype).max)
        ratio = np.ma.fix_invalid(ratio, fill_value=0.0)
        sharp = ratio * rgb
        return sharp, ratio
