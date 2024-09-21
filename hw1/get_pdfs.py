#IMPORTS
import sys
import requests
import re

from bs4 import BeautifulSoup

#FUNCTIONS

'''
getHTMLContent(captured_uri)
    input: captured_uri - string uri link passed into program via command line
    output: text representation of all the html content at the requested link
'''
def getHTMLContent(captured_uri):
    html_content = requests.get(captured_uri)
    return html_content.text
    
'''
create_soup(html_of_page)
    input: text of html of the requested page
    output: beautiful soup object to parse
'''
def create_soup(html_of_page):
    try:
        soup = BeautifulSoup(html_of_page, 'html.parser')
        return soup
    except:
        print('Error creating soup object.')
    

'''
action_on_links(each_link)
    input: content found within all of the A tags on a page

    - gets the link itself, requests the next uri
    - determines if the link references a PDF file and if it does, print the required information
    - if the link does not reference a PDF, nothing is printed 

    output: does not return any objects
'''
def action_on_links(each_link):
    # get the link itself from the whole tag+link representation
    actual_link = each_link.get('href')

    # request the NEXT uri 
    next_uri = requests.get(actual_link)

    # use the Content-Type HTTP response header to determine if the link references a PDF file
    content_type_link = next_uri.headers.get('Content-Type', '')

    # check if it references a pdf
    if 'application/pdf' in content_type_link:
        #print the original URI (found in the parent HTML page)
        print('URI: ', actual_link)

        #print the final URI (after any redirects)
        print('Final URI: ', next_uri.url)

        #print the number of bytes in the PDF file
        num_bytes = next_uri.headers.get('Content-Length')
        print('Content Length:', num_bytes, 'bytes \n')

    return


#BEGINNING OF RUNNING PROGRAM
captured_uri = sys.argv[1]

#PART ONE: SET UP FOR PARSING
html_of_page = getHTMLContent(captured_uri) # get the html content of the page
soup = create_soup(html_of_page) # create soup object

#PART TWO: EXTRACT LINKS AND PERFORM REQUIRED ACTIONS
all_links = soup.find_all('a', href=True) # for some tested pages, there was no href inside the A tag

for each_link in all_links:
    # need to make sure the link is valid, 
    # some websites have internal not external links inside A tag, or other content that isn't a URI
    if each_link.get('href').startswith('http'):
        #print('Link:', each_link.get('href'))
        action_on_links(each_link)
    #else:
        #print('LINK NOT VALID: ', each_link)
    

