from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os
import urllib.request


# define armor data
try:
    armors_url = "https://ironman.fandom.com/wiki/Category:Armors"
    response = requests.get(armors_url)
    page_contents = response.text
    doc = BeautifulSoup(page_contents, 'html.parser')

    li_tags = doc.find_all('li', {'class': 'category-page__member'})

    armor_titles = []
    for i in range(32, 82):
        div_tag = li_tags[i].find('div')
        if div_tag and div_tag.a and div_tag.a.get('title'):
            armor_titles.append(div_tag.a.get('title'))
        elif li_tags[i].a and li_tags[i].a.get('title'):
            armor_titles.append(li_tags[i].a.get('title'))

    # finidng all hrefs of a tags
    armor_urls = []
    for i in range(32, 82):
        armor_urls.append("https://ironman.fandom.com" + li_tags[i].a.get('href'))
except requests.exceptions.RequestException as e:
    print(f"Failed to get armor data: {e}")
    armor_titles = []
    armor_urls = []

armor_image = []

for i in range(len(armor_urls)):
    armor_page_url = armor_urls[i]
    response = requests.get(armor_page_url)
    armor_doc = BeautifulSoup(response.text, 'html.parser')
    image_information = armor_doc.find('figure', {'data-source': 'image'})
    if image_information:
        armor_image.append(image_information.a['href'])
    else:
        armor_image.append(
            'https://static.wikia.nocookie.net/ironman/images/7/79/628678-iron_man_2020_revamped.jpg/revision/latest?cb=20191120034538')


#creating an image folder
image_src=[]
# iterate through the image URLs and download the images
try:
    #creating an image folder
    save_dir =  ("static/images")

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i, image_url in enumerate(armor_image):
        save_path = os.path.join(save_dir, f"image{i}.png")
        urllib.request.urlretrieve(image_url, save_path)
        print(f"Downloaded image{i}.png")
except Exception as e:
    print('There were some error in image section!',e)



