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
        <option value="Plastic Films">Plastic Films</option>
        <option value="Textiles">Textiles</option>
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
      "Plastic Films": ["LDP", "HDP"],
      "Textiles": ["H&M"]
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
            <a href="/reuse_waste">Guidance on reuse</a>
            <a href="/reduce_waste">How to reduce waste</a>
            <a href="/item_input/{{ name }}/{{ location }}">Responsible disposal options</a>
            <a href="/track_and_monitor/{{ location }}">Track and Monitor Waste</a>
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
        <div id="map"></div>
    </div>
<script>
    function initMap() {
        var map = L.map('map').setView([52.52, 13.405], 12); // Default to Berlin
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        var buyerPositions = {{ buyer_positions | tojson }};
        
        Object.keys(buyerPositions).forEach(function(buyer) {
            var data = buyerPositions[buyer];
            var position = [data.lat, data.lon];
            var popupContent = `
                <strong>${buyer}</strong><br>
                💶 Price: €${data.price}<br>
                🌱 Carbon: ${data.carbon} kg CO₂
            `;

            L.marker(position)
            .addTo(map)
            .bindTooltip(popupContent, { permanent: false, direction: 'top' });
        });
    }

    window.onload = initMap;
</script>
</body>
</html>
"""

# Creat the reuse_waste.html template
reuse_waste_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How to Reuse Waste</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .item { border-bottom: 1px solid #ddd; padding: 10px 0; }
        .item a { text-decoration: none; color: blue; }
    </style>
</head>
<body>
    <h1>How to Reduce Waste</h1>
    <p>Agentic flow: What sort of waste you produce would you like to consider for reuse?</p>
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
    <p>Agentic flow: What sort of waste you produce would you like to consider for reduction?</p>
</body>
</html>
"""

# Creat the track_and_monitor.html template
track_and_monitor_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Central Waste Managers - {{ location }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #333; }
        .dash-container { margin-top: 20px; border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Central Waste Managers in {{ location }}</h1>
        <p style="text-align:center; color: #666;">
            Select a waste category below to view real-time transparency and processing metrics.
        </p>
        
        <div class="dash-container">
            <iframe src="{{ dash_url }}" style="width:100%; height:800px; border:none;"></iframe>
        </div>
    </div>
</body>
</html>
"""
