#dataloader here
import numpy as np
import os
import glob
import cv2
import linecache
import pandas as pd
import geopandas as gpd
import rasterio as rio

class LandSatDataset():
    def __init__(self, root, report_path, dataset=None):
        self.root       = root
        self.report     = report_path
        self.dataset    = dataset
        all_dirs        = sorted(os.listdir(self.root))
        self.all_dir_paths   = []
        for _all_dir in all_dirs:
            self.all_dir_paths.append(os.path.join(self.root, _all_dir))


    def load_pond_data(self):
        df      = pd.read_excel(self.report, sheet_name="Pond Info")
        geo_df  = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
        geo_df.crs  = 'epsg:4326'
        pond_locs   = geo_df.to_crs(epsg=32613)
        pond_names  = df['Common Name'].to_list()

        return pond_locs, pond_names

    def run(self, _path):
        print("Filename :", _path)
        paths   = []
        fp      = f'{_path}/*.TIF'
        foldername  = _path.split('/')[-1]
        filepaths   = glob.glob(fp)

        B1_B, B2_B, B3_G, B4_R, B5_NIR, B8_PAN = [], [], [], [], [], [] #bands t be used
        for path in filepaths:
            if (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B1'):
                print("Reading Blue 1 band...")
                tif_obj = rio.open(path)
                B1_B    = tif_obj.read()
                b1b_path = path
            elif (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B2'):
                print("Reading Blue 2 band...")
                tif_obj = rio.open(path)
                B2_B    = tif_obj.read()
                b2b_path = path
            elif (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B3'):
                print("Reading Green band...")
                tif_obj = rio.open(path)
                B3_G    = tif_obj.read()
                b3g_path = path
            elif (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B4'):
                print("Reading Red band...")
                tif_obj = rio.open(path)
                B4_R    = tif_obj.read()
                b4r_path = path
            elif (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B5'):
                print("Reading Infrared band...")
                tif_obj = rio.open(path)
                B5_NIR  = tif_obj.read()
                b5ir_path = path
            elif (path.split('/')[-1].split('.')[0].split('_')[-1] == 'B8'):
                print("Reading Panchromatic band...")
                pan_obj = rio.open(path)
                B8_PAN  = pan_obj.read()
                b8pan_path = path
            
        src_path        = (b8pan_path, b4r_path, b3g_path, b2b_path, b5ir_path)
        blue            = (B1_B + B2_B)/2
        img_stack       = np.concatenate((B4_R, B3_G, blue, B5_NIR), axis=0)

        return src_path, img_stack, pan_obj, B8_PAN, foldername

