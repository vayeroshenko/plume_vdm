import pandas as pd
import numpy as np

from numpy import sqrt

from datetime import datetime as dt

# def n_bunch_type(bunch_type):
#     if (bunch_type == 'bb'):
#         return 2
#     elif (bunch_type == 'be'): 
#         return 2
#     elif (bunch_type == 'eb'):
#         return 2
#     else: 
#         return 3564 - (2+2+2)

def n_bunch_type(bunch_type):
    if (bunch_type == 'bb'):
        return 8
    elif (bunch_type == 'be'): 
        return 4
    elif (bunch_type == 'eb'):
        return 4
    else: 
        return 3564 - 12

def transform(bxid):
    return (bxid + 894 - 1) % 3564 + 1

f = 11245 

def parse_online_mu(fill):
    online_mu = pd.read_csv(f'Data/lumivar_{fill}.csv')
    # online_mu['TS'] = online_mu['TS'].apply(lambda x:  pd.Timestamp(x).timestamp())
    # 05-06-2022 05:29:59.30100000
    # online_mu['TS'] = online_mu['TS'].apply(lambda x:  x)
    online_mu['TS'] = online_mu['TS'].map(lambda x:  dt.strptime(x[:-2], '%d-%m-%Y %H:%M:%S.%f').timestamp() )
    online_mu.columns = online_mu.columns.str.replace('TS', 'time')
    online_mu.time = online_mu.time + 7200

    online_mu = online_mu.set_index(['time', ' DPE']).unstack()[' VALUE'].rename_axis([None], axis=1).reset_index()
    online_mu = online_mu.drop(online_mu.columns[online_mu.columns.str.contains('rate_coincidences_')], axis=1)

    online_mu.columns = online_mu.columns.str.replace('PLDAQTELL40:lumi_counters.', '')
    online_mu.columns = online_mu.columns.str.replace('value_', '')

    online_mu.to_csv(f"Data/lumivar_parse.{fill}.csv")
    return online_mu
  

def make_online_mu(fill):

    scans = pd.read_csv(f'Data/scans.{fill}.gz')
    scans = scans[scans.scan == 1]

  # return 
    online_mu = parse_online_mu(fill)

    scans['mu.inst'] = np.nan
    scans['mu.inst.err'] = np.nan
    scans['coinc.bb'] = np.nan
    scans['coinc.be'] = np.nan
    scans['coinc.eb'] = np.nan
    scans['coinc.ee'] = np.nan
    scans['N.bb'] = np.nan
    scans['N.be'] = np.nan
    scans['N.eb'] = np.nan
    scans['N.ee'] = np.nan

    ######### WIP: SEVERAL SCANS IN FILL
    # for step_seq in scans['step.seq'].unique():
    #     for step in scans[scans['step.seq']==step_seq].step.unique():
    #         print(scans[scans['step.seq']==step_seq][scans.step == step])

    #         tmin = scans[scans['step.seq']==step_seq][scans.step == step].tmin.values[0]
    #         tmax = scans[scans['step.seq']==step_seq][scans.step == step].tmax.values[0]
    #         scans[scans['step.seq']==step_seq][scans.step == step]['mu.inst'] = online_mu['mu_inst'][online_mu.time > tmin][online_mu.time < tmax].mean()
            
    #         # print(tmin, tmax)

    #         for variable in scans.columns:
    #             if ('coinc' in variable):
    #                 N = 'N' + variable.replace('coinc','')
    #                 ti = online_mu.dropna(subset=[variable.replace('.','_')]).time[online_mu.dropna(subset=[variable.replace('.','_')]).time < tmin].values[-1]
    #                 tf = online_mu.dropna(subset=[variable.replace('.','_')]).time[online_mu.dropna(subset=[variable.replace('.','_')]).time < tmax].values[-1]
    #                 scans[scans['step.seq']==step_seq][scans.step == step][variable] = online_mu[variable.replace('.','_')][online_mu.time > tmin][online_mu.time < tmax].sum()
    #                 scans[scans['step.seq']==step_seq][scans.step == step][N] = tf - ti

    ########### WARNING: HARDCODED QUALITY CHECK #############
    # from 2.75s to 3.5s
    # online_mu['mu.inst'] = online_mu['mu_inst'][(online_mu.timestamp > 5.5e8) & (online_mu.timestamp < 7e8)]
    # online_mu['mu_inst'] = online_mu[(online_mu['mu_inst']> 0) & (online_mu['mu_inst'] < 3e-3)]['mu_inst']
    ##########################################################

    # print(scans)
    # print(online_mu)
    # exit()

    for step in scans.step:
        tmin = scans[scans.step == step].tmin.values[0] + 2
        tmax = scans[scans.step == step].tmax.values[0]
        scans['mu.inst'][scans.step == step] = online_mu['mu_inst'][online_mu.time > tmin][online_mu.time < tmax].mean()
        scans['mu.inst.err'][scans.step == step] = sqrt(scans['mu.inst'][scans.step == step]) / \
            sqrt(3*f*n_bunch_type("bb")*online_mu['mu_inst'][online_mu.time > tmin][online_mu.time < tmax].shape[0])
        
        for variable in scans.columns:
            if ('coinc' in variable):
                N = 'N' + variable.replace('coinc','')
                mu_subset = online_mu.set_index('time')[variable.replace('.','_')].dropna()
                ti = mu_subset[mu_subset.index < tmin].index.values[-1]
                tf = mu_subset[mu_subset.index < tmax].index.values[-1]
                scans[variable][scans.step == step] = mu_subset[(mu_subset.index > tmin) & (mu_subset.index < tmax)].sum()
                scans[N][scans.step == step] = tf - ti
    
    for variable in scans.columns:
        if ('coinc' in variable):
            N = 'N' + variable.replace('coinc','')
            N0 = 'N0' + variable.replace('coinc','')
            scans[N] = scans[N]*f
            scans[N0] = scans[N] - scans[variable]/n_bunch_type(variable.replace('coinc.',''))
            scans['mu'+variable.replace('coinc','')] = -np.log(scans[N0]/scans[N])
            scans['mu.err'+variable.replace('coinc','')] = np.sqrt((1/scans[N0])-(1/scans[N]))
            scans['mu'+variable.replace('coinc','')] = scans['mu'+variable.replace('coinc','')].fillna(0.)
            scans['mu.err'+variable.replace('coinc','')] = scans['mu.err'+variable.replace('coinc','')].fillna(0.)
    scans['mu'] = scans['mu.bb'] - scans['mu.be'] - scans['mu.eb'] 

    scans['mu.err'] = np.sqrt( scans['mu.err.bb']**2 + scans['mu.err.be']**2 + scans['mu.err.eb']**2 + scans['mu.err.ee']**2 )
    
    scans = scans.drop(scans.columns[scans.columns.str.contains('N|be|eb|ee|coinc')], axis=1)

    scans_spline = pd.read_csv(f'Data/scans_spline.{fill}.gz', index_col=0)

    # Separate scans DataFrame for Beam 1 and Beam 2 variables
    B1 = scans_spline.loc[:, scans_spline.columns[~scans_spline.columns.str.contains('B2|N.2')]]
    B2 = scans_spline.loc[:, scans_spline.columns[~scans_spline.columns.str.contains('B1|N.1')]]

    # Transform Beam 2 bxid to LHCb system
    B2['bxid'] = transform(B2['bxid'])

    # Merge Beam 1 and Beam 2 DataFrames after bxid transformation
    scans_spline = pd.merge(B1, B2, how='outer', on=list(scans_spline.columns[~scans_spline.columns.str.contains('B1|B2|N.1|N.2')]))

    # scans_spline.groupby(["step","step.seq"])

    # Merge mu and scans DataFrames 
    # scans = pd.merge(scans, scans_spline, how='left', on=['tmin'])
    scans = scans.merge(scans_spline, how='left', on=['step.seq', 'step'], suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

    # bb = [895, 2131]

    ######## Average all bxid N.1*N.2 
    ######## WARNING: HARDCODED 895 AS A COLLIDING BXID. IT'S NOT NECESSARILY THE CASE
    scans["N1.N2"] = scans["N.1"] * scans["N.2"]
    scans = scans.dropna(subset=["N1.N2"])
    scans["N1.N2.av"] = scans.groupby(["step","step.seq"])["N1.N2"].transform("mean")
    scans = scans[scans.bxid==895].drop("bxid",axis=1)

    # Calculate the value of mu specific and its error
    scans['mu.inst.sp'] = 1e25 * scans['mu.inst']/(scans['N1.N2.av'])
    scans['mu.inst.sp.err'] = 1e25 * scans['mu.inst.err']/(scans['N1.N2.av'])

    scans['mu.sp'] = 1e25 * scans['mu']/(scans['N1.N2.av'])
    scans['mu.sp.err'] = 1e25 * scans['mu.err']/(scans['N1.N2.av'])
    
    # mu['mu.sp.err'] = 1e25 * mu['mu.err']/(mu['N.1']*mu['N.2'])

    scans.to_csv(f"Data/online_mu.{fill}.gz")
    scans.to_csv(f"Data/online_mu.{fill}.csv")


import argparse
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Make fake scans table')

    parser.set_defaults(overwrite=True)
    parser.add_argument("-f", "--fill", 
        type=str,
        help="Fill number",
        default="test" 
    )

    just_parse = False
    parser.add_argument('-p', "--parse", action='store_const', 
        help="Transform online counters dump and exit",
        default=just_parse, 
        const=not(just_parse))

    args = parser.parse_args()

    if args.parse:
        parse_online_mu(fill=args.fill)
        exit()

    make_online_mu(fill=args.fill)

