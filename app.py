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
        selectors = ['info','inSideInd','hidden','report','btmFooter','toaster','c-compact-river','next','social-buttons','socialButtons','social','logo','byline_action','logo','timestamp', 'trending', 'widget', 'footer', 'new_', 'header', 'nav', 'slick', 'slider', 'personalise', 'visualstories', 'popup', 'subscribe', 'meta', 'caption', 'rhs', 'recommendation', 'comment', 'share', 'newsletter']

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
        for selector in ['header', 'footer', 'aside', 'nav', 'svg', 'title', 'h1', 'figcaption', 'button']:
            elements = soup.find_all(selector)
            for element in elements:
                element.extract()

        for text in [heading,'Ad Feedback','Trending', 'Also Read','Sign Up','Get Alerts','Share this on', 'Skip to main content', 'Top news', 'Latest news', 'Follow for more', 'Popular From' ,'opt out at any time', 'more newsletters', 'Privacy Policy', ]:
            div = soup.find_all(string = re.compile(text, re.IGNORECASE))
            for i in div:
                i.parent.extract()

        # Get the text content and remove unnecessary whitespaces
        lines = []
        for paragraph in soup.find_all('p'):
            lines.extend(paragraph.get_text().splitlines())

        final_text = " ".join([line.strip() for line in lines if line.strip() != ""])

        return jsonify({'output': final_text, 'heading': heading})

    else:
        return jsonify({'error': 'Failed to retrieve data from the website.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
