from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from config import dbconfig
import sqlite3

#creating full_loans data set from database
engine = create_engine(dbconfig.aws_connection_string)
days = pd.read_sql_query("SELECT * FROM loan_dates", engine)
loans = pd.read_sql_query("SELECT * FROM loans", engine)
partners = pd.read_sql_query("SELECT * FROM partners", engine)
loans_days = pd.merge(loans, days, how = 'left', on = 'loan_id')
partners = partners.rename(columns = {"id": "partner_id"})
full_loans = pd.merge(loans_days, partners, how = "left", on = "partner_id", suffixes=("_loans", "_partners"))
print("Successfully downloaded Kiva data from AWS and merged loan data with partner data")

# creating a subset only with field partner loans
fl_subset = full_loans[full_loans.distribution_model == "field_partner"]
print("Subset only with field partner loans")

#creating a new binary variable that is 0 if the loan was successfully funded and 1 otherwise
fl_subset["status_loans_bi"] = np.where(fl_subset["status_loans"] == "funded", 0, 1)
print("Create successful loan flag")

#Cleaning data set to select only funded loans and get rid of negative values in posted_to_raised_days
fl_subset_cl = fl_subset[fl_subset.status_loans_bi == 0]
fl_subset_cl = fl_subset_cl[fl_subset_cl.posted_to_raised_days >= 0]
print("Selecting only funded loans and getting rid of negative values in posted_to_raised_days")

fl_subset_cl['posted_time_actual'] = fl_subset_cl['posted_time_actual'].astype('int64')
fl_subset_cl['disburse_time_actual'] = fl_subset_cl['disburse_time_actual'].astype('int64')
fl_subset_cl['raised_time_actual'] = fl_subset_cl['raised_time_actual'].astype('int64')
print("Converted datetime64 to int64")

sqlite3_engine = create_engine('sqlite:///config/kiva_data_flat.db')

fl_subset_cl.to_sql('kiva_data_flat', con=sqlite3_engine, if_exists='replace')
print("Created local sqlite3 db named kiva_data_flat")
