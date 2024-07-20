
#importing libaries and cvs file
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pf=pd.read_csv('https://data.cityofnewyork.us/resource/csps-2ne9.csv')

pf.head()

pf.columns

pf.info()

#converting all objects data types into string
new_pf = pf.astype({col: 'string' for col in pf.select_dtypes(include='object').columns})

new_pf.info()

#testing to see if we can drop NAN or invaild values
#dropping will cut down our data by 51% (1000 --> 485)
test_new_pf= new_pf.replace(['s','na'],np.nan)
test_new_pf=new_pf.dropna()
test_new_pf.info()

#Trying to identify how many values of 's' & 'na' are in each column
values_to_find = ['s', 'na']
result = {}
for column in new_pf.columns:
    value_counts = new_pf[column].isin(values_to_find).value_counts()
    if True in value_counts:
        result[column] = value_counts[True]
print(result)

#Decide not to cut down the data
new_pf.info()

#Just replacing the 's' and 'na' as traditional 'NAN'
#Looking at unqiue values for each column
new_pf= new_pf.replace(['s','na'],np.nan)
unique_values = {}
for column in new_pf.columns:
    unique_values[column] = new_pf[column].unique()
for column, values in unique_values.items():
    print(f"Column '{column}': {values}")

#Decided to only pick these columns: 'school_dbn', 'school_level', 'regents_exam', 'year','mean_score'
part_pf= new_pf[['school_dbn', 'school_level', 'regents_exam', 'year','mean_score']]
print(part_pf['school_dbn'].unique())

#Assigning boroughs to School DBN codes
#Noticed we mainly have Manhattan but this code will cover all boroughs
def determine_borough(school_dbn):
    if 'M' in school_dbn:
         return 'Manhattan'
    elif 'K' in school_dbn:
        return 'Brooklyn'
    elif 'X' in school_dbn:
        return 'Bronx'
    elif 'Q' in school_dbn:
        return 'Queens'
    elif 'R' in school_dbn:
        return 'Staten Island'
    else:
        return 'Unknown'

part_pf['borough'] = part_pf['school_dbn'].apply(determine_borough)
part_pf.head()

#Filter out for only Manhattan data
contains_m_pf = part_pf[part_pf['borough'] == 'Manhattan']
print(contains_m_pf.head())
print(contains_m_pf['mean_score'].describe())

#General overview of Mean test scores in Manhattan by School Level
plt.figure(figsize=(12, 6))
sns.barplot(data=contains_m_pf, x='school_level', y='mean_score', palette='viridis', edgecolor='black')
plt.title('Mean Scores by School Level in Manhattan')
plt.xlabel('School Level')
plt.ylabel('Mean Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Narrowing it down to each exams in each school levels in Manhattan
plt.figure(figsize=(14, 8))
sns.barplot(data=contains_m_pf, x='regents_exam', y='mean_score', hue='school_level', palette='viridis', edgecolor='black')
plt.title('Mean Scores of Different Regents Exams by School Level in Manhattan')
plt.xlabel('Regents Exam')
plt.ylabel('Mean Score')
plt.legend(title='School Level')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Filtering for 'K-8', 'High school', 'K-12 all grades' school levels
filtered_levels_pf = contains_m_pf[contains_m_pf['school_level'].isin(['K-8', 'High school', 'K-12 all grades'])]
plt.figure(figsize=(14, 8))
sns.barplot(data=filtered_levels_pf, x='regents_exam', y='mean_score', hue='school_level', palette='viridis', edgecolor='black')
plt.title('Mean Scores of Different Regents Exams by School Level in Manhattan')
plt.xlabel('Regents Exam')
plt.ylabel('Mean Score')
plt.legend(title='School Level')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

filtered_manhattan_pf = contains_m_pf[contains_m_pf['school_level'].isin(['K-8', 'High school', 'K-12 all grades'])]
plt.figure(figsize=(14, 8))
sns.lineplot(data=filtered_manhattan_pf, x='regents_exam', y='mean_score', hue='school_level', marker='o', palette='viridis')
plt.title('Mean Scores of Different Regents Exams by School Level in Manhattan')
plt.xlabel('Regents Exam')
plt.ylabel('Mean Score')
plt.legend(title='School Level')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
