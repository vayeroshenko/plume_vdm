import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import uncertainties

# Define gaussian distribution in one dimension
def gaussFunction(x, A, x0, sigma):
    return A*np.exp(-(x-x0)**2/(2*sigma**2))

# Define function that computes cross section for each counter, bxid and scan
def CrossSection(mu, counter, bxid, scan):
    # Separate dataframes for x and y 
    step_sym_x = mu[mu.scan == scan][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Symmetric_X"]
    step_sym_y = mu[mu.scan == scan][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Symmetric_Y"]
    
    # Set delta columns
    step_sym_x["delta_x"] = step_sym_x["x2.set"] - step_sym_x["x1.set"]
    step_sym_y["delta_y"] = step_sym_y["y2.set"] - step_sym_y["y1.set"]
    
    
    # Fit x and y distributions
    fit = {}
    fit['x'], fit['x.err'] = curve_fit(
        gaussFunction, 
        step_sym_x['delta_x'].values, 
        step_sym_x['mu.sp'].values,
        p0 = [170, 0, 0.15],
        sigma = step_sym_x['mu.sp.err'].values
    )
    fit['y'], fit['y.err'] = curve_fit(
        gaussFunction, 
        step_sym_y['delta_y'].values, 
        step_sym_y['mu.sp'].values,
        p0 = [160, 0, 0.15],
        sigma = step_sym_y['mu.sp.err'].values
    )

    # Get parameters errors from convolution matrix
    fit['x.err'] = np.sqrt(np.diag(fit['x.err']))
    fit['y.err'] = np.sqrt(np.diag(fit['y.err'])) 
    
    # Get integral values
    Ax = fit["x"][0] * np.sqrt(2*np.pi*fit["x"][2]**2)
    Ax_err = Ax * step_sym_x['mu.sp.err'].sum() / step_sym_x['mu.sp'].sum()
    Ay = fit["y"][0] * np.sqrt(2*np.pi*fit["y"][2]**2)
    Ay_err = Ay * step_sym_y['mu.sp.err'].sum() / step_sym_y['mu.sp'].sum()
    
    # Obtain mu max value
    # mu_max = mu['mu.sp'][mu.scan == 1][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Zero"].mean()
    # mu_max_err = mu['mu.sp.err'][mu.scan == 1][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Zero"].mean()

    mu_max = 1
    mu_max_err = 0.01

    
    sigma = Ax * Ay / mu_max
    
    sigma_err = sigma * np.sqrt((Ax_err/Ax)**2+(Ay_err/Ay)**2+(mu_max_err/mu_max)**2)
    
    return sigma, sigma_err, fit

# Define function that plots mu specific for each counter, bxid and scan
def plot1D(mu, counter, bxid, scan, fit):
    # Separate dataframes for x and y 
    step_sym_x = mu[mu.scan == scan][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Symmetric_X"]
    step_sym_y = mu[mu.scan == scan][mu.counter == counter][mu.bxid == bxid][mu.subscan == "Symmetric_Y"]
    
    # Set delta columns
    step_sym_x["delta_x"] = step_sym_x["x2.set"] - step_sym_x["x1.set"]
    step_sym_y["delta_y"] = step_sym_y["y2.set"] - step_sym_y["y1.set"]
    
    # Plot x distribution
    mu_x = plt.figure(figsize=(12, 8))
    plt.errorbar(
        step_sym_x.delta_x.values, 
        step_sym_x['mu.sp'].values,
        yerr = step_sym_x['mu.sp.err'].values,
        marker = 'o',
        linestyle = '',
        label = f'lc-{counter}'
    )
    plt.plot(
        np.arange(-0.8,0.8,0.01), 
        gaussFunction(
            np.arange(-0.8,0.8,0.01), 
            *fit["x"]
        ),
        linestyle = '-',
        label = f'fit\n area = {round(fit["x"][0],3)} \u00B1 {round(fit["x.err"][0],3)} \n' + \
                f'mean = {round(fit["x"][1],3)} \u00B1 {round(fit["x.err"][1],3)} \n' + \
                f'sigma = {round(fit["x"][2],3)} \u00B1 {round(fit["x.err"][2],3)}'
    )
    plt.legend()
    plt.xlabel('\u0394 X [mm]')
    plt.ylabel('\u03BC specific')
    plt.title(f'lc - {counter}, bxid {bxid}')
    plt.savefig(f'Plots/Symmetric X/fill-{fill}.run-{run}.scan-{int(scan)}.lc-{counter}.bxid-{bxid}.pdf')
    plt.close(mu_x)
    
    # Plot y distribution
    mu_y = plt.figure(figsize=(12, 8))
    plt.errorbar(
        step_sym_y.delta_y.values, 
        step_sym_y['mu.sp'].values,
        yerr = step_sym_y['mu.sp.err'].values,
        marker = 'o',
        linestyle = '',
        label = f'lc-{counter}'
    )
    plt.plot(
        np.arange(-0.8,0.8,0.01), 
        gaussFunction(
            np.arange(-0.8,0.8,0.01), 
            *fit["y"]
        ),
        linestyle = '-',
        label = f'fit\n area = {round(fit["y"][0],3)} \u00B1 {round(fit["y.err"][0],3)} \n' + 
                f'mean = {round(fit["y"][1],3)} \u00B1 {round(fit["y.err"][1],3)} \n' + 
                f'sigma = {round(fit["y"][2],3)} \u00B1 {round(fit["y.err"][2],3)}'
    )
    plt.legend()
    plt.xlabel('\u0394 Y [mm]')
    plt.ylabel('\u03BC specific')
    plt.title(f'lc - {counter}, bxid {bxid}')
    plt.savefig(f'Plots/Symmetric Y/fill-{fill}.run-{run}.scan-{int(scan)}.lc-{counter}.bxid-{bxid}.pdf')
    plt.close(mu_y)


def run_vdm_offline(fill, run):
    # Read mu DataFrame 
    mu = pd.read_csv(f'Data/mu.{fill}.{run}.gz', index_col=0).dropna()

    # Define columns for new DataFrame for cross section and create empty DataFrame
    xsec_columns = ['counter', 'bxid', 'scan', 'xsec', 'xsec.err']
    xsec = pd.DataFrame()



    # Compute cross section and plot mu specific for x and y for each counter, bxid and scan
    for scan in mu.scan.unique():
        if ("Symmetric_X" not in mu['subscan'][mu['scan']==scan].unique()
           or "Symmetric_Y" not in mu['subscan'][mu['scan']==scan].unique()): break
        for counter in mu['counter'][mu['scan']==scan].unique():
            for bxid in mu['bxid'][mu['counter']==counter][mu['scan']==scan].unique():
                sigma, sigma_err, fit = CrossSection(mu, counter, bxid, scan)
                row = pd.DataFrame([[counter, bxid, scan, sigma, sigma_err]], columns=xsec_columns)
                xsec = pd.concat([xsec, row], ignore_index=True)
                plot(mu, counter, bxid, scan, fit)     

    # DataFrame is saved as gz compressed file
    xsec.to_csv(f'Data/xsec.{fill}.{run}.gz', compression='gzip')

    print(xsec)

    # Group cross section by counter and scan and get average values
    xsec_avg = xsec.groupby(['counter', 'scan']).mean().drop(['bxid','xsec.err'], axis=1).reset_index()
    errors = list()
    # Compute cross section mean errors
    for scan in xsec.scan.unique():
        for counter in xsec['counter'][xsec['scan']==scan].unique():
            sq_vals =  np.power(xsec['xsec.err'][xsec['scan']==scan][xsec['counter']==counter].values, 2)
            errors.append((1/xsec[xsec['scan']==scan][xsec['counter']==counter].shape[0]) * np.sqrt(sq_vals.sum()))

    xsec_avg['xsec.err'] = np.array(errors)

    # DataFrame is saved as gz compressed file
    xsec_avg.to_csv(f'Data/xsec_avg.{fill}.{run}.gz', compression='gzip')

import argparse
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Make VdM scan ')
    parser.add_argument('--overwrite', action='store_true', 
        help="Recalculate interpolation (takes time)")
    parser.add_argument('--no-overwrite', dest='overwrite', action='store_false',
        help="Use stored interpolated values from DC and FAST")
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
    
    run_vdm_offline(fill=args.fill, run=args.run)


