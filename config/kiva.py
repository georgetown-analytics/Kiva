from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine('sqlite:///config/kiva_data_flat.db')
Kiva = pd.read_sql_query("SELECT * FROM kiva_data_flat", engine)
