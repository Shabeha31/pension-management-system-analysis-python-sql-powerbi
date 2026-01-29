#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# # •	Extraction

# In[2]:


# 1. Extraction:
df= pd.read_csv("pension_dataset_20000.csv")


# In[3]:


df.head()


# # •	Cleaning & Standardization
# 

# In[4]:


# checking null values
df.isnull().sum()


# In[17]:


# Convert to datetime
df["dob"] = pd.to_datetime(df["dob"], errors="coerce")
df["retirement_date"] = pd.to_datetime(df["retirement_date"], errors="coerce")
df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")


# In[18]:


# Remove duplicate records (if any)
df = df.drop_duplicates()
print(df.info())


# In[19]:


df.dtypes


# In[20]:


df.columns = ( df.columns .str.strip() .str.lower() .str.replace(" ", "_") .str.replace(r"[^\w_]", "", regex=True) )


# # •	Data Consistency & Derivation

# In[21]:


# Age at retirement
# Calculated only for retirees with valid dates
df["age_at_retirement"] = (df["retirement_date"] - df["dob"]).dt.days.div(365.25).round(1)
    
df["age_at_retirement"]


# In[22]:


# Pension status
df["pension_status"] = df["retirement_date"].apply(
        lambda x: "Retired" if pd.notna(x) else "Active"
    )


# In[23]:


df.head()


# In[24]:


#Re-calculating the years_of_service field
df["years_of_service"] = (df["retirement_date"] - df["join_date"]) .dt.days.div(365.25).round(1)
df["years_of_service"]      


# In[25]:


# Masking sensitive data
df["beneficiary_name"] = df["beneficiary_name"].apply(
        lambda x: "MASKED" if pd.notna(x) else pd.NA
    )

df["beneficiary_name"].head()


# In[26]:


# Save to CSV for MySQL import
csv_path = "cleaned_pensions.csv"
df.to_csv(csv_path, index=False)

print("CSV file created for MySQL import:", csv_path)


# In[59]:


#Follwing code are to transfer cleaned file to SQL

from sqlalchemy import create_engine
# MySQL credentials

username = 'root'

password = '123456789'

host = 'localhost'       

port = '3306'            # default MySQL port

database = 'Pension_database'


# Creating the SQLAlchemy engine

engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')


# Read CSV file

#df = pd.read_csv('D:\sabiha\study\Fortray\workshop\assignment_pension\pension_dataset_20000.csv')


# To Import the data into MySQL 

df.to_sql(
    name="pension_records",
    con=engine,
    if_exists="replace",
    index=False
)


print("Data imported successfully!")


# In[60]:


import os
print(os.getcwd())


# In[ ]:





# In[ ]:




