<h1 align = "center">HW 3 - Ranking Webpages</h1>

<h3 align = "center">Courtney Maynard</h3>
<h3 align = "center">DATA 440, Fall 2024</h3>
<h3 align = "center">October 17th, 2024</h3>

## Q1: Data Collection

### Part One: Download Raw HTML With Hash Named File

```shell
#!/bin/bash

uris_file="1000_uris_hw3.txt"
hashmap_file="hashmaps_hw3.txt"

# delete existing hashmaps file
> "$hashmap_file"

# read in each URI from the 1000
while IFS= read -r each_uri; do
    
    # create the hash
    hash_val=$(echo -n "$each_uri" | md5 | awk '{print $1}')
    
    # download html and save in a file with the hash value as its name
    curl "$each_uri" > "raw_html_files/${hash_val}.html"
    
    # save add to hash mapping file
    echo "$hash_val $each_uri" >> "$hashmap_file"
    
done < "$uris_file"

```
### Commentary:



### Part Two: Extract Text Content
```python
from boilerpy3 import extractors
from boilerpy3.exceptions import HTMLExtractionError # one error i got

import sys
# suppressing the error traceback content because 
# it was cluttering up command line output, making it harder to see which files 
# were empty, having errors, etc.
sys.tracebacklimit = 0 

extractor = extractors.DefaultExtractor()

# want to gather content from all of the files
# using their hash from hashmaps_hw3.txt rather than
# iterating through the folder
with open('hashmaps_hw3.txt', 'r') as hashmap_file:
    hash_pairs = hashmap_file.read().splitlines()

count_download = 1
total_valid = 0
for each_pair in hash_pairs:

    # using the hash value to load in the file, then that hash is stored 
    # in temp memory and i can use it to save the processed file
    hash_name, url = each_pair.split(' ', 1)
    
    # for each file, extract the content
    html_file = f'raw_html_files/{hash_name}.html'
    
    try:
        content = extractor.get_content_from_file(html_file)  
    except HTMLExtractionError:
        print('an HTMLExtractionError has occurred in file ', count_download, ', excluding.')   
    except UnicodeDecodeError:
        print('an UnicodeDecodeError has occurred in file ', count_download, ', excluding.')
    else:
        # if there is text content, provided no error has occurred
        if content.strip():
            # save the content to a new file, called {hash_name}_processed.txt
            processed_file = f'processed_html_files/{hash_name}_processed.txt'
            
            with open(processed_file, 'w', encoding='utf-8') as output_file:
                output_file.write(content)

            total_valid+=1
            print('processed ', count_download)
        else:
            print('no content found in file ', count_download, ', excluding.')
    
    count_download+=1

print('The number of html containing files is: ', total_valid)

```
### Commentary
---

## Q2: Rank with TF-IDF
