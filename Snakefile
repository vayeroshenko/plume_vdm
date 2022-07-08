
fill = "7923"
run = 236561


# rule all:
#   input:  f'Data/xsec.{fill}.{run}.gz', 
#           f'Data/xsec_avg.{fill}.{run}.gz', 
rule all:
    input:  f'Data/mu.{fill}.{run}.gz', 
            f'Data/online_mu.{fill}.gz', 

rule mu_off:
    input:  f'Data/mu.{fill}.{run}.gz'

rule mu_on:
    input:  f'Data/online_mu.{fill}.gz' 



rule vdm_1d:
    input: 'Data/mu.{fill}.{run}.gz',
    output: 'Data/xsec.{fill}.{run}.gz', 'Data/xsec_avg.{fill}.{run}.gz'
    shell: "python vdm.py --fill {wildcards.fill} --run {wildcards.run} --overwrite"

#rule make_fake_steps:
#   output: "Data/scans.{fill}.gz"
#   shell: "python make_fake_steps.py --fill {wildcards.fill} "

rule offline_mu:
    input:
        counters = "Data/counters.{fill}.{run}.gz",
        scans = "Data/scans_spline.{fill}.gz"
    output: "Data/mu.{fill}.{run}.gz"
    shell: "python offline_mu.py --fill {wildcards.fill} --run {wildcards.run}"

rule online_mu:
    input:
        counters = "Data/lumivar_{fill}.csv",
        scans = "Data/scans.{fill}.gz",
        scans_spline = "Data/scans_spline.{fill}.gz"
    output: "Data/online_mu.{fill}.gz"
    shell: "python online_mu.py --fill {wildcards.fill}"

# rule counters_hist:
#     input:
#         bin = "plume_root_counters/step_hist",
#         scans = "Data/scans.{fill}.gz"
#     output: "Data/counters.{fill}.{run}.gz"
#     shell: "python make_counters.py --fill {wildcards.fill} --run {wildcards.run} --overwrite"


################## Rules to make steps (scans spline)
rule bunch_pop_shape:
    input:
        dc = "Data/dc.raw.{fill}.csv",
        fast = "Data/fast.raw.{fill}.csv"
    output: "Data/dc.{fill}.gz", "Data/fast.{fill}.part_0.gz"
    shell: "python bunch_population_shape.py --fill {wildcards.fill}"

rule scans_spline:
    input:
        scans= "Data/scans.{fill}.gz",
        dc = "Data/dc_spline.{fill}.gz",
        fast = "Data/fast_spline.{fill}.gz"
    output: "Data/scans_spline.{fill}.gz"
    shell: "python make_steps.py --fill {wildcards.fill} --steps"

rule make_fast_spline:
    input: "Data/scans.{fill}.gz", "Data/fast.{fill}.part_0.gz"
    output: "Data/fast_spline.{fill}.gz"
    shell: "python make_steps.py --fill {wildcards.fill} --fast"

rule make_dc_spline:
    input: "Data/scans.{fill}.gz", "Data/dc.{fill}.gz"
    output: "Data/dc_spline.{fill}.gz"
    shell: "python make_steps.py --fill {wildcards.fill} --dc"
###################################


# rule bct_data:
#   output: "Data/dc.{fill}.csv", "Data/fast.{fill}.csv"
#   run: print("Please run BCT export code")



rule compile_counter_hist:
    output: "plume_root_counters/step_hist"
    shell: "cd plume_root_counters; make; cd .."
