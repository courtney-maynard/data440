import pandas as pd

age_num_df = pd.read_csv('memento_age_and_number.csv')

counts = []
for age in range(1, 7):
    counts.append(len(age_num_df[age_num_df['age_days'] == age]))

print(counts)
print('the number of URI-Rs less than a week old: ', sum(counts))