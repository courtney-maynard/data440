# HW0 - Getting Started with Assignment reports and Linux command-line utilities
### Courtney Maynard
### DATA 440, Fall 2024
### September 10th, 2024


# Part One
# Q3

*Upload an image to your GitHub repo and include it in place of the "Growth of the Early Web" image. Make sure to change the description of the image in the report, too.*

## Answer

The image below shows me doing one of my favorite activities - hiking - in Acadia National Park.

<img src="IMG_2057.png" width="200">

## Discussion
In order to arrive at the image above, I downloaded an image from my phone to computer and uploaded it into the correct hw0 directory. Following the example template, I chose an applicable name for the image and pasted the local path to the image. After committing the changes, I realized that the image was too big so I used an online page called Github Gist for an example of how to resize the image. This required me to change the code for uploading an image to use typical HTML syntax of img src="link to image". 

# Q4
*Replace the code in the fenced code block with any other block of code. You can use some Python code, or you can insert code from a different language -- just change the language indicated so that syntax highlighting still works properly.*

## Answer

This code is tokenizing song lyrics, line by line, and is part of the preliminary testing of different tokenization methodologies for my honors thesis. 

```
# must split lyrics into lines, in order to retain the line-level information.
def lyrics_into_lines(lyrics):
    return lyrics.split('\n')

df_balanced['Lyrics_Lines'] = df_balanced['Lyrics'].apply(lyrics_into_lines)

# tokenize each line individually in order to respect the structure of the song.

def tokenize_line(line):
    line = re.sub(r'[^a-zA-Z0-9\s]', '', line.lower())
    tokens = word_tokenize(line)
    return tokens

def tokenize_lyrics(lines):
    return [tokenize_line(line) for line in lines]

df_balanced['Tokenized_Lyrics'] = df_balanced['Lyrics_Lines'].apply(tokenize_lyrics)
```

## Discussion
I arrived at the code block above by following the template for including python code in a markdown file. An implication of this exercise is knowing how to format python code so that it is readable and clear that it is code and not just text. 

# Q5 
*Edit the first table so that it matches the first 4 weeks of our class schedule, as given in our syllabus*

## Answer

The table shows the first four weeks of the Data 440 Web Science class schedule.

|Week|Lecture Dates|Topic|Homework (Data assigned -- Due Date)
|:---|:---|:---|:---|
|01|Aug 29 & Sep 3|[Introduction to Web Science and Web Architecture](https://docs.google.com/presentation/d/1sSNcXMBUJWb-rVbTEvKqFAC2SvJugI8m/)| [HW0](https://github.com/anwala/teaching-web-science/tree/main/fall-2024/homework/hw0) - Getting Started, Aug 29 -- Sep 10|
|02|Sep 5 & 10|[Introduction to Python](https://docs.google.com/presentation/d/1_TcgFerDRT0dZVX98-jMIJBMmV4_IAQg/)|[Python Google Colab notebook](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-2/data_440_03_f22_mod_02_python.ipynb)<br/>[Python lab exercises](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-2/data_440_03_f22_mod_02_lab.ipynb)<br/>[HW1](https://github.com/anwala/teaching-web-science/tree/main/fall-2024/homework/hw1) - Web Sci. Intro, Sep 10 -- 24|
|03|Sep 12 & 17|[Introduction to Info Vis with R, Python](https://docs.google.com/presentation/d/1pSywHD9i3aVNsWNxtcUfT1E2tP4mgcQv/)<br/>[Web Scraping](https://docs.google.com/presentation/d/1vtT9dleNJlUbc3ny14gotGX1Md1dEWhVHYWTz0MMdRk/edit?usp=sharing)|[InfoVis in R Colab Notebook](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-3/data_440_03_f22_mod_03_info_vis_r.ipynb)<br/>[InfoVis in Python Colab Notebook](https://github.com/anwala/teaching-web-science/blob/main/fall-2022/week-3/data_440_03_f22_mod_03_info_vis_python.ipynb)<br/>[Web Scraping (IMDB) Python Colab notebook](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/week-3/data_440_02_f23_mod_03_web_scraping_imdb.ipynb)<br/>[Web Scraping (Twitter) Python scripts](https://github.com/anwala/teaching-web-science/blob/main/fall-2023/week-3/twitter-scraper/)|
|04|Sep 19 & 24|[Measuring the Web](https://docs.google.com/presentation/d/1R7CKhxlAv_nQtt_xb1HQotqgSxcVDz58/)| |

## Discussion

I used the syllabus markdown file as a reference for creating this table. Looking at the raw code for the file allowed me to see how to code line breaks to put the homework topics in the correct stacked order. Additionally, I was able to reference how to include links to other files or markdown pages to create the links in this table as well. I included all global links instead of local links, as I didn't create copies in my folder of the homework assignments.


# References

* Github Gist - Markdown - Resize pictures in GitHub, including in comments comment, <https://gist.github.com/MichaelPolla/a65ac84286ab523603e64549f9850223>
* Scribbr - Poisson Distributions | Definition, Formula & Examples, <https://www.scribbr.com/statistics/poisson-distribution/>
* Computer Science Wiki - Graph theory and connectivity of the web,<https://computersciencewiki.org/index.php/Graph_theory_and_connectivity_of_the_web>


# Part Two
# Q1
*Create a directory (name it whatever you wish, e.g., data440 (or data691). Change the permissions on this directory so that you are the only user who can read, write, or execute. Take a screenshot of (or copy/paste) the command and its output into your report.*

## Answer
![question one answer](/hw0/partTwoScreenshots/hw0-q1screenshot.png)
## Discussion

I have some previous Linux experience, so I remembered that mkdir creates a directory and that chmod allows you to modify the permissions of the dictionary. chmod 700 gives full read, write, and execute permissions to the owner, but gives no permissions to the group that the owner may belong to or any others. Thus, by using 700, I was able to set read, write, and execute privileges for myself only.


# Q2
*For each of the commands below, do the following: Execute the command, Take a screenshot of (or copy/paste) the command and its output into your report, and Write a sentence that describes what the command did*

## wc -l test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-1.png)
Discussion: This command prints the number of lines in a file.

## echo "CS 800" >> test.txt; cat test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-2.png)
Discussion: This command appends ‘CS 800’ to the file, and then outputs the contents of the changed file.

## grep CS test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-3.png)
Discussion: The grep command, which stands for ‘Global Regular Expression Print’, searches for lines containing the phrase ‘CS’ and prints them.

## grep -c CS test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-4.png)
Discussion: This command prints the number of lines that contain the expression ‘CS’.

## sort test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-5.png)
Discussion: This command sorts the contents of the file line by line,  alphabetically and lexicographically by looking at each value in the numbers from left to right, which explains why MATH 212 appears before MATH 32, even though 32 is a smaller number.

## sort -k2 test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-6.png)
Discussion: This command sorts the lines in the file according to the second ‘field’ of information, which in this case is the second portion of the string, the numbers associated with the courses.

## sort -k2 -n test.txt
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-7.png)
Discussion: This command uses numerical sort to sort the lines according to the second ‘field’ of information (the course numbers), which then results in MATH 32 being placed before MATH 212, as 32 is a smaller number than 212.

## sort test.txt | uniq -c
Answer:
![question two answer](/hw0/partTwoScreenshots/hw0-q2-8.png)
Discussion: This command first sorts the file alphabetically/lexicographically, and then counts the number of unique lines that occur, output the number of times the line occurs followed by the actual content of the line.
