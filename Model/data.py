import pandas as pd
import numpy as np
from kivadataloader import KivaDataLoader

m=KivaDataLoader()
cleaneduploans=m.get_clean_dataframe()
cleaneduploans['fol']=np.where(cleaneduploans['posted_to_raised_days']<=5,0,1)
data=cleaneduploans.drop(['posted_to_raised_days','posted_to_raised_bins', 'disburse_to_posted_days','disbursed_to_raised_days',
'loan_id','partner_id', 'funded_amount','loan_image_provided','atleast1_borrower_pictured','distribution_model_field_partner',
'num_borrowers', 'num_borrowers_male', 'num_borrowers_female', 'num_journal_entries','num_bulk_entries','loan_video_provided',
'sector_name_Food','repayment_interval_monthly'], axis=1)
data=data.drop([col for col in data.columns if 'partner_' in col],axis=1)
data=data.select_dtypes(exclude=['object','datetime64[ns, UTC]'])
data['description_length'].fillna(0,inplace=True)
data['loan_use_length'].fillna(0,inplace=True)
data.dropna(axis=1, inplace=True)
data.to_csv('data.csv', index=False)
