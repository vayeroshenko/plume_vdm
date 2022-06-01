import pandas as pd
from datetime import datetime as dt


def make_fake_steps(fill, run, tminmin):
	d = {'step.seq': [1]*5,
	     'step': [1, 3, 5, 7, 9],
	     'run': [run]*5,
	     'tmin': [tminmin, tminmin+20, tminmin+40, tminmin+60, tminmin+80],
	     'time': [tminmin+5, tminmin+25, tminmin+45, tminmin+85, tminmin+85],
	     'tmax': [tminmin+10, tminmin+30, tminmin+50, tminmin+70, tminmin+90],
	     'x1.set': [-0.372203, -0.330847, -0.289491, -0.248136, -0.206780],
	     'x2.set': [0.37220335, 0.33084742, 0.28949149, 0.24813557, 0.20677964],
	     'y1.set': [0., 0., 0., 0., 0.],
	     'y2.set': [0., 0., 0., 0., 0.],
	     'scan': [1]*5,
	     'subscan': ['Symmetric_X', 'Symmetric_X', 'Symmetric_X', 'Symmetric_X', 'Symmetric_X'],
	    }
	df = pd.DataFrame(data=d)

	df.to_csv(f'Data/scans.{fill}.gz')

if __name__ == '__main__':
	run = 231668
	
	timestamp = dt(2022, 5, 29, 12 - 2, 8, 50).timestamp()

	# tminmin = timestamp  + 35
	tminmin = 1653811200.0  + 35

	make_fake_steps(fill="test", run=run, tminmin=tminmin)