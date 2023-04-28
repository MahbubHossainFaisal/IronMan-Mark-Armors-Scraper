from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)


# define armor data
armors_url = "https://ironman.fandom.com/wiki/Category:Armors"

response = requests.get(armors_url)
page_contents = response.text
doc = BeautifulSoup(page_contents,'html.parser')

li_tags = doc.find_all('li',{'class': 'category-page__member'})

armor_titles = []
for i in range(32,82):
    div_tag = li_tags[i].find('div')
    if div_tag and div_tag.a and div_tag.a.get('title'):
        armor_titles.append(div_tag.a.get('title'))
    elif li_tags[i].a and li_tags[i].a.get('title'):
        armor_titles.append(li_tags[i].a.get('title'))


# finidng all hrefs of a tags
armor_urls = []
for i in range(32,82):
    armor_urls.append("https://ironman.fandom.com"+li_tags[i].a.get('href'))
    




#Getting information out of a particular Armor
armor_weapons = []
armor_color = []
armor_capabilities = []
armor_special_features = []
armor_composition = []
armor_image = []
for i in range(len(armor_urls)):
    armor_page_url = armor_urls[i]
    response = requests.get(armor_page_url)
    armor_doc = BeautifulSoup(response.text,'html.parser')
    div_information_class = 'pi-item pi-group pi-border-color'
    #armor_information = armor_doc.find_all('section',{'class': div_information_class})
    weapon_information = armor_doc.find('div', {'data-source' : 'weapons' })
    color_information = armor_doc.find('div',{'data-source': 'armorcolor'})
    capabilities_information = armor_doc.find('div', {'data-source' : 'capabilities' })
    special_features_information = armor_doc.find('div', {'data-source' : 'specialfeats' })
    composition_information = armor_doc.find('div', {'data-source' : 'composition' })
    image_information = armor_doc.find('figure', {'data-source': 'image'})
    
    
    if weapon_information:
        armor_weapons.append(weapon_information.get_text(separator='<br/>').replace('<br/>',','))
    else:
        armor_weapons.append('No info found')
        
        
    if color_information:
        armor_color.append(color_information.text.strip())
    else:
        armor_color.append('No info found')
        
    if capabilities_information:
        armor_capabilities.append(capabilities_information.get_text(separator='<br/>').replace('<br/>',','))
    else:
        armor_capabilities.append('No info found')
        
    if special_features_information:
        armor_special_features.append(special_features_information.get_text(separator='<br/>').replace('<br/>',','))
    else:
        armor_special_features.append('No info found')
        
        
    if composition_information:
        armor_composition.append(composition_information.text.strip())
    else:
        armor_composition.append('No info found')
        
    if image_information:
        armor_image.append(image_information.a['href'])
    else:
        armor_image.append('https://static.wikia.nocookie.net/ironman/images/7/79/628678-iron_man_2020_revamped.jpg/revision/latest?cb=20191120034538')


#cutting extra characters from the list and keeping only the weapons
extract_armor_weapons_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_weapons]
extract_armor_weapons_2 = [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_weapons_1]

final_armor_weapons = extract_armor_weapons_2

# cutting extra characters from the list and keeping only the colors
final_armor_color = [string.split('\n')[1] if '\n' in string else string for string in armor_color]



# cutting extra characters from the list and keeping only the capabilities
extract_armor_capabilities_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_capabilities]
extract_armor_capabilities_2 = [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_capabilities_1]

final_armor_capabilities =extract_armor_capabilities_2


#cutting extra characters from the list and keeping only the capabilities
extract_armor_special_features_1 = [string.split('\n,')[2] if '\n' in string else string for string in armor_special_features]

extract_armor_special_features_2 =  [string.split(',\n')[0] if '\n' in string else string for string in extract_armor_special_features_1]

final_armor_special_features = extract_armor_special_features_2

# Composition

final_armor_composition = [string.split('\n')[1] if '\n' in string else string for string in armor_composition]

print(final_armor_composition)


# main dictionary
armor_data = {}

for i in range(len(armor_titles)):
    armor_data[armor_titles[i]] = {
        'Armor_title': armor_titles[i],
        'Armor_color': final_armor_color[i],
        'Armor_composition': final_armor_composition[i],
        'Armor_weapons': final_armor_weapons[i],
        'Armor_capabilities': final_armor_capabilities[i],
        'Armor_special_features': final_armor_special_features[i],
        'Armor_image': armor_image[i]
    }




@app.route('/')
def index():
    # pass armor data to template
    return render_template('index.html', armors=armor_data)

@app.route('/armor/<armor_name>')
def armor(armor_name):
    # retrieve armor info based on armor name
    armor_info = armor_data.get(armor_name)
    # return armor info as JSON response
    return armor_info

if __name__ == "__main__":
    app.run(host="0.0.0.0")