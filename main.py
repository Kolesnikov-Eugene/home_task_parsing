import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


URL = 'https://habr.com'
KEYWORDS = ['physical', 'Mathematics *', 'Programming *', 'Java *', 'Python *']
ua = UserAgent()
headers = {'accept': '*/*', 'user-agent': ua.firefox}

if __name__ == '__main__':
    res = requests.get(URL, headers=headers)
    text = res.text

    soup = BeautifulSoup(text, features='html.parser')

    articles = soup.find_all("article")
    for article in articles:
        #receive preview of the article
        previews = article.find_all(class_="tm-article-snippet__hubs-item-link")
        previews = [preview.text.strip() for preview in previews]
        for preview in previews:
            if preview in KEYWORDS:
                date_ = article.find('time').get('title')
                title = article.find('h2').find('span').text
                href = article.find(class_='tm-article-snippet__title-link').attrs['href']
                print(f'{date_} - {title} - {URL}{href}')
                #additional part of a home task
                new_response = requests.get(f'{URL}{href}')
                full_text = new_response.text
                full_soup = BeautifulSoup(full_text, features='html.parser')
                #getting full text of the article
                f_art = full_soup.find(id='post-content-body').getText('p')
                for word in KEYWORDS:
                    if word in f_art:
                        print(f_art)

