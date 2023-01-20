import numpy as np
import os

class Indexes():
    def __init__(self):
        print("Initializing Index computation class")

    def salinity_idx(self, img):
        R = img[0, :, :].astype(float)
        G = img[1, :, :].astype(float)
        B = img[2, :, :].astype(float)
        infra = img[3, :, :].astype(float)
        # Allow division by zero
        np.seterr(divide='ignore', invalid='ignore')
        
        #salinity index
        s_idx = np.sqrt(R * infra)
        mn, mx = s_idx.min(), s_idx.max()
        s_idx = (s_idx-mn)/(mx-mn)
    
        #other salinity index
        #os_idx = np.sqrt(B) * R
        os_idx = np.sqrt(B) + R
        if(np.isnan(os_idx).any()):
            os_idx = np.ma.masked_invalid(os_idx)
        '''
        #brightness index
        b_idx = np.sqrt(np.square(R) + np.square(infra))
        if(np.isnan(b_idx).any()):
            b_idx = np.ma.masked_invalid(b_idx)
        '''
    
        #NDSI (ND salinity I)
        ndsi = (R-infra)/(R+infra)
        if(np.isnan(ndsi).any()):
            ndsi = np.ma.masked_invalid(ndsi)
        mn, mx = ndsi.min(), ndsi.max()
        ndsi = (ndsi-mn)/(mx-mn)
   
         #algae
        algae = (G-R)/(G+R)
        if(np.isnan(algae).any()):
            algae = np.ma.masked_invalid(algae)

            #vegetation index
        vegidx = infra * (R/(G*G))
        if(np.isnan(vegidx).any()):
            vegidx = np.ma.masked_invalid(vegidx)
    
        return s_idx, ndsi, algae, vegidx

    def water_quality(self, img):
        '''water qualit OR turbidity computation'''
        s_idx, ndsi, algae, veg_idx = self.salinity_idx(img)
        #w_qual_1  = (np.dot((ndsi - s_idx), algae))/(np.sum(veg_idx))
        w_qual_1  = ((ndsi - s_idx) * algae)/(np.sum(veg_idx))
        #w_qual_2  = np.dot((ndsi - s_idx), algae)
        w_qual_3  = ndsi - s_idx

        return w_qual_3

    def ndvi(self, img):
        R = img[0, :, :]
        G = img[1, :, :]
        B = img[2, :, :]
        infra = img[3, :, :]
        # Allow division by zero
        np.seterr(divide='ignore', invalid='ignore')
        
        #water
        ndvi_water = (G.astype(float) - infra.astype(float))/(infra+G)
        if(np.isnan(ndvi_water).any()):
            ndvi_water = np.ma.masked_invalid(ndvi_water)

        #vegetation
        ndvi_veg = (infra.astype(float) - R.astype(float))/(infra+R)
        if(np.isnan(ndvi_veg).any()):
            ndvi_veg = np.ma.masked_invalid(ndvi_veg)

        return ndvi_water, ndvi_veg

