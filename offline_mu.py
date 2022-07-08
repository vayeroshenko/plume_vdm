import pandas as pd
import numpy as np
import json



def make_offline_mu(fill, run):
    # Read counters and scans file with beam intensities
    counters = pd.read_csv(f'Data/counters.{fill}.{run}.gz')
    # counters = pd.read_csv(f'Data/counters-{fill}-{run}.gz', index_col=0)
    scans = pd.read_csv(f'Data/scans_spline.{fill}.gz', index_col=0)

    # Function transforms beam 2 bxid to beam 1 bxid for LHCb
    def transform(bxid):
        return (bxid + 894 - 1) % 3564 + 1

    # Read cut for Luminosity Counters from json file
    # with open('Data/lc_cut.json') as cc_json:
    #     cut = json.load(cc_json)

    # Group by time, counter and bxid to sum all events.
    N = counters.groupby(['time', 'counter', 'bxid']) \
           .sum().reset_index().drop('bin',axis=1)
    N.columns = N.columns.str.replace('counters', 'N')

    # Create DataFrame from counters for empty events
    N0 = counters.copy()

    # Delete all rows with events that are not empty (greater than the cut).
    for counter in N0.counter.unique():
        N0 = N0.drop(counters[counters['counter'] == counter][counters['bin'] >= 1].index)
        
    # Group by time, counter and bxid to sum all empty events.
    N0 = N0.groupby(['time', 'counter', 'bxid']) \
           .sum().reset_index().drop('bin',axis=1)
    N0.columns = N0.columns.str.replace('counters', 'N0')

    # Merge all and empty events in one table to calculate mu with logzero method
    mu = pd.merge(N0, N, how='left', on=['time', 'counter', 'bxid'])
   
    # print(mu)
    # Rename column names to match scans names
    # mu.columns = mu.columns.str.replace('bxID', 'bxid')
    mu.columns = mu.columns.str.replace('time', 'tmin')
    # mu.columns = mu.columns.str.replace('counters_x', 'N0')
    # mu.columns = mu.columns.str.replace('counters_y', 'N')
    


    # Calculate mu with logzero method and its error 
    mu['mu'] = -np.log(mu['N0']/mu['N'])
    mu['mu.err'] = np.sqrt((1/mu['N0'])-(1/mu['N']))


    # Separate scans DataFrame for Beam 1 and Beam 2 variables
    B1 = scans.loc[:, scans.columns[~scans.columns.str.contains('B2|N.2')]]
    B2 = scans.loc[:, scans.columns[~scans.columns.str.contains('B1|N.1')]]

    # Transform Beam 2 bxid to LHCb system
    B2['bxid'] = transform(B2['bxid'])

    # Merge Beam 1 and Beam 2 DataFrames after bxid transformation
    scans = pd.merge(B1, B2, how='outer', on=list(scans.columns[~scans.columns.str.contains('B1|B2|N.1|N.2')]))

    # Merge mu and scans DataFrames 
    mu = pd.merge(mu, scans, how='left', on=['tmin', 'bxid'])

    # Calculate the value of mu specific and its error
    mu['mu.sp'] = 1e25 * mu['mu']/(mu['N.1']*mu['N.2'])
    mu['mu.sp.err'] = 1e25 * mu['mu.err']/(mu['N.1']*mu['N.2'])

    # Rearrange the order of columns in DataFrame
    # mu = mu.iloc[:, [8,9,10,0,7,11,12,13,14,15,16,17,1,2,3,4,5,6,18,19,20,22,23,24,21,25,26,27]]

    # DataFrame is saved as gz compressed file
    mu.to_csv(f'Data/mu.{fill}.{run}.gz', compression='gzip')
    return mu

import argparse
if __name__ == '__main__':
    # Set fill and run of the counter

    parser = argparse.ArgumentParser(description='Make fake scans table')

    parser.set_defaults(overwrite=True)
    parser.add_argument("-f", "--fill", 
        type=str,
        help="Fill number",
        default="test" 
    )
    parser.add_argument("-r", "--run", 
        type=str,
        help="Run number",
        default="231703" 
    )
    args = parser.parse_args()

    # fill = "test"
    # run = 231703
    
    make_offline_mu(fill=args.fill, run=args.run)
