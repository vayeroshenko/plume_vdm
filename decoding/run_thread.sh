#!/bin/bash

run_number="0000232824"
i_thrd=${1}

out_path="eos\/lhcb\/wg\/plume\/vdm_tuples"
out_path_norm="/eos/lhcb/wg/plume/vdm_tuples"

cp "plume2.py" "plume2_${i_thrd}.py"
sed -i "s/RUNNUMBER/$run_number/g" "plume2_$i_thrd.py"
sed -i "s/PATH/$out_path/g" "plume2_$i_thrd.py"
sed -i "s/THRD/$i_thrd/g" "plume2_$i_thrd.py"
# sed -i "s/INPUTFILE/${2}/g" "plume2_$i_thrd.py"

/afs/cern.ch/work/v/vyeroshe/cmtuser/stack2/Rec/run gaudirun.py "plume2_$i_thrd.py" > "$out_path_norm/$run_number/stdout_$i_thrd"
rm "plume2_$i_thrd.py"
