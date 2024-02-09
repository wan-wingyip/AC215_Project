"""
This Class and its methods scrapes images from Craigslist listings for fixer-upper and renovated properties.
"""


# import packages
import os
import re
import json
import requests
from bs4 import BeautifulSoup
import time


# method to get image urls
def getting_all_house_links(urls:list):  #the urls are the list of urls we want to scrape. this is based on keywords such as fixer upper or renovated
  def individual_url_getter(url):  #from the list of urls, each url is passed here. this function then gets house urls within the keyword based url.
  
    URL=url

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    }

    response = requests.get(URL, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    # Assuming your soup object is named 'soup'
    links = soup.select('li.cl-static-search-result a')

    # Extract the href attribute from each link
    urls = [link['href'] for link in links]

    return urls

  all_urls=[]   #this is where all the house urls are saved
  for idx, url in enumerate(urls):
    print(idx)
    url=url
    print(url)
    print('number of houses detected ', len(all_urls))
    all_urls.extend(individual_url_getter(url))

  all_urls=list(set(all_urls))
  print('the number of unique housings by id are', len(all_urls))
  return list(set(all_urls))


# Download images and save them in a renovated folder
def images_download(url, folder_name_here):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
    }

    # Get the folder name
    folder_name = folder_name_here+'/' + re.search(r'(\d+).html$', url).group(1)
    
    # Check if directory exists
    if os.path.exists(folder_name):
        print("Duplicate exists for ", re.search(r'(\d+).html$', url).group(1))
        return

    # If the directory doesn't exist, proceed with the scraping and downloading
    os.makedirs(folder_name)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the JavaScript array using regular expression
        script_content = soup.find('script', text=re.compile('var imgList = ')).string
        img_list_str = re.search(r'var imgList = (\[.*?\]);', script_content).group(1)

        # Parsing the extracted JSON string
        img_list = json.loads(img_list_str)

        # Getting all image URLs from the parsed JSON list
        img_urls = [img['url'] for img in img_list]

        # Download and save each image
        for idx, img_url in enumerate(img_urls, 1):
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()  # Raise an error for bad responses
            with open(f'{folder_name}/image_{idx}.jpg', 'wb') as file:
                file.write(img_response.content)
            time.sleep(0.1)  # Sleep for a short while between image downloads
        print("Images downloaded for: ", re.search(r'(\d+).html$', url).group(1))
    except requests.RequestException as e:
        print(f"Error encountered: {e}")
    except Exception as e:
        print(f"Unexpected error encountered: {e}")



# main method to scrape images


#start downloading images
def scrape(target_older: str, urls: list):
  all_urls=getting_all_house_links(urls)
  
  i=0
  for url in all_urls:

    time.sleep(1)
    images_download(url, target_older)
    i+=1
    print('images downloaded for ' + str(i) + ' houses')
