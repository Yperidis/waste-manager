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

# Create the index.html template
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Waste Management</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        input, select { padding: 10px; margin: 10px; width: 80%; }
        button { padding: 10px 20px; background-color: green; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Smart Waste Management</h1>
        <p>Reduce, reuse, and track your waste with transparency.</p>
        <form action="/signup" method="post">
            <input type="text" name="name" placeholder="Enter your name" required>
            <input type="email" name="email" placeholder="Enter your email" required>
            <select name="location" required>
                <option value="Berlin">Berlin, Germany</option>
                <option value="Athens">Athens, Greece</option>
            </select>
            <button type="submit">Sign Up</button>
        </form>
    </div>
</body>
</html>
"""

# Save index.html file
with open("templates/index.html", "w") as file:
    file.write(index_html)


# Create the item_input.html template
item_input_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Item Input</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        .scrollable { max-height: 400px; overflow-y: auto; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Describe Your Item</h1>
        <form method="POST" enctype="multipart/form-data">
            <label>Description:</label>
            <input type="text" name="description" required><br><br>
            
            <label>Category:</label>
            <select name="category" id="category" required>
                <option value="">Select a category</option>
                <option value="Plastics">Plastics</option>
            </select><br><br>
            
            <label>Subcategory:</label>
            <select name="subcategory" id="subcategory" required>
                <option value="">Select a subcategory</option>
            </select><br><br>
            
            <label>Upload a photo:</label>
            <input type="file" name="photo" accept="image/*"><br><br>
            
            <div id="extraFields" class="scrollable" style="display: none;">
                <label>Is the material dirty?</label>
                <select name="dirty" required>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                </select><br><br>
                
                <label>Condition:</label>
                <select name="condition" required>
                    <option value="Perfect">Perfect</option>
                    <option value="Worn">Worn</option>
                    <option value="Deteriorated">Deteriorated</option>
                </select><br><br>
                
                <button type="submit" id="submitBtn" disabled>Proceed</button>
            </div>
        </form>
    </div>

    <script>
        const descriptionField = document.getElementById('description');
        const photoField = document.getElementById('photo');
        const submitBtn = document.getElementById('submitBtn');    
        const categoryDropdown = document.getElementById('category');
        const subcategoryDropdown = document.getElementById('subcategory');
        const extraFields = document.getElementById('extraFields');
        
        const categories = {
            "Plastics": ["PET", "PE", "PS", "PVC", "PP", "Plastic Films"],
            "Plastic Films": ["LDP", "HDP"]
        };

        categoryDropdown.addEventListener('change', function() {
            const subcategories = categories[this.value] || [];
            subcategoryDropdown.innerHTML = '<option value="">Select a subcategory</option>' +
                subcategories.map(sub => `<option value="${sub}">${sub}</option>`).join('');
        });

        subcategoryDropdown.addEventListener('change', function() {
            if (this.value) {
                extraFields.style.display = 'block';
            }
        });

    function checkFormCompletion() {
        if (descriptionField.value.trim() !== "" || photoField.files.length > 0) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    descriptionField.addEventListener('input', checkFormCompletion);
    photoField.addEventListener('change', checkFormCompletion);
    </script>
</body>
</html>
"""

# Save item_input.html file
with open("templates/item_input.html", "w") as file:
    file.write(item_input_html)



# Create the dashboard.html template
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .container { max-width: 600px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        .options a { display: block; margin: 10px 0; text-decoration: none; color: blue; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome, {{ name }}!</h1>
        <p>What do you want to handle?</p>
        <div class="options">
            <a href="#">Guidance on reuse</a>
            <a href="#">How to reduce waste</a>
            <a href="/disposal_options/{{ location }}">Responsible disposal options</a>
        </div>
    </div>
</body>
</html>
"""

# Save dashboard.html file
with open("templates/dashboard.html", "w") as file:
    file.write(dashboard_html)

# Create the disposal_options.html template
disposal_options_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disposal Options</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
        .container { max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        .buyers-list { list-style: none; padding: 0; }
        .buyers-list li { margin: 10px 0; }
        #map { height: 400px; width: 100%; margin-top: 20px; }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
    <div class="container">
        <h1>Disposal Options in {{ location }}</h1>
        <ul class="buyers-list">
            {% for buyer in buyers %}
                <li>{{ buyer }}</li>
            {% endfor %}
        </ul>
        <div id="map"></div>
    </div>
    <script>
        function initMap() {
            var map = L.map('map').setView([52.52, 13.405], 12); // Default to Berlin
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
            
            var buyerPositions = {{ buyer_positions|tojson }};
            Object.keys(buyerPositions).forEach(function(buyer) {
                var position = [buyerPositions[buyer][0], buyerPositions[buyer][1]];
                L.marker(position).addTo(map)
                    .bindPopup(buyer)
                    .openPopup();
            });
        }
        window.onload = initMap;
    </script>
</body>
</html>
"""

# Save disposal_options.html file
with open("templates/disposal_options.html", "w") as file:
    file.write(disposal_options_html)
