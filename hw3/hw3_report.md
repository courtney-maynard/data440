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

I created a shell script to read each URI in from the text file containing all 1000 URI-Rs. Then, for each URI, a hash is created and the html is downloaded and saved in a file with that hash value as the name and both the hash value and URI are added to a hashmap file which is also saved. Even though I had already named my links numerically, I decided to do the hashing in order to get some experience with hashing. 

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

I created a python program to extract the text content from the raw HTML. Rather than iterating through the folder containing all of the raw HTML files, I decided to use the hashmap file I created to load in one file at a time, store that hash value in temporary memory, extract the content, and then save valid content to a hashvalue named file of the processed content. Thus, each URI ended up with a unique hash value named raw and processed file. Throughout creation of this program, many errors were thrown as I tested extracting the content. I created try and except blocks to account for the HTMLExtractionErrors and UnicodeDecodeErrors that I was receiving. Additionally, I ensured I only saved content to a file if there was actually content to be found and not just an empty output that would result in a OB file. After this process was completed, I ended up with 733 content-containing processed files.

*How many of your 1000 URIs produced useful text? If that number was less than 1000, did that surprise you?*
733 URIs ended up producing content containing text; there were several URIs that had no content, as well as others that flagged errors such as HTMLExtractionErrors and UnicodeDecodeErrors. This did not surprise me, as I didn't expect all of the webpages to have extractable content. Some of the links were to registration sites or may have been primarily audio or visual, though I filtered for those initially, so they didn't have any pure textual content.

---

## Q2: Rank with TF-IDF
Word: Career

Total Number of Documents with 'Career': 58
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -irm 1 career . | wc -l 
      58
```

[URI One](https://www.keepingtheNHShonest.co.uk/) Law/Healthcare
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 0d9e10232a60b86214399cc6525aacd9_processed.txt | wc -l 
       3
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 0d9e10232a60b86214399cc6525aacd9_processed.txt                  
     5254 0d9e10232a60b86214399cc6525aacd9_processed.txt
```

[URI Two](https://www.hayfestival.com/m-210-dallas-2024.aspx?skinid=23&localesetting=en-GB&currencysetting=USD&hpcurr=USD&pagenum=1&resetfilters=true) Local Events
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career f9c01a6c638506fb47ffd64f6ffa2098_processed.txt | wc -l 
       3
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w f9c01a6c638506fb47ffd64f6ffa2098_processed.txt                  
    5846 f9c01a6c638506fb47ffd64f6ffa2098_processed.txt
```

[URI Three](https://www.espn.com/nfl/story/_/id/40919095/60k-club-passing-yards-quarterback-nfl-history?utm_source=dlvr.it&utm_medium=twitter) Football
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career e28a6d6f7cb98e0f060f260fd0baf539_processed.txt | wc -l
       12
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w e28a6d6f7cb98e0f060f260fd0baf539_processed.txt
     2269 e28a6d6f7cb98e0f060f260fd0baf539_processed.txt
```

[URI Four](https://datascience.virginia.edu/news/msds-alumni-profile-levi-davis) Professional Profile
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 0e075e65a4c6e053b0c587b328abac1e_processed.txt | wc -l
       7
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 0e075e65a4c6e053b0c587b328abac1e_processed.txt
     665 0e075e65a4c6e053b0c587b328abac1e_processed.txt
```

[URI Five](https://www.simplek12.com/?utm_content=310685313&utm_medium=social&utm_source=twitter&hss_channel=tw-133020661) Professional Development
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 3d3e6d46db1f8d172cc39d83f862d8f7_processed.txt | wc -l
       3
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 3d3e6d46db1f8d172cc39d83f862d8f7_processed.txt
     806 3d3e6d46db1f8d172cc39d83f862d8f7_processed.txt
```

[URI Six](https://www.marketingaiinstitute.com/blog/the-ai-show-episode-117?utm_campaign=MAII%3A%20Social%20Media&utm_content=310156390&utm_medium=social&utm_source=twitter&hss_channel=tw-769616948522946560) Artificial Intelligence
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 9c212d8fdab9b0e8424ac8d4206c6792_processed.txt | wc -l
      1
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 9c212d8fdab9b0e8424ac8d4206c6792_processed.txt
    14785 9c212d8fdab9b0e8424ac8d4206c6792_processed.txt
```

[URI Seven](https://thectoclub.com/news/best-data-science-newsletters/?ref=quuu) Newsletter Subscription
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 31db92ba00a9f27666ab0c25cce615a5_processed.txt | wc -l
      3
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 31db92ba00a9f27666ab0c25cce615a5_processed.txt
    1671 31db92ba00a9f27666ab0c25cce615a5_processed.txt
```

[URI Eight](https://nhwc.janeapp.com:443/) Physiotherapy
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 46ead043438570846d1ffca685190b4b_processed.txt | wc -l
      3
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 46ead043438570846d1ffca685190b4b_processed.txt
    4965 46ead043438570846d1ffca685190b4b_processed.txt
```

[URI Nine](https://the-avidreader.blogspot.com/2024/10/Off-Edge-10-02-24-BT-RABT.html) Literature
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 4626a35ef45488212d4c5acede3b0f99_processed.txt | wc -l
      2
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 4626a35ef45488212d4c5acede3b0f99_processed.txt
    956 4626a35ef45488212d4c5acede3b0f99_processed.txt
```

[URI Ten](https://ellenor.org/news/angela/) Work Commemoration
```console
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % grep -o -i career 8376c58e4bbbc685f5e2271fd489caca_processed.txt | wc -l
      8
(base) courtneymaynard@Courtneys-MacBook-Pro-2 processed_html_files % wc -w 8376c58e4bbbc685f5e2271fd489caca_processed.txt
    1350 8376c58e4bbbc685f5e2271fd489caca_processed.txt
```
**Table 1. Indicating the TF, IDF, and TF-IDF Values For Each Link, Ranked by TF-IDF**

|TF-IDF |TF |IDF  |URI
|------:|--:|---:|---
|0.0196|0.011|1.78|https://datascience.virginia.edu/news/msds-alumni-profile-levi-davis
|0.011|0.0059|1.78|https://ellenor.org/news/angela/
|0.0094|0.0053|1.78|https://www.espn.com/nfl/story/_/id/40919095/60k-club-passing-yards-quarterback-nfl-history?utm_source=dlvr.it&utm_medium=twitter
|0.0066|0.0037|1.78|https://www.simplek12.com/?utm_content=310685313&utm_medium=social&utm_source=twitter&hss_channel=tw-133020661
|0.0037|0.0021|1.78|https://the-avidreader.blogspot.com/2024/10/Off-Edge-10-02-24-BT-RABT.html
|0.0032|0.0018|1.78|https://thectoclub.com/news/best-data-science-newsletters/?ref=quuu
|0.0011|0.0006|1.78|https://nhwc.janeapp.com:443/
|0.0010|0.00057|1.78|https://www.keepingtheNHShonest.co.uk/
|0.00091|0.00051|1.78|https://www.hayfestival.com/m-210-dallas-2024.aspx?skinid=23&localesetting=en-GB&currencysetting=USD&hpcurr=USD&pagenum=1&resetfilters=true
|0.000012|0.0000068|1.78|https://www.marketingaiinstitute.com/blog/the-ai-show-episode-117?utm_campaign=MAII%3A%20Social%20Media&utm_content=310156390&utm_medium=social&utm_source=twitter&hss_channel=tw-769616948522946560

