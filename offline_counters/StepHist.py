#!/cvmfs/lhcb.cern.ch/lib/var/lib/LbEnv/2428/stable/linux-64/bin/python3

import pandas as pd
import subprocess
import argparse as arg

import sys

def counters(fill, run):
    # scans = pd.read_csv(f'/afs/cern.ch/work/v/vyeroshe/Plume_vdm/plume-vdm/Data/scans.{fill}.gz')
    scans = pd.read_csv(f'scans.{fill}.gz')
    # rootpath = '/eos/lhcb/wg/Luminosity/data/counters/'
    # rootfile = f'{rootpath}counters-{fill}-{run}-hlt.root'

    rootpath = '/eos/lhcb/wg/plume/vdm_tuples/'
    rootfile = f'{rootpath}plume_ntuple_allch_0000{run}.root'
    
    cmd = f'./step_hist {rootfile}'

    output_path = '/afs/cern.ch/work/v/vyeroshe/Plume_vdm/plume-vdm/Data/'

    # Convert time steps to string
    if (run == 'all'):
        time_range = scans['tmin'].astype(str) + " " + scans['tmax'].astype(str) + "\n"
        time_str = bytes(time_range.sum(), 'utf-8')
    else:
        time_range = scans['tmin'][scans['run'] == run].astype(str) \
                     + " " + scans['tmax'][scans['run'] == run].astype(str) + "\n"
        time_str = bytes(time_range.sum(), 'utf-8')

    # Run root script
    roothist = subprocess.run(cmd, input=time_str, capture_output=True, shell=True)

    # Parse root output
    counters = str(roothist.stdout, 'UTF-8')
    counters = counters.split('\n ')
    counters[0] = counters[0].replace(' ', '', 1)
    counters[-1] = counters[-1].replace('\n', '')
    counters = pd.DataFrame(counters)
    counters = counters[0].str.split(pat=' ',expand=True)

    counters.columns = ['time', 'counter', 'bxID', 'bin', 'counters']

    # Export as csv file
    counters.to_csv(f'{output_path}counters-{fill}-{run}.gz', compression="gzip")

# list_runs = [(6864, 210947),(6864, 210951)]
list_runs = [(7703, 232824)]

if __name__ == '__main__':
    # counters(6864, 210947)

    parser = arg.ArgumentParser(description='Run counter analysis.')
    parser.add_argument("-i", "--index", 
        type=int,
        help="index of analysed fill-run combination",
        default=0
    )   

    args = parser.parse_args()
    run_fill = list_runs[args.index]

    counters(run_fill[0], run_fill[1])
