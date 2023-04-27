from flask import Flask, render_template

app = Flask(__name__)

# define armor data
armor_data = {
    'Mark I': {
        'image': 'https://www.sideshow.com/storage/product-images/903253/mark-i-mark-i-prototype-iron-man_thumbnail.jpg',
        'weapons': 'Flamethrower, missiles, machine guns',
        'os': 'None',
        'color': 'Silver',
        'capabilities': 'Flight, superhuman strength, bulletproof',
        'special_features': 'None'
    }
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