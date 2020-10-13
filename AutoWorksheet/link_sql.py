import pandas as pd
from sqlalchemy import create_engine
import mysql.connector

username = 'root'
password = 'Ryou017273'
hostname = 'localhost'
database = '' 

engine = create_engine("mysql://root:Ryou017273@localhost/test", echo=False)

df = pd.DataFrame({'name': ['User 1', 'User 2', 'User 3'], 'time': [10, 23, 8]})
print(df)

df.to_sql('test_new', con=engine, index=False)