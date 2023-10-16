# actors
# directors
# producers
# composers
# film names
# 


import pandas as pd

# Read the dataset
df = pd.read_csv('data/data.tsv', sep='\t')

# Extract actor names
actor_names = df[df['primaryProfession'].str.contains('actor', na=False)]['primaryName']

# Print actor names
for name in actor_names:
    print(name)
