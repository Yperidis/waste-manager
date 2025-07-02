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
      <label>Category:</label>
      <select name="category" id="category">
        <option value="">Select a category</option>
        <option value="Plastics">Plastics</option>
      </select><br><br>
      
      <label>Subcategory:</label>
      <select name="subcategory" id="subcategory">
        <option value="">Select a subcategory</option>
      </select><br><br>
      
      <label>Upload a photo:</label>
      <input type="file" name="photo" id="photo" accept="image/*"><br><br>
      
      <!-- Extra fields appear only if category and subcategory are selected -->
      <div id="extraFields" class="scrollable" style="display: none;">
        <label>Is the material dirty?</label>
        <select name="dirty" id="dirty">
          <option value="">Select</option>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select><br><br>
        
        <label>Condition:</label>
        <select name="condition" id="condition">
          <option value="">Select</option>
          <option value="Perfect">Perfect</option>
          <option value="Worn">Worn</option>
          <option value="Deteriorated">Deteriorated</option>
        </select><br><br>
      </div>
      
      <!-- Submit button is always visible (when enabled) -->
      <button type="submit" id="submitBtn" disabled>Proceed</button>
    </form>
  </div>

  <script>
    // Get references to all fields.
    const photoField = document.getElementById('photo');
    const submitBtn = document.getElementById('submitBtn');    
    const categoryDropdown = document.getElementById('category');
    const subcategoryDropdown = document.getElementById('subcategory');
    const extraFields = document.getElementById('extraFields');
    const dirtyDropdown = document.getElementById('dirty');
    const conditionDropdown = document.getElementById('condition');

    // Define available subcategories.
    const categories = {
      "Plastics": ["PET", "PE", "PS", "PVC", "PP", "Plastic Films"],
      "Plastic Films": ["LDP", "HDP"]
    };

    // When a category is selected, update the subcategory options.
    categoryDropdown.addEventListener('change', function() {
      const subcategories = categories[this.value] || [];
      subcategoryDropdown.innerHTML = '<option value="">Select a subcategory</option>' +
        subcategories.map(sub => `<option value="${sub}">${sub}</option>`).join('');
      checkFormCompletion();
    });

    // When a subcategory is selected, display extra fields if chosen.
    subcategoryDropdown.addEventListener('change', function() {
      extraFields.style.display = this.value ? 'block' : 'none';
      checkFormCompletion();
    });

    // Check form completion when any relevant field changes.
    function checkFormCompletion() {
      const photoUploaded = photoField.files.length > 0;
      const categoryAndExtraSelected = 
            categoryDropdown.value !== "" &&
            subcategoryDropdown.value !== "" &&
            dirtyDropdown.value !== "" &&
            conditionDropdown.value !== "";
      
      // Enable the button if ANY one criterion is satisfied.
      if (photoUploaded || categoryAndExtraSelected) {
        submitBtn.disabled = false;
      } else {
        submitBtn.disabled = true;
      }
    }

    // Event listeners.
    photoField.addEventListener('change', checkFormCompletion);
    dirtyDropdown.addEventListener('change', checkFormCompletion);
    conditionDropdown.addEventListener('change', checkFormCompletion);
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
            <a href="/reduce_waste">How to reduce waste</a>
            <a href="/item_input/{{ name }}/{{ location }}">Responsible disposal options</a>
            <a href="/track_and_monitor/{{ location }}">Track and monitor waste</a>
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
        .buyer-card { border: 1px solid #ccc; border-radius: 10px; margin: 10px; padding: 20px; background: #f9f9f9; }
        .buyer-name { font-weight: bold; font-size: 1.2em; }
        .kpi { margin: 5px 0; }
        #map { height: 400px; width: 100%; margin-top: 20px; }
    </style>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
    <div class="container">
        <h1>Disposal Options in {{ location }}</h1>
        {% for buyer in buyers %}
        <div class="buyer-card">
            <div class="buyer-name">{{ buyer.name }}</div>
            <div class="kpi">📍 Location: ({{ buyer.lat | round(3) }}, {{ buyer.lon | round(3) }})</div>
            <div class="kpi">💶 Price: €{{ buyer.price }}</div>
            <div class="kpi">🌱 Carbon Footprint: {{ buyer.carbon }} kg CO₂</div>
        </div>
        {% endfor %}
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

# Creat the reduce_waste.html template
reduce_waste_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How to Reduce Waste</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .item { border-bottom: 1px solid #ddd; padding: 10px 0; }
        .item a { text-decoration: none; color: blue; }
    </style>
</head>
<body>
    <h1>How to Reduce Waste</h1>
    {% if results %}
      {% for result in results %}
        <div class="item">
          <a href="{{ result.link }}" target="_blank"><h2>{{ result.title }}</h2></a>
          <p>{{ result.summary }}</p>
        </div>
      {% endfor %}
    {% else %}
      <p>No results found.</p>
    {% endif %}
</body>
</html>
"""

# Creat the track_and_monitor.html template
track_and_monitor_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Track and Monitor Disposed Items - {{ location }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        .manager { border-bottom: 1px solid #ddd; padding: 15px 0; }
        .manager:last-child { border-bottom: none; }
        .kpi { margin-top: 10px; font-size: 0.95em; color: #555; }
        .score { font-weight: bold; color: #2e7d32; }
        .fail { color: #c62828; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Central Waste Managers in {{ location }}</h1>
        <p style="text-align:center; color: #666;">Here are the latest indicators from local authorities and central operators</p>

        {% for manager in managers %}
        <div class="manager">
            <h2>{{ manager.name }}</h2>
            <div class="kpi">Transparency Score: <span class="score">{{ manager.transparency }}</span></div>
            <div class="kpi">Cost per Tonne: <span class="score">€{{ manager.cost_per_tonne }}</span></div>
            <div class="kpi">Service Coverage: <span class="score">{{ manager.coverage }}%</span></div>
            <div class="kpi">Reported Incidents: 
                {% if manager.incidents == 0 %}
                    <span class="score">None</span>
                {% else %}
                    <span class="fail">{{ manager.incidents }}</span>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>

"""