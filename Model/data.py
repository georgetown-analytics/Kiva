import pandas as pd
import numpy as np

#Hack because python is odd
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from ingestion.kivadataloader import KivaDataLoader

m=KivaDataLoader()
cleaneduploans=m.get_clean_dataframe()
#cleaneduploans=pd.concat([cleaneduploans,pd.get_dummies(cleaneduploans['country_name'], prefix='country_name')],axis=1)
cleaneduploans.to_csv('data.csv', index=False)
