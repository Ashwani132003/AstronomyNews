from flask import Flask, render_template, request
import requests
import json
from datetime import date, timedelta
import logging

current_date = date.today()
start_date = current_date - timedelta(days=15)



app = Flask(__name__, static_url_path='', static_folder='static')


app.config['DEBUG'] = True

# Configure logging
logging.basicConfig(level=logging.DEBUG)



@app.route('/')
def index():
    url = ('https://newsapi.org/v2/everything?'
       f'q=Astronomy&'
       f'from={start_date}&'
       f'to={current_date}&'
       f'sortBy=popularity&'
       'apiKey=ae8e6d4a75d7462e8f1e248b2e139a2c')
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        articles = json_data['articles']
        processed_articles = []
        for article in articles:
            processed_article = {
                "title": article.get("title", ""),
                "author": article.get("author", ""),
                "published_date": article.get("publishedAt", ""),
                "description": article.get("description", ""),
                "url": article.get("url", "")
            }
            if "Undefined" not in processed_article.values():
                processed_articles.append(processed_article)

        # Get the current page number from the query parameters
        page = int(request.args.get('page', 1))
        per_page = 10  # Number of articles per page
        start = (page - 1) * per_page
        end = start + per_page
        paginated_articles = processed_articles[start:end]

        return render_template('index.html', articles=paginated_articles, page=page, per_page=per_page)
    else:
        return f"Error: {response.status_code}"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
