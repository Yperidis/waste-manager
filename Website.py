from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for
import random
import requests
from Web_data import index_html, item_input_html, dashboard_html, disposal_options_html, reduce_waste_html
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urljoin

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
        return redirect(url_for('dashboard', name=name, location=location))
    
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
    app.run(debug=True)

# Save index.html file
with open("templates/index.html", "w") as file:
    file.write(index_html)

# Save item_input.html file
with open("templates/item_input.html", "w") as file:
    file.write(item_input_html)

with open("templates/dashboard.html", "w") as file:
    file.write(dashboard_html)

# Save disposal_options.html file
with open("templates/disposal_options.html", "w") as file:
    file.write(disposal_options_html)

with open("templates/reduce_waste.html", "w") as file:
    file.write(reduce_waste_html)
