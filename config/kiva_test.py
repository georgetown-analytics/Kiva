from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from config import dbconfig

engine = create_engine(dbconfig.aws_connection_string)
data = pd.read_sql_query("SELECT * FROM kiva_data_flat", engine)