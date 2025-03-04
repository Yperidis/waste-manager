

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