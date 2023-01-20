#utility functions here
import numpy as np
import os
import glob
import cv2
import linecache
import importlib
import rasterio as rio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from rasterio.transform import guard_transform
rio_pansharpen = importlib.import_module("rio-pansharpen")
from rio_pansharpen import worker

class Utils():
    def __init__(self):
        print("Initialize utility class")

    def pansharp_data(self, src_path, img_stack, B8_PAN):
        #[0.166, 0.167, 0.167, 0.5]
        with rio.open(src_path[0]) as pan_src:
            profile = pan_src.profile
            if profile['count'] > 1:
                raise RuntimeError(
                    "Pan band must be 1 band - is {}".format(profile['count']))

            dst_dtype = 'uint32'
            profile['count'] = 4

        with rio.open(src_path[1]) as r_src:
            r_meta = r_src.meta

        dst_crs = profile['crs']
        r_crs   = r_meta['crs']
        dst_aff = guard_transform(profile['transform'])
        r_aff   = guard_transform(r_meta['transform'])
        #weight  = [0.52, 0.25, 0.23, 1.0]
        weight  = [0.166, 0.167, 0.167, 0.5]
        print("Calling the PanSharpen Function....")

        pansharpened    = worker.pansharpen(img_stack, r_aff, B8_PAN.squeeze(), dst_aff, \
                                        dst_dtype, r_crs, dst_crs, weight, \
                                        method="Brovey", src_nodata=0)
        print("Pansharpening Done!!!")
        pansharpened    = np.clip(pansharpened, a_min=-30770, a_max=64572)

        return pansharpened

    def georef_lookup(self, src):
        transform = src.transform
        N = src.width
        M = src.height
        dx = transform.a
        dy = transform.e
        minx = transform.c
        maxy = transform.f
        print("new coords")
        print("upper left: ", minx, maxy)
        print("cell size: ", dx, dy)
        print("columns and rows:", M, N)
        print("bounds: ", src.bounds)
        '''
        Generate X and Y grid locations
        notice that ydata, the (0,0) co-ordinates are at bottom-left
        unlike the idea numpy matrix (0,0) at top-left
        '''
        xdata = minx  + dx*np.arange(N+1)
        ydata = maxy  + dy*np.arange(M+1)
        print("check new coodinates")
        extent = [xdata[0], xdata[-1], ydata[0], ydata[-1]]
        print("extent: ", extent)

        return xdata, ydata

    def find_pond(self, xdata, ydata, pond_locs):
        x_pix, y_pix    = [], []
        xpond   = pond_locs.geometry.x
        ypond   = pond_locs.geometry.y
        for i,j in zip(xpond, ypond):
            x_diff  = xdata - i
            y_diff  = ydata - j
            x_pix.append(np.argmin(np.abs(x_diff)))
            y_pix.append(np.argmin(np.abs(y_diff)))

        return x_pix, y_pix

    def segment_pond_save_output(self, w_qual, cus_cmap, seg_class, pond_names, x_pix, y_pix, args, \
                                 foldername, vol, topavg):
        vmin    = seg_class.min()
        vmax    = seg_class.max()
        count   = 0
        h, w    = seg_class.shape
        for cx, cy in zip(x_pix, y_pix):
            start_point = (int(cx-20), int(cy-20))
            end_point   = (int(cx+20), int(cy+20))
            if start_point[0]< 0 : start_point[0] = 0
            if start_point[1]< 0 : start_point[1] = 0
            if end_point[0]> w-1 : end_point[0] = w-1
            if end_point[1]> h-1 : end_point[1] = h-1

            pond_segcolr    = seg_class[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            '''save output color coded image'''
            self.dump_img(pond_segcolr, pond_names[count], cus_cmap, foldername, vmin, vmax, args)
            
            '''compute histogram is True'''
            if args.plot_hist is True:
                pond_seg    = w_qual[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                mu, sig = self.draw_hist(pond_seg, pond_names[count], foldername, args)
            
            '''compute volume of water in each pond'''
            if args.volume is True:
                print("compute volume of water in each pond")
                pond_seg    = w_qual[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                _vol, _top_avg  = self.vol_topavg(pond_seg)
                if count in vol:
                    vol[count].append(_vol)
                    topavg[count].append(_top_avg)
                else:
                    vol[count]  = [_vol]
                    topavg[count]  = [_top_avg]

            count = count+1

    def dump_img(self, img, name, cus_cmap, foldername, vmin, vmax, args):
        dir_path    = f'{args.visual_out}/{name}'
        img_path    = f'{dir_path}/{foldername}.png'
        if not (os.path.isdir(dir_path)):
            os.mkdir(dir_path)
            print("created directory", dir_path)
            plt.imsave(img_path, img, vmin=vmin, vmax=vmax, cmap=cus_cmap)
        elif (os.path.isdir(dir_path)):
            plt.imsave(img_path, img, vmin=vmin, vmax=vmax, cmap=cus_cmap)
    
        return

    def draw_hist(self, pond_seg, name, foldername, args):
        bin_clr = ["black", "gray", "silver", "aqua", "lightcyan", "deepskyblue", "yellow", "sandybrown", \
                   "peru", "salmon", "orangered", "yellowgreen", "g", "darkgreen", "blue", "darkslateblue"]
        list_n, bins, patches = plt.hist(pond_seg.flatten(), bins=16, range=(0.2, 1.0), \
                                         density=True, facecolor='g', alpha=0.75)
        plt.xlabel('bins')
        plt.ylabel('number of pixels')
        plt.grid(True)
    
        mu  = np.mean(pond_seg)
        sigma   = np.std(pond_seg)
        y_axis = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        plt.plot(bins, y_axis, '--', color ='black')
        dir_path    = f'{args.hist_out}/{name}'
        img_path    = f'{dir_path}/{foldername}.png'
    
        #assign color to each bin
        for i in range(16):
            patches[i].set_facecolor(bin_clr[i])
    
        if not (os.path.isdir(dir_path)):
            os.mkdir(dir_path)
            print("created directory", dir_path)
            plt.savefig(img_path)
        elif (os.path.isdir(dir_path)):
            plt.savefig(img_path)
        plt.close()

        return mu, sigma

    def vol_topavg(self, pond_seg):
        _vol = np.argwhere(pond_seg>0.40)
        _vol = _vol.shape[0]
        pond_seg    = pond_seg.flatten()
        srt_args    = np.argsort(pond_seg)
        _top_avg     = pond_seg[srt_args[-10:]].mean()
    
        return _vol, _top_avg

    def non_linearity(self, img):
        return np.sign(img)*np.log(1+np.abs(img))

    def norm_data(self, band_data):
        band_data   = np.ma.masked_where(band_data==0, band_data)
        mn, mx      = band_data.min(), band_data.max()
        band_data   = (band_data-mn)/(mx-mn)
        band_data   = band_data.data

        return band_data

    def my_calc_stats(self, data, mask=None):
        idx = np.where(mask != False)
        data = np.take(data, idx.squeeze(), axis=1)
        mean = np.average(data, axis=1)
        C    = np.cov(data)

        return mean, C

    def denoise_data(self, data):
        data = np.transpose(data, (1,2,0))
        np.seterr(divide='ignore', invalid='ignore')
        h, w, ch = data.shape
        data_mask = np.ma.masked_where(data==0, data)
        signal = calc_stats(data_mask)
        h_t = int(h/2)-500
        h_b = int(h/2)+500
        w_l = int(w/2)-500
        w_r = int(w/2)+500
        noise  = noise_from_diffs(data_mask[h_t:h_b, w_l:w_r, :])
        try:
            mnfr   = mnf(signal, noise)
        except:
            import pdb; pdb.set_trace()
            return -1
        denoised_data = mnfr.denoise(data_mask, num=3)
        denoised_data = np.transpose(denoised_data, (2,0,1))

        return denoised_data

    def gen_custom_cmap(self, img):
        #ndvi_class_bins = [-np.inf, 0, 0.1, 0.15, 0.20, 0.25, 0.30, 0.4, np.inf]
        #ndvi_class_bins = [-np.inf, -0.3, -0.1, -0.05, -0.025, 0, 0.05, 0.1, 0.125, np.inf]
        #ndvi_class_bins = [-np.inf, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75,  np.inf]
        ndvi_class_bins = [-np.inf, 0.42, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75,  np.inf]
        ndvi_class = np.digitize(img, ndvi_class_bins)
        cus_colors = ["black", "gray", "white","yellow", "orange", "yellowgreen", "g",\
                        "darkgreen", "blue"]
        cus_cmap = ListedColormap(cus_colors)
        ndvi_class = np.ma.masked_where(np.ma.getmask(img), ndvi_class)

        return cus_cmap, ndvi_class



