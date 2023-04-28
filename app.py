from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

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

# Getting information out of a particular Armor
armor_weapons = []
armor_color = []
armor_capabilities = []
armor_special_features = []
armor_composition = []


for i in range(len(armor_urls)):
    try:
        armor_page_url = armor_urls[i]
        response = requests.get(armor_page_url)
        armor_doc = BeautifulSoup(response.text, 'html.parser')
        div_information_class = 'pi-item pi-group pi-border-color'

        weapon_information = armor_doc.find('div', {'data-source': 'weapons'})
        if weapon_information:
            armor_weapons.append(weapon_information.get_text(separator='<br/>').replace('<br/>', ','))
        else:
            armor_weapons.append('No info found')

        color_information = armor_doc.find('div', {'data-source': 'armorcolor'})
        if color_information:
            armor_color.append(color_information.text.strip())
        else:
            armor_color.append('No info found')

        capabilities_information = armor_doc.find('div', {'data-source': 'capabilities'})
        if capabilities_information:
            armor_capabilities.append(
                capabilities_information.get_text(separator='<br/>').replace('<br/>', ','))
        else:
            armor_capabilities.append('No info found')

        special_features_information = armor_doc.find('div', {'data-source': 'specialfeats'})
        if special_features_information:
            armor_special_features.append(
                special_features_information.get_text(separator='<br/>').replace('<br/>', ','))
        else:
            armor_special_features.append('No info found')

        composition_information = armor_doc.find('div', {'data-source': 'composition'})
        if composition_information:
            armor_composition.append(composition_information.text.strip())
        else:
            armor_composition.append('No info found')

        

    except requests.exceptions.RequestException as e:
        print(f"Failed to get armor page data for {armor_titles[i]}: {e}")

# cutting extra characters from the list and keeping only the weapons
extract_armor_weapons_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_weapons]
extract_armor_weapons_2 = [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_weapons_1]

final_armor_weapons = extract_armor_weapons_2

# cutting extra characters from the list and keeping only the colors
final_armor_color = [string.split('\n')[1] if '\n' in string else string for string in armor_color]

# cutting extra characters from the list and keeping only the capabilities
extract_armor_capabilities_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_capabilities]
extract_armor_capabilities_2 = [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_capabilities_1]

final_armor_capabilities = extract_armor_capabilities_2

# cutting extra characters from the list and keeping only the capabilities
extract_armor_special_features_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_special_features]
extract_armor_special_features_2 =  [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_special_features_1]

final_armor_special_features = extract_armor_special_features_2

# cutting extra characters from the list and keeping only the composition
final_armor_composition = [string.split('\n')[1] if '\n' in string else string for string in armor_composition]

# main dictionary
armor_data = {}



for i in range(len(armor_titles)):
    try:
        armor_data[armor_titles[i]] = {
            'Armor_title': armor_titles[i],
            'Armor_color': final_armor_color[i],
            'Armor_composition': final_armor_composition[i],
            'Armor_weapons': final_armor_weapons[i],
            'Armor_capabilities': final_armor_capabilities[i],
            'Armor_special_features': final_armor_special_features[i],
            'Armor_image': f"static/images/image{i}.png"
        }
    except IndexError:
        print(f"Error: Could not add armor {armor_titles[i]} to dictionary")

@app.route('/')
def index():
    # pass armor data to template
    return render_template('index.html', armors=armor_data)

@app.route('/armor/<armor_name>')
def armor(armor_name):
    try:
        # retrieve armor info based on armor name
        armor_info = armor_data.get(armor_name)
        # return armor info as JSON response
        return armor_info
    except KeyError:
        return f"Error: Could not find armor {armor_name}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
