#main file here
import numpy as np
import os
import glob
import cv2
import linecache
import pandas as pd
import geopandas as gpd
import rasterio as rio
from rasterio.transform import guard_transform
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from spectral.algorithms.algorithms import *

#custom imports
from utils.arg_parser import args
from dataloader.dataloader import LandSatDataset
from utils.utils import Utils
from indexes import Indexes

def main():
    dataset     = LandSatDataset(args.data_dir, args.report_path)
    utility     = Utils()
    index       = Indexes()
    vol         = {}
    topavg      = {}
    pond_locs, pond_names   = dataset.load_pond_data()
    for _path in dataset.all_dir_paths:
        '''load image'''
        src_path, img_stack, pan_obj, B8_PAN, foldername = dataset.run(_path)
        '''pansharpen image'''
        pansharpened    = utility.pansharp_data(src_path, img_stack, B8_PAN)
        '''Generating a look-up table for refernce coordinates'''
        xdata, ydata    = utility.georef_lookup(pan_obj)
        '''Find pond location in cartesian co-ordinates'''
        x_pix, y_pix    = utility.find_pond(xdata, ydata, pond_locs)
        '''compute water quality/turbidity'''
        print("Computing water Quality index...")
        w_qual  = index.water_quality(pansharpened.data)
        print("Getting Custom colormaps")
        cus_cmap, seg_class = utility.gen_custom_cmap(w_qual)
        '''segment each pond and save output'''
        utility.segment_pond_save_output(w_qual, cus_cmap, seg_class, pond_names, x_pix, y_pix, args, \
                                        foldername, vol, topavg)

    if args.volume is True:
        vol_df  = pd.DataFrame(vol)
        topavg_df  = pd.DataFrame(topavg)
        vol_df.to_csv("vol.csv")
        top_avg_df.to_csv("top5avg.csv")
            
if __name__=='__main__':
    main()
