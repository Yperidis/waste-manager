from analytics import init_dashboard
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, Response, url_for
import random
import requests
import os
from web_data import (
    index_html, 
    item_input_html, 
    dashboard_html, 
    disposal_options_html, 
    reduce_waste_html, 
    reuse_waste_html, 
    track_and_monitor_html,
)
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
init_dashboard(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Example metric
requests_total = Counter('http_requests_total', 'Total HTTP requests')

@app.before_request
def before_request():
    requests_total.inc()


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


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
    return redirect(url_for('dashboard', name=name, location=location))


@app.route('/dashboard/<name>/<location>')
def dashboard(name, location):
    return render_template('dashboard.html', name=name, location=location)


@app.route('/item_input/<name>/<location>', defaults={'mode': None}, methods=['GET', 'POST'])
@app.route('/item_input/<name>/<location>/<mode>', methods=['GET', 'POST'])
def item_input(name, location, mode):
    if request.method == 'POST':
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
            'category': category,
            'subcategory': subcategory,
            'condition': condition,
            'dirty': dirty,
            'photo': photo_filename
        })
        item_index = len(items) - 1

        if mode == 'track':
            return redirect(url_for('track_and_monitor', name=name, location=location, item_index=item_index))
        else:
            return redirect(url_for('disposal_options', name=name, location=location))
    
    categories = {
        "Plastics": ["PET", "PE", "PS", "PVC", "PP", "Plastic Films"],
        "Plastic Films": ["LDP", "HDP"],
        "Textiles": ["H&M"],
    }

    return render_template('item_input.html', name=name, location=location, categories=categories)


@app.route('/disposal_options/<location>')
def disposal_options(location):
    berlin_buyers = ["BSR", "ALBA"] + [f"Buyer {i}" for i in range(1, 11)]
    athens_buyers = [f"Municipality {i}" for i in range(1, 11)] + [f"Buyer {i}" for i in range(1, 11)]
    
    buyers = berlin_buyers if location == "Berlin" else athens_buyers
    # Generate buyer data with position, price, and carbon footprint
    buyer_data = []
    for buyer in buyers:
        buyer_data.append({
            "name": buyer,
            "lat": random.uniform(52.3, 52.6) if location == "Berlin" else random.uniform(37.9, 38.1),
            "lon": random.uniform(13.2, 13.6) if location == "Berlin" else random.uniform(23.6, 23.9),
            "price": round(random.uniform(5.0, 50.0), 2),  # price in EUR
            "carbon": round(random.uniform(1.0, 20.0), 2)  # kg CO₂ per transaction
        })
    buyer_positions = {
        buyer: {
            "lat": round(random.uniform(52.3, 52.6), 4) if location == "Berlin" else round(random.uniform(37.9, 38.1), 4),
            "lon": round(random.uniform(13.2, 13.6), 4) if location == "Berlin" else round(random.uniform(23.6, 23.9), 4),
            "price": round(random.uniform(5.0, 50.0), 2),
            "carbon": round(random.uniform(1.0, 20.0), 2),
        }
        for buyer in buyers
    }
    
    return render_template('disposal_options.html', location=location, buyers=buyer_data, buyer_positions=buyer_positions)


@app.route('/track_and_monitor/<location>/<int:item_index>')
def track_and_monitor(location, item_index):
    item = items[item_index]
    dash_url = f"/analytics/?location={location}"
    print(f"Serving monitoring dashboard for item {item} at location {location}")
    show_dashboard = item.get('category', '').lower() == 'textiles'
    return render_template(
        'track_and_monitor.html', 
        location=location, 
        item=item, 
        show_dashboard=show_dashboard, 
        dash_url=dash_url
        )


@app.route('/reuse_waste')
def reuse_waste():
    # Scrape information from an external site that has content on reducing waste.
    return render_template('reuse_waste.html')


@app.route('/reduce_waste')
def reduce_waste():
    # Scrape information from an external site that has content on reducing waste.
    results = scrape_reduce_waste()
    return render_template('reduce_waste.html', results=results)

def is_allowed(url, user_agent='*'):
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    robots_url = urljoin(base_url, 'robots.txt')

    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)

def scrape_reduce_waste():
    """
    This function uses requests and BeautifulSoup to perform a respectful crawl.
    Ensure the target site allows crawling (check its robots.txt) and adjust the URL and parsing logic accordingly.
    """
    # Replace with a valid URL that allows crawling.
    url = "https://onetreeplanted.org"
    headers = {
        'User-Agent': '*'}

    if is_allowed(url, 'YourBotName'):
        response = requests.get(url)

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Error fetching data:", e)
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        
        # The following parsing logic assumes that each article is contained in an <article> tag.
        # Adjust selectors as required by the structure of your target page.
        articles = soup.find_all('article')
        for article in articles:
            title_tag = article.find('h2')
            summary_tag = article.find('p')
            link_tag = article.find('a')
            if title_tag and summary_tag and link_tag:
                title = title_tag.get_text(strip=True)
                summary = summary_tag.get_text(strip=True)
                link = link_tag.get('href')
                results.append({'title': title, 'summary': summary, 'link': link})
        
        return results
    else:
        print("Access to this URL is disallowed by robots.txt")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Listen on 0.0.0.0 so external requests reach you
    app.run(host='0.0.0.0', port=port, debug=False)
    # app.run(debug=True)

# Save index.html file
with open("templates/index.html", "w") as file:
    file.write(index_html)

with open("templates/dashboard.html", "w") as file:
    file.write(dashboard_html)

# Save disposal_options.html file
with open("templates/disposal_options.html", "w") as file:
    file.write(disposal_options_html)

# Save item_input.html file
with open("templates/item_input.html", "w") as file:
    file.write(item_input_html)

with open("templates/reuse_waste.html", "w") as file:
    file.write(reuse_waste_html)

with open("templates/reduce_waste.html", "w") as file:
    file.write(reduce_waste_html)

with open("templates/track_and_monitor.html", "w") as file:
    file.write(track_and_monitor_html)