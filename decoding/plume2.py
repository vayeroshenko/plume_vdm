###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

run_number = 'RUNNUMBER'
partition = 'LHCb'  ### or 'PLUME'
#partition = 'PLUME'
import glob
from Gaudi.Configuration import VERBOSE, INFO

from PyConf.application import (
    default_raw_event,
    configure_input,
    configure,
    make_odin,
    ApplicationOptions,
    CompositeNode,
)
from PyConf.Algorithms import (
    PlumeRawToDigits,
    PlumeDigitMonitor,
    PlumeTuple,
)

options = ApplicationOptions(_enabled=False)

options.input_type = "RAW"
### run_number = 1022

# if partition == 'LHCb':
# 	options.input_files = [ 
# 		list(glob.glob(f'/eos/lhcb/point8/lhcb/data/2022/RAW/FULL/LHCb/CALIBRATION22/{run_number}/*.raw'))[THRD], ]

low = int(THRD*FILESPERJOB)
high = int(low+FILESPERJOB)


if partition == 'LHCb':
    list_files = list(glob.glob(f'/eos/lhcb/point8/lhcb/data/2022/RAW/FULL/LHCb/RUNTYPE/{run_number}/*.raw'))
    if high < len(list_files):
        list_files = list_files[low:high]
    else: 
        list_files = list_files[low:]
    options.input_files = list_files
        # list(glob.glob(f'/eos/lhcb/point8/lhcb/data/2022/RAW/FULL/LHCb/COLLISION22/{run_number}/*.raw'))[THRD*20:(THRD+1)*20]

else:
    options.input_files = [ 
        list(glob.glob(f'/eos/lhcb/point8/PLUME/{run_number}/Run_{run_number}*.mdf'))[THRD], ]
# else:
# 	options.input_files = list(
# 		glob.glob(
# 			f'/eos/lhcb/point8/PLUME/0000232824/INPUTFILE'))


options.dddb_tag = 'dddb-20210617'
options.conddb_tag = 'sim-20210617-vc-md100'
# options.evt_max = NEVT
# options.first_evt = FIRST
options.evt_max = -1
#options.n_threads=5
#options.n_event_slots=-1
options.histo_file = f'/PATH/{run_number}/plume_decoding_allch_{run_number}_THRD.root'
options.ntuple_file = f'/PATH/{run_number}/plume_ntuple_allch_{run_number}_THRD.root'
options.monitoring_file = f"/PATH/{run_number}/plume_decoding_THRD.json"
configure_input(options)  # must call this before calling default_raw_event
odin = make_odin()

read_all_channels = False

digits = PlumeRawToDigits(
    ReadAllChannels=read_all_channels, OutputLevel=INFO,
    RawEventLocation=default_raw_event(["Plume"])).Output

monitor = PlumeDigitMonitor(Input=digits, 
                            # OutputLevel=VERBOSE,
                            #adcThldRegMon=500,
                            ODIN=odin) 

plume_tuple = PlumeTuple(
    Input=digits,
    ODIN=odin,
    OutputLevel=INFO,
    ReadAllChannels=read_all_channels)

top_node = CompositeNode("Top", [plume_tuple, monitor])
configure(options, top_node)
