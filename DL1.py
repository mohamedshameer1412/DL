import requests
from bs4 import BeautifulSoup
import csv
import re

# Define the URL of the WikiHow page to scrape
url = 'https://www.wikihow.com/Special:Randomizer'

# Open the CSV file for writing
with open('wikiHow.csv', mode='a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    for count in range(30):
        # Send an HTTP request to the URL and receive the HTML content
        response = requests.get(url)
        html_content = response.content

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        article_title = soup.find('title').text.strip()
        print(article_title + " " + str(count))

        # Extract the subheadings and paragraphs using the appropriate HTML tags
        subheadings = []
        paragraphs = []

        steps = soup.find_all('div', {'class': 'step'})
        for step in steps:
            subheading_element = step.find('b')
            if subheading_element is not None:
                subheading_text = subheading_element.text.strip().replace('\n', '')
                subheading_text = subheading_text.encode('ascii', errors='ignore').decode()
                subheading_text = re.sub(r'\s+', ' ', subheading_text)
                print(subheading_text)
                subheadings.append(subheading_text)
                subheading_element.extract()

            for span_tag in step.find_all('span'):
                span_tag.extract()

            paragraph_text = step.text.strip().replace('\n', ' ').replace('\r', '')
            paragraph_text = paragraph_text.encode('ascii', errors='ignore').decode()
            paragraph_text = re.sub(r'\s+', ' ', paragraph_text)
            print(paragraph_text)
            paragraphs.append(paragraph_text)

        # Write the extracted data to the CSV file
        if len(subheadings):
            for i in range(len(subheadings)):
                writer.writerow([article_title, subheadings[i], paragraphs[i]])
