from flask import Flask, render_template, request, redirect, url_for
import random
from Web_data import index_html, item_input_html, dashboard_html, disposal_options_html

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Placeholder for storing user data (in-memory, for MVP purposes)
users = []
items = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    location = request.form.get('location')
    if name and email and location:
        users.append({'name': name, 'email': email, 'location': location})
    return redirect(url_for('item_input', name=name, location=location))

@app.route('/dashboard/<name>/<location>')
def dashboard(name, location):
    return render_template('dashboard.html', name=name, location=location)

@app.route('/item_input/<name>/<location>', methods=['GET', 'POST'])
def item_input(name, location):
    if request.method == 'POST':
        description = request.form.get('description')
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        condition = request.form.get('condition')
        dirty = request.form.get('dirty')
        
        photo = request.files.get('photo')
        photo_filename = None
        if photo:
            photo_filename = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_filename)
        
        items.append({
            'name': name,
            'location': location,
            'description': description,
            'category': category,
            'subcategory': subcategory,
            'condition': condition,
            'dirty': dirty,
            'photo': photo_filename
        })
        return redirect(url_for('disposal_options', location=location))
    
    categories = {
        "Plastics": ["PET", "PE", "PS", "PVC", "PP", "Plastic Films"],
        "Plastic Films": ["LDP", "HDP"]
    }
    
    return render_template('item_input.html', name=name, location=location, categories=categories)

@app.route('/disposal_options/<location>')
def disposal_options(location):
    berlin_buyers = ["BSR", "ALBA"] + [f"Buyer {i}" for i in range(1, 11)]
    athens_buyers = [f"Municipality {i}" for i in range(1, 11)] + [f"Buyer {i}" for i in range(1, 11)]
    
    buyers = berlin_buyers if location == "Berlin" else athens_buyers
    buyer_positions = {buyer: (random.uniform(52.3, 52.6), random.uniform(13.2, 13.6)) for buyer in berlin_buyers} if location == "Berlin" else {buyer: (random.uniform(37.9, 38.1), random.uniform(23.6, 23.9)) for buyer in athens_buyers}
    
    return render_template('disposal_options.html', location=location, buyers=buyers, buyer_positions=buyer_positions)


if __name__ == '__main__':
    app.run(debug=True)

# Save index.html file
with open("templates/index.html", "w") as file:
    file.write(index_html)

# Save item_input.html file
with open("templates/item_input.html", "w") as file:
    file.write(item_input_html)

# Save disposal_options.html file
with open("templates/disposal_options.html", "w") as file:
    file.write(disposal_options_html)
