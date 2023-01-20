### # In-situ-Water-quality-monitoring-in-Oil-and-Gas-operations
Salinity and turbidity detection of water ponds using Satellite imagery
The water quality detection is a statistical algorithm to analyze the quality of water in lakes/ponds/deltas using LandSat8 satellite times series data. The repo contains method for detection on 2 types of dataset, Satelytics dataset (containes all the all the bands into a single .TIF file) and LandSat8 sensor dataset (Contains individual .TIF file for each band)

### [**Our Method**](to-be-released-soon)
[Satish Kumar*](https://www.linkedin.com/in/satish-kumar-81912540/), [Rui Kou*](https://www.linkedin.com/in/rui-kou/), [Vikram Jayaram](https://www.linkedin.com/in/vjayaram/)

<img src="https://github.com/satish1901/In-situ-Water-quality-monitoring-in-Oil-and-Gas-operations/blob/main/.readfiles/method_overview.gif" width="700">

This repository includes:
* Source code for Water Quality detection alogrithm
* Dataloader for LandSat8 imagery and Satelytics imager
* Python code for Pansharpening multispectral image using panchromatic band
* Example datasample for generating color coded output, histogram, volume of water in pond/lake/delta etc

![supported versions](https://img.shields.io/badge/python-(3.5--3.8)-brightgreen/?style=flat&logo=python&color=green)
![GitHub license](https://img.shields.io/cocoapods/l/AFNetworking)

The repo structure follows standard dataloader and ultily function imported into the main code. Please consider citing/staring our work if it is useful to you

### Requirements
* Python ≥ 3.5
* pip ≥ 21.1.0
* Virtualenv

### Installation
1. Clone this repository
2. Create a python (3.6 or greater) virtualenv
3. Activate the virtualenv
4. Install dependencies
```
pip install -r requirements.txt
```
5. cd to rio-pansharpen directory and run the following commands
```
cd rio-pansharpen
rm -rf build/*
python setup.py install
```
This finishes the environment setup for water quality detection

### Getting started
[main.py](https://github.com/satish1901/In-situ-Water-quality-monitoring-in-Oil-and-Gas-operations/blob/main/main.py) is the primary file to run the code. To see the list of arguments run
```
python main.py --help
```
It dumps the following output
```
usage: main.py [-h] [-d DATA_DIR] [-r REPORT_PATH] [-vo VISUAL_OUT]
               [-ho HIST_OUT] [-ph PLOT_HIST] [-vt VOLUME]

optional arguments:
  -h, --help            show this help message and exit
  -d DATA_DIR, --data_dir DATA_DIR
                        path to data directory
  -r REPORT_PATH, --report_path REPORT_PATH
                        file to get location of ponds
  -vo VISUAL_OUT, --visual_out VISUAL_OUT
                        path to dir for qualitative output
  -ho HIST_OUT, --hist_out HIST_OUT
                        path to directory to dump histogram data
  -ph PLOT_HIST, --plot_hist PLOT_HIST
                        enable histogram plot
  -vt VOLUME, --volume VOLUME
                        enable volume and top 10 average csv file
```
Sample commands to run the code 
```
python main.py -d <path to data directory> -ph <True/False> -vt <True/False>
```
The output of above command will generate color coded output of water quality of each pond/lake in [visual_output](https://github.com/satish1901/water_quality_detection_from_LandSat8/tree/main/visual_output) directory and histogram plot in [histogram](https://github.com/satish1901/water_quality_detection_from_LandSat8/tree/main/histogram) directory. Along with that, it will generate 2 .csv files with names *vol.csv* and *top5avg.csv*, which contains the relative volumne of water in each pond and expected value of top-10 pixel of water quality output respectively
