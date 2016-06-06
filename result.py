#Post1
#https://collegescorecard.ed.gov/assets/FullDataDocumentation.pdf 

#All the libraries that I need
%matplotlib inline 

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
import statsmodels.api as sm
from statsmodels.formula.api import ols

import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("poster")

# special matplotlib argument for improved plots
from matplotlib import rcParams

#Read CSV file into Pandas DataFrame
data = pd.read_csv("merged_2013_PP.csv")

#givin list of columns, drop those columns in dataframe
def drop_cols(cols, DF):
    #given array of column names, it drops all the columns in DF
    count = len(cols) #get how many columns you want to get rid of 
    start = 0
    cols_in_DF = DF.columns.values
    cols_in_DF = cols_in_DF.tolist()
    while start < count:
        #make sure column exists in DataFrame
        if(cols[start] in cols_in_DF):
            DF = DF.drop(cols[start],1)
            start = start + 1
            print("Succ")
        else:
            print("Column does not exist in the DataFrame")
            return
    return DF

#given list of columns, only keep those columns in dataframe
def keep_these_cols(cols, DF):
    #Only keep colums that are in cols list
    start = 0
    cols_in_DF = DF.columns.values
    cols_in_DF = cols_in_DF.tolist()
    count = len(cols_in_DF)
    while start < count:
        #make sure column exists in DataFrame
        if(cols_in_DF[start] in cols):
            start = start + 1
        else:
            DF = DF.drop(cols_in_DF[start],1)
            start = start + 1
    return DF

#This is columns that I only need
cols_I_Want = ['INSTNM','ADM_RATE', 'SATVR25','SATVR75','SATMT25','SATMT75','SATWR25','SATWR75',
 'SATVRMID','SATMTMID','SATWRMID','ACTCM25','ACTCM75','ACTEN25','ACTEN75','ACTMT25','ACTMT75',
 'ACTWR25','ACTWR75','ACTCMMID','ACTENMID','ACTMTMID','ACTWRMID','SAT_AVG','SAT_AVG_ALL','UGDS_WHITE',
 'UGDS_BLACK','UGDS_HISP','UGDS_ASIAN','COSTT4_A','COSTT4_P','INC_PCT_LO','INC_PCT_M1','INC_PCT_M2',
 'INC_PCT_H1','INC_PCT_H2','RET_FT4','RET_FTL4','RET_PT4','RET_PTL4']

#copy the data so I won't mess up with the original data
use_data = data;

#get only the columns that I need
filtered_data = keep_these_cols(cols_I_Want, use_data)

#We want to drop every row that has too many NaN values
dropped_NaN_Data = filtered_data.dropna(subset=['ADM_RATE', 'SATVR25'])

#************************Question 1: Is there relationship between total SAT score, and admissions rate?************************
#do it for every year and see if that is changing 
Question1 = dropped_NaN_Data
Question1['TOTAL_SAT_SCORE'] = 0
#Add the scores
Questions1.TOTAL_SAT_SCORE = Questions1.SATMT75 + Questions1.SATVR75 + Questions1.SATWR75


#Graph Scatter plot to see if there is a realtioship
plt.scatter(Questions1.TOTAL_SAT_SCORE, Questions1.ADM_RATE)
plt.xlabel("Total SAT score out of 2400")
plt.ylabel("Acceptance rate")
plt.title("Relationship between total SAT score and Acceptance rate")

#This graph also gives best fit line
sns.regplot(y="ADM_RATE", x="TOTAL_SAT_SCORE", data=Questions1, fit_reg = True)

#This histogram plot shows how many schools for acceptance rate
plt.hist(Questions1.ADM_RATE)

#get the other years data
data_2008 = pd.read_csv("merged_2008_PP.csv")
data_2009 = pd.read_csv("merged_2009_PP.csv")
data_2010 = pd.read_csv("merged_2010_PP.csv")
data_2011 = pd.read_csv("merged_2011_PP.csv")
data_2012 = pd.read_csv("merged_2012_PP.csv")


#We want to look at multiple data files, lets create clean up function
def extract_data(cols_extract, DataF):
    #extract columns that I want
    result = keep_these_cols(cols_extract, DataF)
    #now get rid of all NaN rows
    new_result = result.dropna(subset=['ADM_RATE', 'SATVR75', 'SATMT75', 'SATWR75'])
    
    #Now, create TOTAL_SAT_SCORE column
    new_result['TOTAL_SAT_SCORE'] = 0
    
    #calculate 
    new_result.TOTAL_SAT_SCORE = new_result.SATMT75 + new_result.SATVR75 + new_result.SATWR75
    
    return new_result

#need to run extract_data function to all data
extracted_data_2008 = extract_data(cols_I_Want, data_2008)
extracted_data_2009 = extract_data(cols_I_Want, data_2009)
extracted_data_2010 = extract_data(cols_I_Want, data_2010)
extracted_data_2011 = extract_data(cols_I_Want, data_2011)
extracted_data_2012 = extract_data(cols_I_Want, data_2012)

#Look at the linear regression summary
m = ols('ADM_RATE ~ TOTAL_SAT_SCORE',extracted_data_2008).fit()
print m.summary()

#See if trend changed over the years(number of schools with certain admission rates)
plt.hist(extracted_data_2008.ADM_RATE, alpha=0.9, label='2008', color = 'red')
plt.hist(extracted_data_2008.ADM_RATE, alpha=0.9, label='2009', color = 'blue')
plt.hist(extracted_data_2008.ADM_RATE, alpha=0.9, label='2010', color = 'yellow')
plt.hist(extracted_data_2008.ADM_RATE, alpha=0.9, label='2011', color = 'green')
plt.hist(extracted_data_2008.ADM_RATE, alpha=0.9, label='2012', color = 'brown')
plt.hist(Questions1.ADM_RATE, alpha=0.5, label='2013',  color = 'black')
plt.legend(loc='upper right')

#Lets look at the relationship between Retention rate vs. total SAT Scores with 2013 data
plt.scatter(Questions1.TOTAL_SAT_SCORE, Questions1.RET_FT4)

m = ols('RET_FT4 ~ TOTAL_SAT_SCORE',Questions1).fit()
print m.summary()

plt.scatter(Questions1.RET_FT4, Questions1.ADM_RATE)
m = ols('RET_FT4 ~ ADM_RATE',Questions1).fit()
print m.summary()

#Suprisingly there is so strong relationship between Retention rate and SAT scores, then relationship between Retention rate and Acceptance rate

