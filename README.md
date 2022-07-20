# PLUME VdM

## Requirements

See `environment.yml` file.
```
- python=3.8
- pandas
- scipy
- iminuit
- matplotlib
- numpy
```

`Snakemake` is optional but very convenient. Instructions: 
https://snakemake.readthedocs.io/en/stable/getting_started/installation.html

## Running snakemake workflow

Optimized for using with `lb-conda default`. 

```
snakemake --cores 6 all
```

To get a report on the workflow:

```
snakemake all --report
```
After which you can open your `report.html` with a browser.
To run a specific target specify a name instead of `all`


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

## Exporting the online counter data

For exporting the table with online counters from the PVSS archive run:

```
./get_online_data.sh 7650 "29-05-2022 06:00:00" "29-05-2022 10:00:00"
```

Providing the script with a desired fill number and the time range (in UTC).
