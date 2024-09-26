from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)


def clean_text(text):
    return re.sub(r'\(.*?\)|\[.*?\)', '', text).strip()

def format_animal_name(animal_name):
    return re.sub(r'\s+', '_', animal_name.strip())

def get_animal_info(animal_name):
    formatted_name = format_animal_name(animal_name)
    url = f"https://ru.wikipedia.org/wiki/{formatted_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    image = soup.find(class_='infobox-image')
    image_url = "https:" + image.find('img')['src'] if image else None
    article_url = url

    info_texts = [clean_text(paragraph.text) for paragraph in paragraphs[:3]]
    return {"info": info_texts, "image_url": image_url, "article_url": article_url}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    animal_name = request.form.get('animal')
    animal_info = get_animal_info(animal_name)

    return render_template('result.html', 
                            animal=animal_name, 
                            image_url=animal_info["image_url"],
                            info=animal_info["info"][0],
                            article_url=animal_info["article_url"])

if __name__ == '__main__':
    app.run(debug=True)