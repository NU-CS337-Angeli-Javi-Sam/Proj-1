import pandas as pd
from data_structures.Entity import Entity
import pickle as pkl

# Read datasets
df_title_principals = pd.read_csv('data/title.principals.tsv', sep='\t')
df_title_basics = pd.read_csv('data/title.basics.tsv', sep='\t')
df_name_basics = pd.read_csv('data/name.basics.tsv', sep='\t')

year = '2013'
df_title_basics_certainyear = df_title_basics[df_title_basics['startYear'] == year]

# Initialize data structure
items_for_year = {"Films": [], "People": []}

# Loop through films and add corresponding year, titles, and people
count = 0
for index, row in df_title_basics_certainyear.iterrows(): #
    #print(row)

    # Get attributes, mainly for the year
    title_id = row['tconst']
    title_name = row['originalTitle']
    title_startyear = row['startYear']
    title_endyear = row['endYear']

    #print("TITLE NAME: ", title_name)
    #print("TITLE YEAR: ", title_startyear)
    
    if title_endyear != "\\N": # TV series
        years_to_add = [i for i in range(title_startyear, title_endyear+1)]
    elif title_startyear == "\\N": # unknown
        continue
    else: # film
        years_to_add = [title_startyear]

    #print("YEARS TO ADD: ", years_to_add)

    # Get people in film/series
    df_title_people_ids = df_title_principals[df_title_principals['tconst'] == title_id]
    people_names = []

    for index_people, row_people in df_title_people_ids.iterrows():
        person_name_lst = df_name_basics[df_name_basics['nconst'] == row_people['nconst']]['primaryName'].tolist()
        people_names.append(Entity(person_name_lst[0]))
    
    #print("PEOPLE NAMES: ", people_names)

    # for each year in years_to_add, add those people and the film name
    for year in years_to_add:
        film_entity = Entity(title_name)
        items_for_year["Films"].append(film_entity)
        items_for_year["People"].extend(people_names)

        #print(year, years[year])
    print(count)
    count += 1

with open("data/"+str(year)+".pkl", 'wb') as file:
    pkl.dump(items_for_year, file)
