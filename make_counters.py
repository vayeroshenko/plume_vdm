"""Obtain Root Histogram from Counters."""

import pandas as pd
import subprocess


def counters(fill, run, overwrite=True):
    """ Run root counters file and parse its ouput as a DataFrame.

        Runs a root script to obtain histogram of luminosity counters tuples
        for an specific fill and run. It captures its output and saves it as a
        DataFrame.

        Parameters
        ----------
        fill: Number of fill desired.

        run: Specific run of the fill.

        Returns
        -------
        Saves a GZ compressed file containing DataFrame.

    """

    if not overwrite:
        counters = pd.read_csv(f'Data/counters.{fill}.{run}.gz')
        return counters

    # Read scans file to get time steps
    scans = pd.read_csv(f'Data/scans.{fill}.gz')

    # Set path and name of root tuples
    # rootpath = '/eos/lhcb/wg/Luminosity/data/counters/'
    # rootfile = f'{rootpath}counters-{fill}-{run}-hlt.root'
    rootpath = '/afs/cern.ch/work/v/vyeroshe/'
    rootfile = f'{rootpath}plume_ntuple_allch_0000{run}.root'

    # Set terminal command to run root script
    cmd = f'./plume_root_counters/step_hist {rootfile} 270'

    # Convert time steps to string
    if (run == 'all'):
        time_range = scans['tmin'].astype(str) \
                    + " " + scans['tmax'].astype(str) + "\n"
        time_str = bytes(time_range.sum(), 'utf-8')
    else:
        time_range = scans['tmin'][scans['run'] == run].astype(str) \
                     + " " + scans['tmax'][scans['run'] == run].astype(str) + "\n"
        time_str = bytes(time_range.sum(), 'utf-8')

    print(f"{cmd}\n{time_str}")

    # Run root script
    roothist = subprocess.run(cmd, input=time_str, capture_output=True, shell=True)
    print(roothist.stdout)
    # Parse root output
    counters = str(roothist.stdout, 'UTF-8')
    counters = counters.split('\n ')
    counters[0] = counters[0].replace(' ', '', 1)
    counters[-1] = counters[-1].replace('\n', '')
    counters = pd.DataFrame(counters)
    counters = counters[0].str.split(pat=' ',expand=True)
    print(counters)
    counters.columns = ['time', 'counter', 'bxid', 'bin', 'events']

    # Export as gz compress file
    counters.to_csv(f'Data/counters.{fill}.{run}.gz', compression='gzip')
    return counters

if __name__ == '__main__':
    counters("test", 231703, overwrite=True)
