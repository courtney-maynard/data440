# IMPORTS
import json
import gzip
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

'''
group_memento_counts()
    input: none
    output: text file of grouped counts of mementos, i.e. how many URI-Rs have each number of mementos
    - sorts the counts of mementos and groups them, then saves to an output file
'''
def group_memento_counts(): 
    with open('memento_counts.txt', 'r') as file:
        counts = [int(line.strip()) for line in file]

    # sort the counts
    sorted_counts = sorted(counts)
    counts_groups = {}

    for count in sorted_counts:
        if count in counts_groups:
            counts_groups[count] += 1
        else:
            counts_groups[count] = 1

    # save in a file where i can manually read and bin them
    with open('memento_grouped_counts.txt', 'w') as output_file:
        for count, total in counts_groups.items():
            output_file.write(f'{count} --> {total}\n')

'''
get_first_memento_date()
    input: json file of the timemap for the URI-R
    output: the oldest datetime occurence for that URI-R
    - opens the zipped json files and retrieves the oldest datetime
    - when the json is empty/doesn't contain and datetime information, it catches the decode error
    and outputs that there are no mementos
    - keeps track of even those URI-Rs with no mementos so that the ordering of URI-Rs is maintained
'''
def get_first_memento_date(json_file):
    try:
        with gzip.open(json_file, 'rt', encoding='utf-8') as f:
            data = json.load(f)
        
        # ensure that there are mementos, handle cases where there are no mementos
        if 'mementos' in data and 'first' in data['mementos']:
            oldest_datetime = data['mementos']['first']['datetime']
            return oldest_datetime
        else:
            return None
    except json.JSONDecodeError: #handle cases where there are no mementos
        print('No Mementos.')
        return None
    
'''
save_age_and_number()
    input: none
    output: csv file of the URI-R index, age of oldest memento, and number of mementos for each URI-R,
    - finds the corresponding json.gz timemap file for each URI-R
    - utilizes the get_first_memento_date() function to retrieve the oldest datetime
    - calculate the age in days, if there are no mementos i.e. no oldest datetime, age is saved as zero
    - collect all results and save as csv
'''
def save_age_and_number():
    with open('memento_counts.txt', 'r') as file:
        memento_counts = [int(line.strip()) for line in file.readlines()]

    age_and_num_results = [] # store data we are about to retrieve

    # for each URI-R/link
    for each_link in range(len(memento_counts)):
        json_file = f'timemap_files_hw2/link_{each_link + 1}.json.gz' 
        
        first_datetime = get_first_memento_date(json_file)
        
        # calculate age in days, account for case of no mementos i.e. zero days
        if first_datetime:
            first_date = datetime.fromisoformat(first_datetime[:-1])
            age_days = (datetime.utcnow() - first_date).days
        else:
            age_days = 0

        num_mementos = memento_counts[each_link]
        
        # append results to the list
        age_and_num_results.append({'age_days': age_days, 'num_mementos': num_mementos})

    # save to dataframe and download as csv 
    age_and_num_df = pd.DataFrame(age_and_num_results)
    age_and_num_df.to_csv('memento_age_and_number.csv', index=True)


# RUNNING ANALYSIS FUNCTIONS
group_memento_counts()
save_age_and_number()


# CREATING ANALYSIS PLOT
num_age_analysis_df = pd.read_csv('memento_age_and_number.csv')
age_greater_zero = num_age_analysis_df[num_age_analysis_df['num_mementos'] > 0]
#print(len(age_greater_zero)) # this value should be 1046-431 = 615 ---- it is!

# make colors for bin categories!
age_greater_zero['memento_category'] = pd.cut(age_greater_zero['num_mementos'],
    bins=[1, 5, 10, 50, 100, 1000, 10000, 100000, float('inf')],
    labels=['1-5', '6-10', '11-50', '51-100', '101-1000', '1001-10000', '10001-100000', '100000+'])


plt.figure(figsize=(10, 6))
sns.scatterplot(data=age_greater_zero, x='age_days', y='num_mementos', hue='memento_category', palette = 'flare', alpha=0.6)

plt.title('URI-R Age vs. Number of Mementos')
plt.xlabel('Age in Days')
plt.ylabel('Number of Mementos')

plt.grid()
plt.legend(title='Grouped Number of Mementos')
plt.tight_layout()

# save figure and show 
plt.savefig('age_vs_num_mementos.png')
plt.show()