import pandas as pd
import numpy as np

from datetime import datetime as dt

def make_online_mu(fill):

    scans = pd.read_csv(f'Data/scans.{fill}.gz')
    scans = scans[scans.scan == 1]

    online_mu = pd.read_csv(f'Data/lumivar_{fill}.csv')
    # online_mu['TS'] = online_mu['TS'].apply(lambda x:  pd.Timestamp(x).timestamp())
    # 05-06-2022 05:29:59.30100000
    # online_mu['TS'] = online_mu['TS'].apply(lambda x:  x)
    online_mu['TS'] = online_mu['TS'].apply(lambda x:  dt.strptime(x[:-2], '%d-%m-%Y %H:%M:%S.%f').timestamp() )
    online_mu.columns = online_mu.columns.str.replace('TS', 'time')

    # print(online_mu)
    # print(scans)

    online_mu = online_mu.set_index(['time', ' DPE']).unstack()[' VALUE'].rename_axis([None], axis=1).reset_index()
    online_mu = online_mu.drop(online_mu.columns[online_mu.columns.str.contains('rate_coincidences_')], axis=1)

    online_mu.columns = online_mu.columns.str.replace('PLDAQTELL40:lumi_counters.', '')
    online_mu.columns = online_mu.columns.str.replace('value_', '')

    online_mu.to_csv(f"Data/lumivar_parse.{fill}.csv")
    # return 

    scans['mu.inst'] = np.nan
    scans['coinc.bb'] = np.nan
    scans['coinc.be'] = np.nan
    scans['coinc.eb'] = np.nan
    scans['coinc.ee'] = np.nan
    scans['N.bb'] = np.nan
    scans['N.be'] = np.nan
    scans['N.eb'] = np.nan
    scans['N.ee'] = np.nan

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


    for step in scans.step:
        print(scans[scans.step == step])
        tmin = scans[scans.step == step].tmin.values[0]
        tmax = scans[scans.step == step].tmax.values[0]
        scans['mu.inst'][scans.step == step] = online_mu['mu_inst'][online_mu.time > tmin][online_mu.time < tmax].mean()
        
        for variable in scans.columns:
            if ('coinc' in variable):
                N = 'N' + variable.replace('coinc','')
                ti = online_mu.dropna(subset=[variable.replace('.','_')]).time[online_mu.dropna(subset=[variable.replace('.','_')]).time < tmin].values[-1]
                tf = online_mu.dropna(subset=[variable.replace('.','_')]).time[online_mu.dropna(subset=[variable.replace('.','_')]).time < tmax].values[-1]
                scans[variable][scans.step == step] = online_mu[variable.replace('.','_')][online_mu.time > tmin][online_mu.time < tmax].sum()
                scans[N][scans.step == step] = tf - ti

    f = 11245 

    def n_bunch_type(bunch_type):
        if (bunch_type == 'bb'):
            return 2
        elif (bunch_type == 'be'): 
            return 2
        elif (bunch_type == 'eb'):
            return 2
        else: 
            return 3564 - (2+2+2)

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
    
    # scans=scans[["mu.bb","mu.err.bb","mu","mu.err","mu.inst"]] 
    scans = scans.drop(scans.columns[scans.columns.str.contains('N|be|eb|coinc')], axis=1)

    # steps = pd.read_csv(f"Data/scans_spline.{fill}.gz")
    

    # steps = steps.merge(scans, how='left', on=['step.seq', 'step'], suffixes=('', '_DROP')).filter(regex='^(?!.*_DROP)')

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

    args = parser.parse_args()
    make_online_mu(fill=args.fill)

