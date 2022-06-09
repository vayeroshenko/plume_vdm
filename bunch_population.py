from nxcals.api.extraction.data.builders import *

import os
from nxcals import spark_session_builder
from pyspark.sql import SparkSession
from nxcals.spark_session_builder import Flavor

os.environ['PYSPARK_PYTHON']="./environment/bin/python"

spark = spark_session_builder.get_or_create(flavor=Flavor.YARN_MEDIUM, 
    conf={'spark.executor.memory': '20g'},
    hadoop_env="pro")
print(spark.sparkContext.parallelize(range(1)).map(lambda x: x).collect())

# import pandas as pd

# spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

def export_fbct(time_range, name="test"):
    start, end = time_range
    data = DataQuery.builder(spark).byVariables() \
        .system('CMW') \
        .startTime(start).endTime(end) \
        .variableLike('LHC.BCTFR.%:BUNCH_INTENSITY') \
        .variableLike('ATLAS.BPTX.%:BUNCH_INTENSITIES') \
        .build() \
        .toPandas()
    
    print("Data is extracted, analysing...")
#     data = pd.DataFrame.from_records(data.collect(), columns=data.columns)
    data['nxcals_N'] = data['nxcals_value'].map(lambda x: x['elements'])
    data = data.drop('nxcals_value',axis=1)
    data = data.drop('nxcals_entity_id',axis=1)
    data = data.explode('nxcals_N')
    data['bxid'] = data.groupby(['nxcals_timestamp', 'nxcals_variable_name']).cumcount()+1
    data = data[data.nxcals_N != 0]
    data["nxcals_variable_name"] = data["nxcals_variable_name"].str.extract('(.*B[1-2])')
    data["nxcals_variable_name"].replace('^LHC\\.','',regex=True, inplace = True)
    data = data.reset_index(drop=True)
    data = data.iloc[:, [0,3,1,2]]
    data.columns = data.columns.str.replace('nxcals_timestamp', 'time')
    # data.time = data.time - 7200.e9
    data = data.set_index(['time', 'bxid', 'nxcals_variable_name']).unstack()
    data = data.nxcals_N.rename_axis([None], axis=1).reset_index()
    data.to_csv(f"Data/fast.{name}.csv")
    print("CSV saved successfully! (FAST)")

def export_dc(time_range, name="test"):
    start, end = time_range
    data = DataQuery.builder(spark).byVariables() \
        .system('CMW') \
        .startTime(start).endTime(end) \
        .variableLike('LHC.BCTDC.%:BEAM_INTENSIT%') \
        .build() \
        .toPandas()

    print("Data is extracted, analysing...")
#     data = pd.DataFrame.from_records(data.collect(), columns=data.columns)
    data = data.iloc[:, [1,2,3,0]]
    data = data.drop('nxcals_entity_id',axis=1)
    #data["nxcals_beam"] = data["nxcals_variable_name"].str.extract('.*\\.?B([1-2]).*')
    data.columns = data.columns.str.replace('nxcals_value', 'nxcals_N')
    data.columns = data.columns.str.replace('nxcals_timestamp', 'time')
    # data.time = data.time - 7200.e9
    data = data.set_index(['time', 'nxcals_variable_name']).unstack()
    data = data.nxcals_N.rename_axis([None], axis=1).reset_index()
    data.to_csv(f"Data/dc.{name}.csv")
    print("CSV saved successfully! (DC)")

# time = ('2022-05-29 10:00:00.000', '2022-05-29 10:30:00.000')
# time = ('2022-06-05 05:30:00.000', '2022-06-05 08:00:00.000') ## Fill 7702
time = ('2022-06-05 14:30:00.000', '2022-06-05 17:00:00.000') ## Fill 7703

export_fbct(time, name="7703")
export_dc(time, name="7703")

