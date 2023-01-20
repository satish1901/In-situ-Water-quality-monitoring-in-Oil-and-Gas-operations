import argparse

#Inputs
parser = argparse.ArgumentParser()

parser.add_argument('-d', '--data_dir', type=str, required=False,
                default='/data_satish/satish/liquid_leaks/LandSat8_new', help='path to data directory')

parser.add_argument('-r', '--report_path', type=str, required=False,
                default='./water_quality_reports/Pond_report.xls', help='file to get location of ponds')

parser.add_argument('-vo', '--visual_out', type=str, required=False,
                default='./visual_output', help='path to dir for qualitative output')

parser.add_argument('-ho', '--hist_out', type=str, required=False,
                default='./histogram', help='path to directory to dump histogram data')

parser.add_argument('-ph', '--plot_hist', type=bool, required=False,
                default=False, help='enable histogram plot')

parser.add_argument('-vt', '--volume', type=bool, required=False,
                default=False, help='enable volume and top 10 average csv file')

args    = parser.parse_args()
