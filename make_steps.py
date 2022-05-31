import pandas as pd
import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt

# Define function for spline interpolation
def make_fast_spline(scans, fast, group, bxid):
    group_list=[]
    for variable in fast.columns:
        if variable == "time" or variable == "bxid": continue
        # Sort DataFrame by time in order to interpolate based on it
        group_val = group[['time','bxid',variable]].dropna()
        group_val = scans.merge(group_val, how='outer', on='time')  
        group_val = group_val.sort_values(by=['time'])
        # Group by bxid in order for interpolation
        group_val['bxid'] = group_val['bxid'].fillna(bxid)
        group_val = group_val.set_index('time')
        # Perform interpolation for each value 
        group_val[variable] = group_val[variable].interpolate(method='spline', order=3)
        group_val = group_val.reset_index()
        group_list.append(group_val[["step.seq","step","bxid", variable]])
    group_final = scans
    group_final = group_final.merge(group_list[0], how='left', on=["step.seq","step"])
    for group_var in group_list[1:]:
        group_final = group_final.merge(group_var, how='left', on=["step.seq","step","bxid"])
    return group_final


def make_dc(fill, overwrite=True):
	if not overwrite:
		dc_spline = pd.read_csv(f'dc_spline.{fill}.gz', index_col=0).reset_index(drop=True)
		return dc_spline

	scans = pd.read_csv(f'scans.{fill}.gz', compression="gzip")
	dc = pd.read_csv(f'dc.{fill}.csv', index_col=0)

	dc['time']=dc['time']/1000000000

	dc_list=[]

	for variable in dc.columns:
	    if variable == "time": continue
	#     dc_val = dc[variable].dropna()
	    dc_val = dc[['time',variable]].dropna()
	#     print(dc_val)
	    kernel_size = 3
	    kernel = np.ones(kernel_size)/kernel_size
	    dc_val[variable] = convolve(dc_val[variable], kernel, mode='same', method='auto')
	    dc_val = dc_val[1:-1]
	    data_dc = scans.merge(dc_val, how='outer', on='time')
	    dc_spline = data_dc.sort_values(by=['time'])
	    dc_spline = dc_spline.reset_index(drop=True)
	    dc_spline = dc_spline.set_index('time')

	    # Interpolation of each DC variable against time 
	    dc_spline[variable] = dc_spline[variable].interpolate(method='spline', order=3)
	    
	    # Remove all time different from the scans file
	    dc_spline = dc_spline[dc_spline['step'].notnull()]
	    dc_spline = dc_spline.reset_index()
	    
	    dc_list.append(dc_spline[["step.seq","step", variable]])
	    
	dc_final = scans
	    
	for dc_var in dc_list:
	    dc_final = dc_final.merge(dc_var, how='left', on=["step.seq","step"])

	# dc_final
	dc_final['N.1'] = dc_final[dc_final.columns[dc_final.columns.str.contains('B1')]].mean(axis=1)
	dc_final['N.2'] = dc_final[dc_final.columns[dc_final.columns.str.contains('B2')]].mean(axis=1)

	dc_final.to_csv(f'dc_spline.{fill}.gz', compression='gzip')

	print("DC output has been saved...")

	return dc_final

def make_fast(fill, overwrite=True):
	if not overwrite:
		fast_spline = pd.read_csv(f'fast_spline.{fill}.gz', index_col=0).reset_index(drop=True)
		return fast_spline
	scans = pd.read_csv(f'scans.{fill}.gz', compression="gzip")
	fast = pd.read_csv(f'fast.{fill}.csv', index_col=0)

	fast['time']=fast['time']/1000000000

	# Get variables names from FAST as a list
	fast_columns = fast.columns[fast.columns.str.contains('B1|B2')]
	        
	# Define Dictionary to store DataFrames for each bxid
	fast_dic = {}
	# Perform Spline Interpolation for each bxid
	for bxid in fast.bxid.unique():
	    fast_dic[bxid] = fast[fast['bxid'] == bxid]
	    fast_dic[bxid] = make_fast_spline(scans=scans, fast=fast, group=fast_dic[bxid], bxid=bxid)
	    fast_dic[bxid] = fast_dic[bxid][fast_dic[bxid]['step'].notnull()]

	# Create new DataFrame including all bxids after interpolation 
	fast_spline = pd.DataFrame()
	for key, value in fast_dic.items():
	    fast_spline = pd.concat([fast_spline, value], ignore_index=True)
	    
	# DataFrame is saved as CSV
	fast_spline.to_csv(f'fast_spline.{fill}.gz', compression='gzip')

	print("FAST output has been saved...")

	return fast_spline

def merge_steps(fill, fast, dc):
	# Create separate DataFrame to perform calibration
	data = fast.copy()

	# Create DataFrame with the sum of FAST values per time and for all bxids
	fast_sum = fast.groupby(list(fast.columns[~fast.columns.str.contains('B1|B2|bxid')])) \
       .sum().reset_index().drop('bxid',axis=1)

	# Calibrate each FAST variable with DC and data_sum values for each beam
	for bxid in data.bxid.unique():
	    for column in data.columns[data.columns.str.contains('B1')]:
	        data[column][data['bxid'] == bxid] = data[column][data['bxid'] == bxid].values*dc['N.1'].values/fast_sum[column].values
	    for column in data.columns[data.columns.str.contains('B2')]:
	        data[column][data['bxid'] == bxid] = data[column][data['bxid'] == bxid].values*dc['N.2'].values/fast_sum[column].values

	# Get bunch intensities calibrated for each beam and bxid
	data['N.1'] = data[data.columns[data.columns.str.contains('R4.B1')]].mean(axis=1)
	data['N.2'] = data[data.columns[data.columns.str.contains('R4.B2')]].mean(axis=1)

	# DataFrame is saved as CSV
	data.to_csv(f'scans_spline.{fill}.gz', compression='gzip')
	return data


def make_steps(fill, overwrite=True):
	dc = make_dc(fill, overwrite=overwrite)
	fast = make_fast(fill, overwrite=overwrite)
	steps = merge_steps(fill, fast=fast, dc=dc)

import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Make steps table')

	parser.add_argument('--overwrite', action='store_true', 
		help="Recalculate interpolation (takes time)")
	parser.add_argument('--no-overwrite', dest='overwrite', action='store_false',
		help="Use stored interpolated values from DC and FAST")
	parser.set_defaults(overwrite=True)
	parser.add_argument("-f", "--fill", 
	    type=str,
	    help="Fill number", 
	)

	args = parser.parse_args()

	# fill = 'test'
	make_steps(args.fill, args.overwrite)
	


	    