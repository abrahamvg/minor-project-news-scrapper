from flask import Flask, request, jsonify
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_website():
    # Get the URL parameter from the request
    url = request.args.get('url')

    if url is None:
        return jsonify({'error': 'URL parameter is missing.'}), 400

    # Send a request to the website to retrieve the HTML content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        heading = soup.find('title').get_text()

        # Define selectors to remove specific elements
        selectors = ['logo','byline_action','logo','timestamp', 'trending', 'widget', 'footer', 'new_', 'header', 'nav', 'sidebar', 'slick', 'slider', 'personalise', 'visualstories', 'popup', 'subscribe', 'meta', 'caption', 'rhs', 'recommendation', 'comment', 'share']

        # Remove elements matching selectors
        # Remove elements matching selectors
        for selector in selectors:
            divs = soup.find_all('div', class_=re.compile(selector, re.IGNORECASE))
            for div in divs:
                div.extract()
        # Remove elements matching selectors
        for selector in selectors:
            divs = soup.find_all('div', id=re.compile(selector, re.IGNORECASE))
            for div in divs:
                div.extract()

        # Remove elements matching specific tags
        for selector in ['header', 'footer', 'aside', 'nav', 'svg', 'ol', 'ul', 'title', 'h1', 'figcaption']:
            elements = soup.find_all(selector)
            for element in elements:
                element.extract()

        # Get the text content and remove unnecessary whitespaces
        lines = soup.get_text().split("\n")
        final_text = " ".join([line.strip() for line in lines if line.strip() != ""])

        return jsonify({'output': final_text, 'heading': heading})

    else:
        return jsonify({'error': 'Failed to retrieve data from the website.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
