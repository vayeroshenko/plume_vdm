# PLUME VdM

## Setting up NXCALS environment on lxplus and extracting data from NXCALS

### Source
https://nxcals-docs.web.cern.ch/current/user-guide/data-access/access-methods/#nxcals-spark-bundle

### Instructions

1) Create venv with NXCALS and necessary packages

In a working directory: 
```
python3 -m venv ./venv
source ./venv/bin/activate
python -m pip install git+https://gitlab.cern.ch/acc-co/devops/python/acc-py-pip-config.git
python -m pip install nxcals
python -m pip install pandas
```

2) Every new login:

- Set up the environment
```
cd path/to/working/dir
source ./venv/bin/activate
kinit
```

- Launch local `pyspark` session

```
pyspark --executor-cores 4 --executor-memory 5G --conf spark.driver.memory=20G
```
Adjust worker and driver memory quota for your needs.

- Launch `bunch_population`

```
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.2.1
      /_/

Using Python version 3.9.12 (main, Mar 24 2022 23:25:59)
Spark context Web UI available at http://lxplus746.cern.ch:5201
Spark context available as 'sc' (master = local[*], app id = local-1653575873034).
SparkSession available as 'spark'.
>>> 
>>> import bunch_population
```

## Merging BCT data with scans table

### Usage:
```
python make_steps.py --overwrite --fill 1234
```
The `--no-overwrite` option means the interpolated BCT data at the centers of the steps will be read from the stored tables instead of re-runing the interpolation again. This can save a lot of time since the interpolation algorithm is time consuming.
- Known issue: it will fail with `--no-overwrite` option if the corresponding files don't exist.
