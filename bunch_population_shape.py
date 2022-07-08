import pandas as pd
# import dask.dataframe as dd
from ast import literal_eval

n_lines_max = 10000

def make_ana_fbct(data):
    data['nxcals_value'] = data['nxcals_value'].apply(lambda x: literal_eval(x.replace(" ", ",")) )
    data = data.drop('nxcals_entity_id',axis=1)
    data = data.rename(columns={"nxcals_value": "nxcals_N", 'nxcals_timestamp': 'time' })
    data = data.explode('nxcals_N')
    data['bxid'] = data.groupby(['time', 'nxcals_variable_name']).cumcount()+1
    data = data[data.nxcals_N != 0]
    # data.columns = data.columns.str.replace('nxcals_timestamp', 'time')
    # print(data.compute())
    # data["nxcals_variable_name"] = data["nxcals_variable_name"].apply(lambda x: x.extract('(.*B[1-2])') )
    data = data.reset_index(drop=True)
    # data.time = data.time - 7200.e9

    # data = data.iloc[:, [0,3,1,2]]
    # data = data.compute()
    data["nxcals_variable_name"] = data["nxcals_variable_name"].str.extract('(.*B[1-2])')
    data["nxcals_variable_name"].replace('^LHC\\.','',regex=True, inplace = True)
    
    data = data.set_index(['time', 'bxid', 'nxcals_variable_name']).unstack()
    data = data.nxcals_N.rename_axis([None], axis=1).reset_index()

    # print(data)
    return data

def shape_fbct(name="test"):

    chunks = pd.read_csv(f"Data/fast.raw.{name}.csv", 
        dtype={ "nxcals_value": str, 
                "nxcals_entity_id": int, 
                "nxcals_timestamp": int, 
                "nxcals_variable_name": str},
        chunksize=n_lines_max)
    
    # make_ana_fbct(next(chunks)).to_csv(f"Data/fast.{name}.csv", encoding='utf-8', index=False, sep=',')
    # print(f"Fast chunk # 0")

    i_chunk = 0
    for chunk in chunks:
        # make_ana_fbct(chunk).to_csv(f"Data/fast.{name}.part_{i_chunk}.csv", mode="a", encoding='utf-8', index=False,sep=',')
        fbct_data = make_ana_fbct(chunk)
        fbct_data.to_csv(f"Data/fast.{name}.part_{i_chunk}.csv", encoding='utf-8', index=False,sep=',')
        fbct_data.to_csv(f"Data/fast.{name}.part_{i_chunk}.gz", encoding='utf-8', index=False,sep=',')
        print(f"Fast chunk # {i_chunk}")
        i_chunk += 1
        # if i_chunk > 3: break

    print("CSV saved successfully! (FAST)")

def shape_dc(name="test"):
    data = pd.read_csv(f"Data/dc.raw.{name}.csv", 
        dtype={ "nxcals_value": float, 
                    "nxcals_entity_id": int, 
                    "nxcals_timestamp": int, 
                    "nxcals_variable_name": str})

    # data = data.iloc[:, [1,2,3,0]]
    data = data.drop('nxcals_entity_id',axis=1)
    data.columns = data.columns.str.replace('nxcals_value', 'nxcals_N')
    data.columns = data.columns.str.replace('nxcals_timestamp', 'time')
    # data.time = data.time - 7200.e9
    # data = data.compute()
    data["nxcals_beam"] = data["nxcals_variable_name"].str.extract('.*\\.?B([1-2]).*')
    data = data.set_index(['time', 'nxcals_variable_name']).unstack()
    data = data.nxcals_N.rename_axis([None], axis=1).reset_index()
    data.to_csv(f"Data/dc.{name}.csv")
    data.to_csv(f"Data/dc.{name}.gz")
    print("CSV saved successfully! (DC)")


# shape_fbct(name="7822")
# shape_dc(name="7822")

import argparse
if __name__ == '__main__':
    # Set fill and run of the counter

    parser = argparse.ArgumentParser(description='Transform BCT data')

    parser.set_defaults(overwrite=True)
    parser.add_argument("-f", "--fill", 
        type=str,
        help="Fill number",
        default="test" 
    )

    args = parser.parse_args()

    # fill = "test"
    # run = 231703
    
    # make_offline_mu(fill=args.fill, run=args.run)
    # shape_fbct(name=args.fill)
    shape_dc(name=args.fill)

# spark.sparkContext.parallelize([export_fbct, export_dc]).map(lambda x: x(time, name="7822") ).collect()
