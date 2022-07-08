#!/bin/bash

source /cvmfs/sft.cern.ch/lcg/views/LCG_101/x86_64-centos7-gcc11-opt/setup.sh

# run_number="0000232824"
run_number="236561"
# run_number="236306"
i_thrd=${1}

files_per_job=1
run_type="VDM22"

out_path="eos\/lhcb\/wg\/plume\/vdm_tuples"
out_path_norm="/eos/lhcb/wg/plume/vdm_tuples"

cp "plume2.py" "plume2_${i_thrd}.py"
sed -i "s/RUNNUMBER/$run_number/g" "plume2_$i_thrd.py"
sed -i "s/RUNTYPE/$run_type/g" "plume2_$i_thrd.py"
sed -i "s/PATH/$out_path/g" "plume2_$i_thrd.py"
sed -i "s/THRD/$i_thrd/g" "plume2_$i_thrd.py"
sed -i "s/FILESPERJOB/$files_per_job/g" "plume2_$i_thrd.py"
# sed -i "s/INPUTFILE/${2}/g" "plume2_$i_thrd.py"

/afs/cern.ch/work/v/vyeroshe/cmtuser/stack2/Rec/run gaudirun.py "plume2_$i_thrd.py" > "$out_path_norm/$run_number/stdout_$i_thrd"
rm "plume2_$i_thrd.py"
